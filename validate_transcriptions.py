#!/usr/bin/env python3
"""Validator for the IPA transcription style defined in transcription_guide.md.

Implements the "Machine-checkable constraints" of §11:
  - banned symbols and sequences (regex checks)
  - capitals only in letter-name tokens
  - accent marks only on vowel symbols, with the expected encoding
    - Latin vowel bases use the required j/w glide notation
  - unaccented tokens must be known weak forms (strict mode)
    - complete source/transcription pairs and layout parity (JSON mode)

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
    ("what-accented", re.compile("wɒ" + ACUTE + "t"), "what is always bare wɒt"),
    ("precomposed-ae", re.compile("[ǽǼ]"), "precomposed ae-acute — write æ + combining acute (U+0301)"),
]
LEGACY_SKIP = {"banned-vowels", "centering-schwa"}

WEAK_FORMS = set("""
ə ən ðə ðij ənd ɔr bət ɪf æz ðən ðət əv tə ɪn ɒn ət baj fɔr frəm wɪð
əp dawn awt aj juw hij ʃij ɪt wij ðej mij hɪm hər əs ðɛm
maj jɔr hɪz ɪts awər ðɛr ðɪs ðijz ðowz
əm ɪz ɑr wəz wər bij bɪn həv həz həd dəz dɪd
kən kʊd wɪl wʊd ʃəl ʃʊd mej majt məst
nɒt səm ɔl ðər wɒt wɒts
""".split())

NOTATION_WORDS = set("""
sin cos tan cot sec csc log ln exp sqrt abs max min lim sup inf arg mod det dim gcd
km cm mm kg mg ml mL kW Hz kHz MHz GHz dB mph
""".split())
GREEK_SINGLES = set("πθφλμσδΔΣΩαβγε∞")
TRADITIONAL_DIPHTHONG = re.compile(r"eɪ|əʊ|oʊ|aɪ|aʊ|ɔɪ")
REQUIRED_GLIDES = {"a": "jw", "e": "j", "i": "j", "o": "w", "u": "w"}


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


def token_core(raw):
    """Remove surrounding punctuation while preserving phonetic content."""
    return raw.strip("".join(PUNCT - {" "}))


def phonetic_initial(raw):
    """Classify an inspectable phonetic token's first sound."""
    tok = token_core(raw)
    if not tok:
        return None
    seg = tok.split("-", 1)[0]
    if is_notation(seg) or any(c in CAPS or c in DIGITS for c in seg):
        return None
    first = seg[0]
    if first in IPA_VOWELS or first in LATIN_VOWELS or first in PRECOMPOSED:
        return "vowel"
    if first in PHONETIC_LOWER or first in CONSONANT_IPA:
        return "consonant"
    return None


def stressless(text):
    """Return decomposed text without this style's stress accents."""
    return "".join(ch for ch in unicodedata.normalize("NFD", text)
                   if ch not in {ACUTE, GRAVE})


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

    # The weak form of "the" follows the next sound. Pass-through tokens such
    # as digits and letter names cannot be inferred from the transcription.
    raw_tokens = text.split()
    for index, raw in enumerate(raw_tokens[:-1]):
        form = token_core(raw)
        if form not in {"ðə", "ðij"}:
            continue
        initial = phonetic_initial(raw_tokens[index + 1])
        if form == "ðə" and initial == "vowel":
            out.append(("the-context", f"'{form} {token_core(raw_tokens[index + 1])}' — use ðij before a vowel sound"))
        elif form == "ðij" and initial == "consonant":
            out.append(("the-context", f"'{form} {token_core(raw_tokens[index + 1])}' — use ðə before a consonant sound"))

    # token-level checks
    for raw in raw_tokens:
        tok = token_core(raw)
        if not tok:
            continue
        for seg in tok.split("-"):
            seg = seg.strip("".join(PUNCT - {" "}))
            if not seg:
                continue
            if is_notation(seg):
                continue                      # formulas, units, variables (§9)
            phonetic_seg = seg.replace("'", "").replace("’", "")
            if phonetic_seg != seg:
                out.append(("word-apostrophe",
                            f"'{seg}' — omit apostrophes inside phonetic words"))
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
            vowel_shape = stressless(phonetic_seg)
            traditional_matches = list(TRADITIONAL_DIPHTHONG.finditer(vowel_shape))
            if traditional_matches:
                out.append(("traditional-diphthong",
                            f"'{seg}' — write ij uw ej ow aj aw ɔj"))
            traditional_starts = {match.start() for match in traditional_matches}
            for index, ch in enumerate(vowel_shape):
                required = REQUIRED_GLIDES.get(ch)
                if required is None or index in traditional_starts:
                    continue
                following = vowel_shape[index + 1] if index + 1 < len(vowel_shape) else ""
                if not following or following not in required:
                    forms = " / ".join(ch + glide for glide in required)
                    out.append(("invalid-glide-vowel",
                                f"'{seg}' — {ch} must occur as {forms}"))
            nfd = unicodedata.normalize("NFD", phonetic_seg)
            acutes = nfd.count(ACUTE)
            if acutes > 1:
                out.append(("multiple-acutes", f"'{seg}' — one primary stress per word"))
            elif acutes == 0 and not legacy:
                if phonetic_seg not in WEAK_FORMS:
                    out.append(("unaccented-token",
                                f"'{seg}' — not a §6 weak form, so it needs an acute"))
    return out


