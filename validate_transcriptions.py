#!/usr/bin/env python3
"""Validator for the IPA transcription style defined in transcription_guide.md.

Implements the "Machine-checkable constraints" of §11:
  - banned symbols and sequences (regex checks)
  - capitals only in letter-name tokens
  - accent marks only on vowel symbols, with the expected encoding
  - unaccented tokens must be known weak forms (strict mode)
  - token-count parity between source and trans_* fields (JSON mode)

Usage:
  python validate_transcriptions.py --self-test
  python validate_transcriptions.py --text "ðə flɔ́r lǽmp ɪz tɔ́l."
  python validate_transcriptions.py data/questions            # strict scan
  python validate_transcriptions.py --legacy data/questions   # relax rules for
                                    # material that predates the strict style
                                    # (ɛər/ɪər/ʊər, ʌ, ᵻ, weak-form strictness)

Exit code 0 = clean, 1 = violations found, 2 = usage error.
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ACUTE = "́"
GRAVE = "̀"

IPA_VOWELS = set("æɛɪɔɒʊəɜɑ")          # take combining accents directly
LATIN_VOWELS = set("aeiou")             # must arrive precomposed (á é í ó ú)
PRECOMPOSED = set("áéíóúàèìòù")
PHONETIC_LOWER = set("abdefhijklmnoprstuvwz")   # no c g q x y
CONSONANT_IPA = set("ɡŋðθʃʒ")
CAPS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
DIGITS = set("0123456789")
PUNCT = set(" \t\n.,;:!?'\"()[]{}-–—…‘’“”/%&+*=«»^<>_~\\|°±×÷·√∫≈≠≤≥→#@$")

ALLOWED = (PHONETIC_LOWER | CONSONANT_IPA | IPA_VOWELS | PRECOMPOSED
           | {ACUTE, GRAVE} | CAPS | DIGITS | PUNCT)
# chars that have their own dedicated rule (don't double-report as illegal-char)
RULE_COVERED = set("gːˈˌɹɾʔɫʌᵻǽǼ")

SEQUENCE_RULES = [
    ("stress-marks", re.compile(r"[ˈˌ]"), "IPA stress mark — use acute/grave on the vowel"),
    ("length-mark", re.compile(r"ː"), "length mark — long vowels are glide-spelled or ɑ"),
    ("banned-allophones", re.compile(r"[ɹɾʔɫ]"), "use plain r / t / l"),
    ("banned-vowels", re.compile(r"[ʌᵻ]"), "STRUT is ə; ᵻ is never used"),
    ("centering-schwa", re.compile("[ɛɪʊ][́̀]?ər"), "write ɛr / ɪr / ʊr"),
    ("traditional-diphthong", re.compile(r"eɪ|əʊ|oʊ|aɪ|aʊ|ɔɪ"), "write ej ow aj aw ɔj"),
    ("what-accented", re.compile("wɒ" + ACUTE + "t"), "what is always bare wɒt"),
    ("precomposed-ae", re.compile("[ǽǼ]"), "precomposed ae-acute — write æ + combining acute (U+0301)"),
]
LEGACY_SKIP = {"banned-vowels", "centering-schwa"}

WEAK_FORMS = set("""
ə ən ðə ənd ɔr bət ɪf æz ðən ðət əv tə ɪn ɒn ət baj fɔr frəm wɪð
əp dawn awt aj juw hij ʃij ɪt wij ðej mij hɪm hər əs ðɛm
maj jɔr hɪz ɪts awər ðɛr ðɪs ðijz ðowz
əm ɪz ɑr wəz wər bij bɪn həv həz həd dəz dɪd
kən kʊd wɪl wʊd ʃəl ʃʊd mej majt məst
nɒt səm ɔl ðər wɒt
""".split())

NOTATION_WORDS = set("""
sin cos tan cot sec csc log ln exp sqrt abs max min lim sup inf arg mod det dim gcd
km cm mm kg mg ml mL kW Hz kHz MHz GHz dB mph
""".split())
GREEK_SINGLES = set("πθφλμσδΔΣΩαβγε∞")


def is_notation(seg):
    """Formula/unit/variable tokens pass through verbatim (guide §9)."""
    if any(c in DIGITS for c in seg):
        return True                           # 1970s, mc^2, 2nd
    if seg in NOTATION_WORDS or seg in GREEK_SINGLES:
        return True
    if seg.isascii():
        if len(seg) == 1 and seg.isalpha():
            return True                       # bare variable: e, x, n
        if any(c in "()=^+*/<>\\|_~" for c in seg):
            return True                       # sin(x, km/h, f(x)=...
    return False


def check_string(text, legacy=False):
    """Return a list of (rule, detail) violations for one transcription string."""
    out = []

    for rule, rx, msg in SEQUENCE_RULES:
        if legacy and rule in LEGACY_SKIP:
            continue
        for m in rx.finditer(text):
            out.append((rule, f"'{snippet(text, m.start())}' — {msg}"))

    allowed = ALLOWED | ({"ʌ", "ᵻ"} if legacy else set())

    # accent placement / encoding (skip inside all-caps letter-name segments,
    # which never carry accents anyway)
    for i, ch in enumerate(text):
        if ch in (ACUTE, GRAVE):
            prev = text[i - 1] if i else ""
            if prev in IPA_VOWELS or (legacy and prev == "ʌ"):
                continue
            if prev in LATIN_VOWELS:
                out.append(("encoding-decomposed",
                            f"'{snippet(text, i - 1)}' — a e i o u must be precomposed (á é í ó ú)"))
            else:
                out.append(("accent-misplaced",
                            f"'{snippet(text, i - 1)}' — accent must follow a vowel symbol"))

    # token-level checks
    for raw in text.split():
        tok = raw.strip("".join(PUNCT - {" "}))
        if not tok:
            continue
        for seg in tok.split("-"):
            seg = seg.strip("".join(PUNCT - {" "}))
            if not seg:
                continue
            if is_notation(seg):
                continue                      # formulas, units, variables (§9)
            if any(c in CAPS for c in seg):
                if not all(c in CAPS for c in seg):
                    out.append(("mixed-capitals",
                                f"'{seg}' — capitals only as whole letter-name tokens"))
                continue                      # USB, T — letter-name segment
            if "g" in seg:
                out.append(("ascii-g", f"'{seg}' — must be IPA ɡ (U+0261)"))
            for ch in seg:
                if ch not in allowed and ch not in RULE_COVERED:
                    out.append(("illegal-char", f"'{ch}' (U+{ord(ch):04X}) in '{seg}'"))
            nfd = unicodedata.normalize("NFD", seg)
            acutes = nfd.count(ACUTE)
            if acutes > 1:
                out.append(("multiple-acutes", f"'{seg}' — one primary stress per word"))
            elif acutes == 0 and not legacy:
                base = seg.split("'")[0] or seg
                if base not in WEAK_FORMS and seg not in WEAK_FORMS:
                    out.append(("unaccented-token",
                                f"'{seg}' — not a §6 weak form, so it needs an acute"))
    return out


def snippet(text, pos, width=12):
    return text[max(0, pos - width // 2): pos + width].replace("\n", " ")


def check_json_file(path, legacy=False):
    """Validate every trans_* field of a question file. Returns list of (loc, rule, detail)."""
    out = []
    items = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    pairs = [("Question", "trans_Question"), ("RightAnswer", "trans_RightAnswer"),
             ("Explanation", "trans_Explanation")]
    for idx, item in enumerate(items):
        fields = []
        for src_key, trans_key in pairs:
            fields.append((trans_key, item.get(src_key), item.get(trans_key)))
        for j, (src, trans) in enumerate(zip(item.get("WrongAnswers", []),
                                             item.get("trans_WrongAnswers", []))):
            fields.append((f"trans_WrongAnswers[{j}]", src, trans))
        for name, src, trans in fields:
            if not isinstance(trans, str):
                continue
            loc = f"{Path(path).name}[{idx}].{name}"
            for rule, detail in check_string(trans, legacy=legacy):
                out.append((loc, rule, detail))
            if isinstance(src, str) and len(src.split()) != len(trans.split()):
                out.append((loc, "token-count",
                            f"source has {len(src.split())} tokens, transcription {len(trans.split())}"))
    return out


def D(s):
    """Undo NFC normalization that editors may apply to this source file: the
    project style wants combining accents on IPA letters (never precomposed ǽ)."""
    return s.replace("\u01fd", "\u00e6\u0301").replace("\u01fc", "\u00c6\u0301")


VALID_SAMPLES = [D(s) for s in [
    "ðə flɔ́r lǽmp ɪz tɪ́pɪkəlij tɔ́l ənd slɛ́ndər.",
    "wɒt's ðə núwəst dɪzájn frəm ðə 1980s ðət júwd wɛ́r dʊ́rɪŋ ə kúwl ɔ́təm íjvnɪŋ?",
    "ɪf aj həd hǽd wɔ́tər, aj wʊd həv ʃɛ́rd ɪt.",
    "aj ríjəlàjzd ðət ðǽt wəz rɔ́ŋ, túw léjt.",
    "maj fɑ́ðər júwzd ə USB drájv tə rɪkɔ́rd ðə rɪzə́lts — wɛ́r dəz ðə mə́nij kə́m frɒ́m?",
    "dɪvájd-ənd-kɒ́ŋkər rɪkɜ́rənsɪz ɒn ə T-ʃɜ́rt frəm ðə '70s",
    "mæ̀θəmǽtɪkəl əsówsijèjtɪd wɔ́l-tə-wɔ́l",
    "ájnstàjnz ɪkwéjʒən e = mc^2 rɪléjts ɛ́nərdʒij ənd mǽs.",
    "ðə fə́ŋkʃən sin(x) ɪz pɪ̀rijɒ́dɪk, ə̀nlájk log(x).",
]]
INVALID_SAMPLES = [(D(s), r) for s, r in [
    ("wɛ́ər", "centering-schwa"),
    ("bʌt", "banned-vowels"),
    ("kwɑ́ntᵻtij", "banned-vowels"),
    ("ðə gɑ́rmənt", "ascii-g"),
    ("wɒ́t ɪz ðɪs", "what-accented"),
    ("ˈleðər", "stress-marks"),
    ("wɜːld", "length-mark"),
    ("meɪd", "traditional-diphthong"),
    ("Méjd", "mixed-capitals"),
    ("fʊtwɛr ɪz", "unaccented-token"),
    ("ɹɪ́lij", "banned-allophones"),
    ("kɒ́ŋkə́r", "multiple-acutes"),
    ("ðə leather dʒǽkət", "unaccented-token"),
]]


def self_test():
    failures = 0
    for s in VALID_SAMPLES:
        got = check_string(s)
        if got:
            failures += 1
            print(f"FAIL (expected clean): {s}")
            for rule, detail in got:
                print(f"    {rule}: {detail}")
    for s, expected in INVALID_SAMPLES:
        rules = {rule for rule, _ in check_string(s)}
        if expected not in rules:
            failures += 1
            print(f"FAIL (expected {expected}): {s} -> {sorted(rules)}")
    total = len(VALID_SAMPLES) + len(INVALID_SAMPLES)
    print(f"self-test: {total - failures}/{total} passed")
    return failures == 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", help="JSON files or directories (default: data/questions)")
    ap.add_argument("--text", help="validate a single transcription string")
    ap.add_argument("--legacy", action="store_true",
                    help="relax rules for material that predates the strict style")
    ap.add_argument("--summary", action="store_true", help="print per-rule counts only")
    ap.add_argument("--limit", type=int, default=40, help="max individual violations to print")
    ap.add_argument("--self-test", action="store_true", help="run built-in test cases")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(0 if self_test() else 1)

    if args.text is not None:
        violations = [("<text>", r, d) for r, d in check_string(args.text, legacy=args.legacy)]
    else:
        files = []
        for p in (args.paths or ["data/questions"]):
            p = Path(p)
            files += sorted(p.glob("*.json")) if p.is_dir() else [p]
        if not files:
            print("no JSON files found", file=sys.stderr)
            sys.exit(2)
        violations = []
        for f in files:
            violations += check_json_file(f, legacy=args.legacy)

    if not args.summary:
        for loc, rule, detail in violations[: args.limit]:
            print(f"{loc}: {rule}: {detail}")
        if len(violations) > args.limit:
            print(f"... and {len(violations) - args.limit} more")

    counts = {}
    for _, rule, _ in violations:
        counts[rule] = counts.get(rule, 0) + 1
    mode = "legacy" if args.legacy else "strict"
    print(f"\n{mode} mode: {len(violations)} violation(s)"
          + (" — " + ", ".join(f"{r}: {n}" for r, n in sorted(counts.items(), key=lambda x: -x[1]))
             if counts else ""))
    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