def snippet(text, pos, width=12):
    return text[max(0, pos - width // 2): pos + width].replace("\n", " ")


def layout_skeleton(token):
    """Return punctuation and symbols, excluding the omitted apostrophe class."""
    return "".join(ch for ch in token
                   if ch not in "'’" and unicodedata.category(ch)[0] in "PS")


def check_source_layout(source, transcription):
    """Check mechanically preservable layout between one source/transcription pair."""
    out = []
    source_space = re.split(r"\S+", source)
    trans_space = re.split(r"\S+", transcription)
    if source_space != trans_space:
        out.append(("whitespace-layout",
                    f"source whitespace {source_space!r}, transcription {trans_space!r}"))

    source_tokens = re.findall(r"\S+", source)
    trans_tokens = re.findall(r"\S+", transcription)
    if len(source_tokens) != len(trans_tokens):
        out.append(("token-count",
                    f"source has {len(source_tokens)} tokens, transcription {len(trans_tokens)}"))
        return out

    for index, (source_token, trans_token) in enumerate(zip(source_tokens, trans_tokens), 1):
        source_digits = re.findall(r"\d+", source_token)
        trans_digits = re.findall(r"\d+", trans_token)
        if source_digits != trans_digits:
            out.append(("digits-changed",
                        f"token {index}: source digits {source_digits!r}, transcription {trans_digits!r}"))

        source_layout = layout_skeleton(source_token)
        trans_layout = layout_skeleton(trans_token)
        if source_layout != trans_layout:
            out.append(("punctuation-layout",
                        f"token {index}: source {source_layout!r}, transcription {trans_layout!r}"))
    return out


def check_json_items(items, filename="<data>", legacy=False):
    """Validate parsed question items. Returns a list of (location, rule, detail)."""
    out = []
    pairs = [("Question", "trans_Question"), ("RightAnswer", "trans_RightAnswer"),
             ("Explanation", "trans_Explanation")]
    for idx, item in enumerate(items):
        fields = []
        for src_key, trans_key in pairs:
            source = item.get(src_key)
            transcription = item.get(trans_key)
            if isinstance(source, str):
                if isinstance(transcription, str):
                    fields.append((trans_key, source, transcription))
                else:
                    out.append((f"{filename}[{idx}].{trans_key}", "missing-transcription",
                                f"{src_key} is present but {trans_key} is missing or not text"))

        source_answers = item.get("WrongAnswers", [])
        trans_answers = item.get("trans_WrongAnswers")
        if isinstance(source_answers, list):
            if not isinstance(trans_answers, list):
                if source_answers:
                    out.append((f"{filename}[{idx}].trans_WrongAnswers", "missing-transcription",
                                "WrongAnswers is present but trans_WrongAnswers is missing or not a list"))
                trans_answers = []
            elif len(source_answers) != len(trans_answers):
                out.append((f"{filename}[{idx}].trans_WrongAnswers", "answer-count",
                            f"source has {len(source_answers)} answers, transcription has {len(trans_answers)}"))
            for j, (source, transcription) in enumerate(zip(source_answers, trans_answers)):
                name = f"trans_WrongAnswers[{j}]"
                if isinstance(source, str) and isinstance(transcription, str):
                    fields.append((name, source, transcription))
                elif isinstance(source, str):
                    out.append((f"{filename}[{idx}].{name}", "missing-transcription",
                                f"WrongAnswers[{j}] is present but {name} is not text"))

        for name, src, trans in fields:
            loc = f"{filename}[{idx}].{name}"
            for rule, detail in check_string(trans, legacy=legacy):
                out.append((loc, rule, detail))
            for rule, detail in check_source_layout(src, trans):
                out.append((loc, rule, detail))
    return out


def check_json_file(path, legacy=False):
    """Validate every source/transcription pair in a question file."""
    items = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    return check_json_items(items, Path(path).name, legacy=legacy)


def D(s):
    """Undo NFC normalization that editors may apply to this source file: the
    project style wants combining accents on IPA letters (never precomposed ǽ)."""
    return s.replace("\u01fd", "\u00e6\u0301").replace("\u01fc", "\u00c6\u0301")


VALID_SAMPLES = [D(s) for s in [
    "ðə flɔ́r lǽmp ɪz tɪ́pɪkəlij tɔ́l ənd slɛ́ndər.",
    "wɒts ðə núwəst dɪzájn frəm ðə 1980s ðət júwd wɛ́r dʊ́rɪŋ ə kúwl ɔ́təm íjvnɪŋ?",
    "ɪf aj həd hǽd wɔ́tər, aj wʊd həv ʃɛ́rd ɪt.",
    "aj ríjəlàjzd ðət ðǽt wəz rɔ́ŋ, túw léjt.",
    "maj fɑ́ðər júwzd ə USB drájv tə rɪkɔ́rd ðə rɪzə́lts — wɛ́r dəz ðə mə́nij kə́m frɒ́m?",
    "dɪvájd-ənd-kɒ́ŋkər rɪkɜ́rənsɪz ɒn ə T-ʃɜ́rt frəm ðə '70s",
    "mæ̀θəmǽtɪkəl əsówsijèjtɪd wɔ́l-tə-wɔ́l",
    "ájnstàjnz ɪkwéjʒən e = mc^2 rɪléjts ɛ́nərdʒij ənd mǽs.",
    "ðə fə́ŋkʃən sin(x) ɪz pɪ̀rijɒ́dɪk, ə̀nlájk log(x).",
    "ðij ǽpəl ənd ðə júwnɪt",
    "míj dúw méj nów tájm dáwn tʃɔ́js",
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
    ("ðə ǽpəl", "the-context"),
    ("ðij júwnɪt", "the-context"),
    ("ɪt's", "word-apostrophe"),
    ("wɛ́rər’z", "word-apostrophe"),
    ("mí dú mé", "invalid-glide-vowel"),
    ("méɪd óʊn áɪ áʊ ɔ́ɪ", "traditional-diphthong"),
]]

VALID_LAYOUT_SAMPLES = [
    ("What's wrong?", "wɒts rɔ́ŋ?"),
    ("O'Connor left.", "owkɒ́nər lɛ́ft."),
    ("T-shirt '70s", "T-ʃɜ́rt '70s"),
]

INVALID_LAYOUT_SAMPLES = [
    ("Hello,  world!", "həlów wɜ́rld.", {"whitespace-layout", "punctuation-layout"}),
    ("Use 1980s.", "júwz 1970s.", {"digits-changed"}),
    ("one two", "wə́n", {"whitespace-layout", "token-count"}),
    (" one", "wə́n ", {"whitespace-layout"}),
]

VALID_JSON_SAMPLES = [
    [{"Question": "What's wrong?", "trans_Question": "wɒts rɔ́ŋ?",
      "WrongAnswers": ["O'Connor left."], "trans_WrongAnswers": ["owkɒ́nər lɛ́ft."]}],
]

INVALID_JSON_SAMPLES = [
    ([{"Question": "Hi"}], {"missing-transcription"}),
    ([{"WrongAnswers": ["a", "b"], "trans_WrongAnswers": ["ə"]}], {"answer-count"}),
    ([{"WrongAnswers": [], "trans_WrongAnswers": ["ə"]}], {"answer-count"}),
    ([{"Question": "Hello,  world!", "trans_Question": "həlów wɜ́rld."}],
     {"whitespace-layout", "punctuation-layout"}),
]


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
    for source, transcription in VALID_LAYOUT_SAMPLES:
        got = check_source_layout(source, transcription)
        if got:
            failures += 1
            print(f"FAIL (expected clean layout): {source!r} -> {transcription!r}: {got}")
    for source, transcription, expected in INVALID_LAYOUT_SAMPLES:
        rules = {rule for rule, _ in check_source_layout(source, transcription)}
        if not expected.issubset(rules):
            failures += 1
            print(f"FAIL (expected {sorted(expected)}): {source!r} -> {transcription!r}: {sorted(rules)}")
    for items in VALID_JSON_SAMPLES:
        got = check_json_items(items)
        if got:
            failures += 1
            print(f"FAIL (expected clean JSON): {items!r} -> {got}")
    for items, expected in INVALID_JSON_SAMPLES:
        rules = {rule for _, rule, _ in check_json_items(items)}
        if not expected.issubset(rules):
            failures += 1
            print(f"FAIL (expected {sorted(expected)}): {items!r} -> {sorted(rules)}")
    total = (len(VALID_SAMPLES) + len(INVALID_SAMPLES) + len(VALID_LAYOUT_SAMPLES)
             + len(INVALID_LAYOUT_SAMPLES) + len(VALID_JSON_SAMPLES)
             + len(INVALID_JSON_SAMPLES))
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
