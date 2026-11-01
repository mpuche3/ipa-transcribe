#!/usr/bin/env python3
"""Validator for the IPA transcription style defined in transcription_guide.md.

Implements the "Machine-checkable constraints" of §11:
  - banned symbols and sequences (regex checks)
  - capitals only in letter-name tokens and approved mixed forms
  - accent marks only on vowel symbols, with the expected encoding
  - Latin vowel bases use the required j/w glide notation
  - unaccented tokens must be known weak forms (strict mode)
  - ruled weak-vowel spellings, where the §4.4 tie-breaker settled the word
  - complete source/transcription pairs and layout parity, allowing only the
    four approved inserted-underscore pairs (JSON mode)

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
    ("epsilon-glide", re.compile("\u025b[\u0300\u0301]j"),
     "FACE is ej — ɛ is DRESS, so ɛ + accent + j is never right (guide §4.2)"),
    ("precomposed-ae", re.compile("[ǽǼ]"), "precomposed ae-acute — write æ + combining acute (U+0301)"),
]
LEGACY_SKIP = {"banned-vowels", "centering-schwa"}

WEAK_FORMS = set("""
ə ən ðə ðij ənd ɔr bət ɪf æz ðən ðət əv tə ɪn ɒn ət baj fɔr pər frəm wɪð
əp dawn awt aj juw hij ʃij ɪt wij ðej mij hɪm hər əs ðɛm
maj jɔr hɪz ɪts ðɛr
ðɪs ðæt ðijz ðowz
də əm ɪz ɑr wəz wər bij bɪn həv həz həd dəz dɪd
kən kʊd wɪl wʊd ʃəl ʃʊd mej majt məst
səm ðər ðərz ðəts wɒt wɒts
""".split())

NOTATION_WORDS = set("""
sin cos tan cot sec csc log ln exp sqrt abs max min lim sup inf arg mod det dim gcd
km cm mm kg mg ml mL kW Hz kHz MHz GHz dB mph
fingerd
""".split())
GREEK_SINGLES = set("πθφλμσδΔΣΩαβγε∞")
TRADITIONAL_DIPHTHONG = re.compile(r"eɪ|əʊ|oʊ|aɪ|aʊ|ɔɪ")
REQUIRED_GLIDES = {"a": "jw", "e": "j", "i": "j", "o": "w", "u": "w"}
LETTER_NAME_SUFFIX = re.compile(r"^([A-Z]+)(ɪz|[sz])$")
DOTTED_LETTER_NAMES = re.compile(r"(?:[A-Z]\.)+[A-Z]")
PHONETIC_WITH_LETTER_NAMES = re.compile(r"([^A-Z]+)([A-Z]+(?:ɪz|[sz])?)")
LETTER_NAME_IZ_FINALS = set("HSX")

APPROVED_SEPARATED_WORDS = {
    "OAuth": "O_ɔ́θ",
    "GenAIOps": "dʒɛ́n_AI_ɒ̀ps",
    "VNet": "V_nɛ́t",
    "qrels": "Q_rɛ́lz",
}
APPROVED_JOINED_WORDS = {"Odéjtə": ("déjtə",)}
APPROVED_SEPARATED_TRANSCRIPTIONS = frozenset(APPROVED_SEPARATED_WORDS.values())
APPROVED_SOURCE_BY_TRANSCRIPTION = {
    **{trans: source for source, trans in APPROVED_SEPARATED_WORDS.items()},
    "Odéjtə": "OData",
}
SPECIAL_WORD_RX = re.compile("|".join(
    re.escape(word) for word in sorted(
        APPROVED_SEPARATED_TRANSCRIPTIONS | APPROVED_JOINED_WORDS.keys(),
        key=len, reverse=True)))
WORD_PART = r"(?:[^\W_]|[\u0300-\u036f])+"
SEPARATED_WORD_SHAPE = re.compile(
    rf"(?:{WORD_PART}_[A-Z]+_{WORD_PART}|[A-Z]+_{WORD_PART}|{WORD_PART}_[A-Z]+)")
APPROVED_LOOKALIKE_SHAPE = re.compile(
    rf"(?:{WORD_PART}_+AI_+{WORD_PART}|[OVQ]_+{WORD_PART})")
SPECIAL_REMAINDER_SPLIT = re.compile(
    "[" + re.escape("".join(PUNCT - {" ", "'", "’"})) + "]+")
APPROVED_TOKEN_WRAPPERS = set(".,;:!?()[]{}'\"‘’“”«»…–—")

# §4.4 spelling tie-breaker: a reduced vowel spelled i/y is ɪ, never ə, and the
# rule outranks M-W's schwa (guide §4.4; design_choices "ɪ or ə by morpheme,
# then spelling").  Ruled and swept 2026-09-26, so no `j[úù]wnə` sequence is
# left anywhere: unit / units / uniform / unified / unifies, universe / universal
# / university, communicate / communication, and punitive.  Only ruled sequences
# are listed — for other i-spelled vowels the tie-breaker is not derivable here.
REDUCED_I_RULINGS = [
    ("júwnə", "júwnɪ"),                 # unit(s), uniform, unified, unifies,
    ("jùwnə", "jùwnɪ"),                 #   universe, communicate, punitive
]

# §7 fixes -ible as ɪbəl, so the reduced vowel spelled i before its b is ɪ, never
# ə (ruled and swept 2026-09-26: flexible, visible, responsible, susceptibility,
# credibility, reproducibility, accessibility).  A blanket əbəl pattern is
# impossible here — -able words legitimately write əbəl — so --text mode uses
# these ruled stems while pair mode derives the rule from the source spelling in
# check_ible_vowel().  *Accountability* was corrected in the same sweep, but only
# its fixed -ity vowel was wrong: it is an -able word, so it has no entry here.
# See the ledger's -ible entries.
IBLE_RULINGS = [
    ("flɛ́ksə", "flɛ́ksɪ"), ("flɛ̀ksə", "flɛ̀ksɪ"),
    ("vɪ́zə", "vɪ́zɪ"), ("vɪ̀zə", "vɪ̀zɪ"),
    ("spɒ́nsə", "spɒ́nsɪ"), ("spɒ̀nsə", "spɒ̀nsɪ"),
    ("sɛ̀ptəbɪ́", "sɛ̀ptɪbɪ́"),
    ("krɛ̀dəbɪ́", "krɛ̀dɪbɪ́"),
    ("dùwsəbɪ́", "dùwsɪbɪ́"),
    ("sɛsəbɪ́", "sɛsɪbɪ́"),
]

PUPIL_RULINGS = {
    "pjúwpɪl": "pjúwpəl",
    "pjúwpɪlz": "pjúwpəlz",
}


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
    seg = re.split(r"[-–—]", tok, maxsplit=1)[0]
    if is_notation(seg) or seg[0] in CAPS:
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


def check_word_stress(display, phonetic, legacy, allow_weak=True):
    acutes = unicodedata.normalize("NFD", phonetic).count(ACUTE)
    if acutes > 1:
        return [("multiple-acutes", f"'{display}' — one primary stress per word")]
    if acutes == 0 and not legacy and (not allow_weak or phonetic not in WEAK_FORMS):
        return [("unaccented-token",
                 f"'{display}' — not a §6 weak form, so it needs an acute")]
    return []


def check_phonetic_component(seg, legacy, check_stress=True):
    """Check a phonetic component, optionally deferring stress to the whole word."""
    out = []
    phonetic_seg = seg.replace("'", "").replace("’", "")
    if phonetic_seg != seg:
        out.append(("word-apostrophe",
                    f"'{seg}' — omit apostrophes inside phonetic words"))
    if any(c in CAPS for c in seg):
        out.append(("mixed-capitals",
                    f"'{seg}' — phonetic components must be lowercase"))
    if "g" in seg:
        out.append(("ascii-g", f"'{seg}' — must be IPA ɡ (U+0261)"))
    allowed = ALLOWED | ({"ʌ", "ᵻ"} if legacy else set())
    for ch in seg:
        if ch not in allowed and ch not in RULE_COVERED:
            out.append(("illegal-char", f"'{ch}' (U+{ord(ch):04X}) in '{seg}'"))
    for wrong, right in REDUCED_I_RULINGS:
        if wrong in phonetic_seg:
            out.append(("reduced-i-spelling",
                        f"'{seg}' — the reduced i takes ɪ, write "
                        f"{phonetic_seg.replace(wrong, right)} (§4.4)"))
    for wrong, right in IBLE_RULINGS:
        if wrong in phonetic_seg:
            out.append(("ible-reduced-vowel",
                        f"'{seg}' — -ible is fixed as ɪbəl, write "
                        f"{phonetic_seg.replace(wrong, right)} (§7)"))
    if phonetic_seg in PUPIL_RULINGS:
        out.append(("pupil-vowel",
                    f"'{seg}' — pupil takes ə, write "
                    f"{PUPIL_RULINGS[phonetic_seg]} (§1.1)"))
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
    if check_stress:
        out.extend(check_word_stress(seg, phonetic_seg, legacy))
    return out


def word_boundaries(text, start, end):
    """Underscores and punctuation delimit words; letters, marks and digits do not."""
    return ((start == 0 or unicodedata.category(text[start - 1])[0] not in "LMN")
            and (end == len(text) or unicodedata.category(text[end])[0] not in "LMN"))


def resembles_approved_separated(word):
    parts = word.split("_")
    for approved in APPROVED_SEPARATED_TRANSCRIPTIONS:
        expected = approved.split("_")
        if len(parts) != len(expected):
            continue
        if (all(part == ref for part, ref in zip(parts, expected)
                if all(c in CAPS for c in ref))
                and any(stressless(part) == stressless(ref)
                        for part, ref in zip(parts, expected)
                        if not all(c in CAPS for c in ref))):
            return True
    return False


def check_special_segment(seg, legacy):
    """Validate approved mixed words and diagnose similar malformed shapes."""
    if "_" not in seg and "Odéjtə" not in seg:
        return None
    matches = [(m.start(), m.end(), m.group()) for m in SPECIAL_WORD_RX.finditer(seg)
               if word_boundaries(seg, m.start(), m.end())]
    for m in SEPARATED_WORD_SHAPE.finditer(seg):
        if (not m.group().isascii()
                and (not is_notation(seg) or resembles_approved_separated(m.group()))
                and word_boundaries(seg, m.start(), m.end())
                and not any(m.start() < end and start < m.end()
                            for start, end, _ in matches)):
            matches.append((m.start(), m.end(), m.group()))
    if not matches:
        return None
    matches.sort()

    out = []
    remaining = []
    masked = []
    previous = 0
    for start, end, word in matches:
        remaining.append(seg[previous:start])
        masked.extend((seg[previous:start], "X"))
        previous = end
        if word in APPROVED_JOINED_WORDS:
            components = APPROVED_JOINED_WORDS[word]
        else:
            components = tuple(part for part in word.split("_")
                               if not all(c in CAPS for c in part))
            if word not in APPROVED_SEPARATED_TRANSCRIPTIONS:
                out.append(("unapproved-separated-word",
                            f"'{word}' — inserted underscores are limited to the approved forms (§9)"))
        for component in components:
            out.extend(check_phonetic_component(component, legacy, check_stress=False))
        out.extend(check_word_stress(word, "".join(components), legacy, allow_weak=False))
    remaining.append(seg[previous:])
    masked.append(seg[previous:])

    # Keep surrounding ASCII code/identifier material as notation, while
    # checking any remaining phonetic material in the same punctuation token.
    if not is_notation("".join(masked)):
        global_rules = {rule for rule, _, _ in SEQUENCE_RULES} | {
            "accent-misplaced", "encoding-decomposed"}
        for fragment in remaining:
            for component in SPECIAL_REMAINDER_SPLIT.split(fragment):
                if component:
                    out.extend(issue for issue in check_string(component, legacy=legacy)
                               if issue[0] not in global_rules)
    return out


def check_string(text, legacy=False):
    """Return mechanical violations; weak-form membership permits a spelling,
    not its use in every context. Grammatical roles require source review.
    """
    out = []

    for rule, rx, msg in SEQUENCE_RULES:
        if legacy and rule in LEGACY_SKIP:
            continue
        for m in rx.finditer(text):
            out.append((rule, f"'{snippet(text, m.start())}' — {msg}"))

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
        for seg in re.split(r"[-–—]", tok):
            seg = seg.strip("".join(PUNCT - {" "}))
            if not seg:
                continue
            special = check_special_segment(seg, legacy)
            if special is not None:
                out.extend(special)
                continue
            if is_notation(seg):
                continue                      # formulas, units, variables (§9)
            if any(c in CAPS for c in seg):
                if "'" in seg or "’" in seg:
                    out.append(("word-apostrophe",
                                f"'{seg}' — omit apostrophes inside phonetic words"))
                mixed_match = PHONETIC_WITH_LETTER_NAMES.fullmatch(seg)
                if mixed_match:
                    prefix, letter_names = mixed_match.groups()
                    out.extend(check_string(prefix, legacy=legacy))
                    out.extend(check_string(letter_names, legacy=legacy))
                    continue
                suffix_match = LETTER_NAME_SUFFIX.fullmatch(seg)
                if suffix_match:
                    stem, suffix = suffix_match.groups()
                    final_letter = stem[-1]
                    expected = "s" if final_letter == "F" else "ɪz" if final_letter in LETTER_NAME_IZ_FINALS else "z"
                    if suffix != expected:
                        out.append(("letter-name-suffix",
                                    f"'{seg}' — final {final_letter} takes {expected}"))
                elif not all(c in CAPS for c in seg) and not DOTTED_LETTER_NAMES.fullmatch(seg):
                    out.append(("mixed-capitals",
                                f"'{seg}' — capitals only in letter-name tokens and their s / z / ɪz suffixes"))
                continue                      # USB, USBz, PDFs — letter-name segment
            out.extend(check_phonetic_component(seg, legacy))
    return out


def snippet(text, pos, width=12):
    return text[max(0, pos - width // 2): pos + width].replace("\n", " ")


IBLE_TAILS = ("ibility", "ibly", "ibles", "ible")
COMBINING_MARK = re.compile(r"[\u0300-\u036f]")


def check_ible_vowel(source_token, trans_token):
    """§7 fixes -ible as ɪbəl, so the vowel before its b is ɪ, never ə.

    The source spelling is required: -able words legitimately write əbəl and the
    transcription alone cannot tell the two endings apart.
    """
    letters = re.sub(r"[^A-Za-z]", "", source_token).lower()
    if not letters.endswith(IBLE_TAILS):
        return None
    core = token_core(trans_token)
    pos = core.rfind("b")
    if pos < 1:
        return None
    index = pos - 1
    while index > 0 and COMBINING_MARK.match(core[index]):
        index -= 1
    if core[index] != "ə":
        return None
    fixed = core[:index] + "ɪ" + core[pos:]
    return ("ible-reduced-vowel",
            f"'{core}' — source '{source_token}' ends in -ible, fixed as ɪbəl; write {fixed} (§7)")


# §4.4 spelling tie-breaker for a reduced vowel spelled e: it takes ɪ, and takes ə
# when the vowel is followed by r, l, n, m, ŋ or t (judged by adjacency in the
# transcription, since syllable boundaries are not written).  The fixed §6 and §7
# endings outrank the rule, so an e that IS the vowel of a fixed ending is skipped.
# Ruled 2026-09-27 and swept corpus-wide; pair mode is needed because only the
# source spelling says whether the reduced vowel is an e.
#
# Only the *ə* half is enforced (see E_ENFORCE_KIT).  The ə half never contradicts
# the dictionary — a reduced e before r/l/n/m/ŋ/t is a schwa in every word the
# corpus and M-W agree on (mɑ́rkət, téjbəl, prɒ́bləm, fɪ́tnəs, hə́ndrəd) — and it is
# what keeps mɑ́rkɪt / pǽkɪts from coming back.  The ɪ half does contradict M-W in
# many of those words (specific spə-, synthesis -thə-, necessarily -sə-), the author
# ruled 2026-09-27 that no clear rule can be stated from a corpus this size, and the
# words already decided are registered in the ledger, so it is reported as practice
# rather than asserted as a rule.
E_NUCLEI = ("ij", "uw", "ej", "ow", "aj", "aw", "ɔj",
            "ər", "ɜr", "ɑr", "ɔr", "ɛr", "ɪr", "ʊr",
            "ɪ", "ɛ", "æ", "ɒ", "ə", "ʊ", "ɑ", "ɔ")
E_SONORANT = set("rlnmŋt")
E_ENFORCE_KIT = False   # the ɪ half of the rule; flip to True once a rule lands
E_FIXED_END = ("ness", "less", "est", "ous", "ment", "ments", "ent", "ents",
               "ence", "ences", "ant", "ants", "ance", "ances", "er", "or", "ers",
               "ors", "al", "als", "ful", "ed", "es", "age", "ange", "ible",
               "ibles", "ibly", "ability", "able", "ables", "ably", "ic", "ics",
               "ing", "ity", "ities", "ish", "ify", "ate", "ates", "ize", "ized",
               "izes", "tion", "tions", "sion", "sions", "ture", "sure", "ly",
               "ally", "ily")
E_FIXED_PREFIX = ("be", "de", "re", "pre", "se", "e", "ex", "in", "im", "dis",
                  "mis", "en", "em", "un")
E_DERIVATION = ("s", "es", "d", "ed", "ing", "ness", "less", "ly", "al", "ally",
                "ily", "ity", "ities", "ism", "ist", "ment", "ments", "ful",
                "ous", "ate", "ates")
E_FUNCTION_SEG = {"the", "a", "an", "to", "of", "and", "or", "but", "if", "as",
                  "than", "that", "in", "on", "at", "by", "for", "from", "with",
                  "is", "are", "was", "were"}


def e_nuclei(word):
    """Nucleus symbols of a stressless phonetic token, with their start offsets."""
    out, i = [], 0
    while i < len(word):
        for nucleus in E_NUCLEI:
            if word.startswith(nucleus, i):
                out.append((nucleus, i))
                i += len(nucleus)
                break
        else:
            i += 1
    return out


def e_vowel_groups(letters):
    """Spelling-side vowel groups (a final silent e is dropped, -le excepted)."""
    groups = [(m.group(0), m.start()) for m in re.finditer(r"[aeiouy]+", letters)]
    if letters.endswith("e") and not letters.endswith("le") and len(groups) > 1 \
            and groups[-1][0] == "e":
        groups = groups[:-1]
    return groups


def e_fixed_ending(letters, pos):
    """True when the group at pos is the vowel of a fixed §6/§7 ending."""
    for ending in E_FIXED_END:
        start = pos if ending.startswith("e") else pos - 1
        if start < 0 or letters[start:start + len(ending)] != ending:
            continue
        after = letters[start + len(ending):]
        if after == "" or after in E_DERIVATION:
            return True
    return False


def base_offset(plain, accented, plain_index):
    """Index in the accented token of the base character at plain_index."""
    seen = 0
    for i, ch in enumerate(accented):
        if unicodedata.combining(ch):
            continue
        if seen == plain_index:
            return i
        seen += 1
    return None


def check_e_reduction(source_token, trans_token):
    """§4.4: a reduced e before r/l/n/m/ŋ/t is ə (adjacency).  The ɪ half is off."""
    naked = token_core(source_token).lower()
    if " " in naked:  # a phrase, not a token: nothing to align to
        return None
    segments = re.split(r"[-–—]", naked)
    if any(segment.lower() in E_FUNCTION_SEG for segment in segments):
        return None
    if any(segment.lower().startswith(E_FIXED_PREFIX)
           for segment in segments if segment):
        return None
    letters = re.sub(r"[^a-z]", "", naked)
    if len(letters) < 4 or "e" not in letters:
        return None
    core = token_core(trans_token)
    if not core:
        return None
    plain = stressless(core)
    if not plain or plain in WEAK_FORMS or is_notation(plain):
        return None
    groups = e_vowel_groups(letters)
    nuclei = e_nuclei(plain)
    if len(groups) != len(nuclei):
        return None
    for (group, gpos), (nucleus, index) in zip(groups, nuclei):
        if group != "e" or e_fixed_ending(letters, gpos):
            continue
        schwa = nucleus.startswith("ə")
        kit = nucleus == "ɪ"
        if not schwa and not kit:
            continue
        following = ("r" if schwa and nucleus[1:2] == "r"
                     else plain[index + len(nucleus): index + len(nucleus) + 1])
        if not following:
            continue
        if following in E_SONORANT:
            if kit:
                fixed = plain[:index] + "ə" + plain[index + 1:]
                return ("e-reduction",
                        f"'{core}' — source '{source_token}' has a reduced e before "
                        f"{following}; write ə ({fixed}) (§4.4)")
        elif schwa and E_ENFORCE_KIT:
            fixed = plain[:index] + "ɪ" + plain[index + 1:]
            return ("e-reduction",
                    f"'{core}' — source '{source_token}' has a reduced e not before "
                    f"r/l/n/m/ŋ/t; write ɪ ({fixed}) (§4.4)")
    return None


def layout_skeleton(token):
    """Return punctuation and symbols, excluding the omitted apostrophe class."""
    return "".join(ch for ch in token
                   if ch not in "'’" and unicodedata.category(ch)[0] in "PS")


def layout_atoms(token, forms):
    """Keep punctuation, content, and recognized words in order."""
    atoms = []
    index = 0
    while index < len(token):
        for spelling, atom in forms:
            end = index + len(spelling)
            if token.startswith(spelling, index) and word_boundaries(token, index, end):
                atoms.append(atom)
                index = end
                break
        else:
            ch = token[index]
            if ch not in "'’" and unicodedata.category(ch)[0] in "PS":
                atoms.append(("punctuation", ch))
            elif ch not in "'’" and (not atoms or atoms[-1][0] != "content"):
                atoms.append(("content", ""))
            index += 1
    return atoms


def underscore_edges(atoms):
    """Record whether each preserved underscore has content on either side."""
    remaining = sum(kind != "punctuation" for kind, _ in atoms)
    seen = False
    edges = []
    for kind, value in atoms:
        if kind != "punctuation":
            seen = True
            remaining -= 1
        elif value == "_":
            edges.append((seen, remaining > 0))
    return edges


def split_approved_token(token):
    """Split ordinary surrounding punctuation from a complete token core."""
    start = 0
    end = len(token)
    while start < end and token[start] in APPROVED_TOKEN_WRAPPERS:
        start += 1
    while end > start and token[end - 1] in APPROVED_TOKEN_WRAPPERS:
        end -= 1
    return token[:start], token[start:end], token[end:]


def punctuation_layout_matches(source_token, trans_token):
    """Match punctuation, hiding only exact approved pairs or unchanged literals."""
    if source_token == trans_token:
        return True
    if "_" not in source_token and "_" not in trans_token:
        return layout_skeleton(source_token) == layout_skeleton(trans_token)

    source_prefix, source_core, source_suffix = split_approved_token(source_token)
    trans_prefix, trans_core, trans_suffix = split_approved_token(trans_token)
    if ("_" not in source_token
            and APPROVED_SEPARATED_WORDS.get(source_core) == trans_core
            and source_prefix == trans_prefix and source_suffix == trans_suffix):
        return True

    # When literal identifier text otherwise matches, underscores must stay
    # at their original offsets after restoring the approved word spellings.
    normalized = SPECIAL_WORD_RX.sub(
        lambda m: (APPROVED_SOURCE_BY_TRANSCRIPTION[m.group()]
                   if word_boundaries(trans_token, m.start(), m.end()) else m.group()),
        trans_token)
    if (source_token.replace("_", "") == normalized.replace("_", "")
            and source_token != normalized):
        return False

    trans_forms = [(word, ("word", word)) for word in APPROVED_SEPARATED_TRANSCRIPTIONS]
    approved_spans = [(m.start(), m.end()) for m in SPECIAL_WORD_RX.finditer(trans_token)
                      if (m.group() in APPROVED_SEPARATED_TRANSCRIPTIONS
                          and word_boundaries(trans_token, m.start(), m.end()))]
    literal_forms = []
    for m in APPROVED_LOOKALIKE_SHAPE.finditer(trans_token):
        if (word_boundaries(trans_token, m.start(), m.end())
                and not any(m.start() < end and start < m.end()
                            for start, end in approved_spans)):
            literal_forms.append((m.group(), ("literal", m.group())))
    trans_forms += literal_forms
    trans_forms.sort(key=lambda pair: len(pair[0]), reverse=True)
    trans_atoms = layout_atoms(trans_token, trans_forms)
    trans_markers = {atom for atom in trans_atoms if atom[0] in {"word", "literal"}}
    # A transcription-shaped source may itself be a verbatim identifier.
    source_forms = [form for form in trans_forms if form[1] in trans_markers]
    source_forms.sort(key=lambda pair: len(pair[0]), reverse=True)
    source_atoms = layout_atoms(source_token, source_forms)
    if underscore_edges(source_atoms) != underscore_edges(trans_atoms):
        return False
    if not trans_markers:
        return layout_skeleton(source_token) == layout_skeleton(trans_token)

    source_atoms = [atom for atom in source_atoms if atom[0] != "content"]
    trans_atoms = [atom for atom in trans_atoms if atom[0] != "content"]
    return source_atoms == trans_atoms


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
        if not punctuation_layout_matches(source_token, trans_token):
            out.append(("punctuation-layout",
                        f"token {index}: source {source_layout!r}, transcription {trans_layout!r}"
                        + (" (underscore is not at an approved boundary)"
                           if source_layout == trans_layout else "")))

        ible_issue = check_ible_vowel(source_token, trans_token)
        if ible_issue:
            out.append((ible_issue[0], f"token {index}: {ible_issue[1]}"))

        e_issue = check_e_reduction(source_token, trans_token)
        if e_issue:
            out.append((e_issue[0], f"token {index}: {e_issue[1]}"))
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
    "wɒ́ts ðə núwəst dɪzájn frəm ðə 1980s ðət júwd wɛ́r dʊ́rɪŋ ə kúwl ɔ́təm íjvnɪŋ?",
    "ɪf aj həd hǽd wɔ́tər, aj wʊd həv ʃɛ́rd ɪt.",
    "aj ríjəlàjzd ðət ðǽt wəz rɔ́ŋ, túw léjt.",
    "maj fɑ́ðər júwzd ə USB drájv tə rɪkɔ́rd ðə rɪzə́lts — wɛ́r dəz ðə mə́nij kə́m frɒ́m?",
    "ðə USBz wər nɛ́kst tə ðə PDFs ənd ðə Xɪz.",
    "dɪvájd-ənd-kɒ́ŋkər rɪkɜ́rənsɪz ɒn ə T-ʃɜ́rt frəm ðə '70s",
    "mæ̀θəmǽtɪkəl əsówsijèjtɪd wɔ́l-tə-wɔ́l",
    "ðə júwnɪts, ə júwnɪfɔ̀rm tríjtmənt, ənd ə júwnɪfàjd prɒ́sɛs",
    "ðə jùwnɪvɜ́rsɪtij, jùwnɪvɜ́rsəl kəmjùwnɪkéjʃən, pjúwnɪtɪv mɛ́ʒərz",
    "pjúwpəl pjúwpəlz pjúwpɪlədʒ",
    "ájnstàjnz ɪkwéjʒən e = mc^2 rɪléjts ɛ́nərdʒij ənd mǽs.",
    "ðə fə́ŋkʃən sin(x) ɪz pɪ̀rijɒ́dɪk, ə̀nlájk log(x).",
    "ðij ǽpəl ənd ðə júwnɪt",
    "míj dúw méj nów tájm dáwn tʃɔ́js",
    "dʊ̀rəbɪ́lɪtij",
    "ɡrǽdʒuwəl",
    "ɔ́l əv ðɛm ət ɔ́l",
    "pʊ́t ɒ́n ə wɒ́tʃ",
    "aj lájnd ðɛm ə́p ɒn ðə bɔ́rd.",
    "tówkənz pər mɪ́nət ənd péj-pər-júws",
    "rɪláj ɒn ðɛm ənd pʊ́t ə́p wɪð ɪt.",
    "səm píjsɪz wər tʃɪ́pt. sə́m wər tʃɪ́pt.",
    "wɒ́t ɪz ðɪ́s? wɒ́t ə déj!",
    "téjk wɒt juw níjd. téjk wɒts lɛ́ft.",
    "ʃij də́z ðə wɜ́rk. ʃij dɪ́d ðə wɜ́rk.",
    "dəz ʃij wɜ́rk? dɪd ʃij wɜ́rk?",
    "aj də nɒ́t wɒ́nt tə prəsíjd. aj dúw wɒ́nt tə prəsíjd.",
    "áwər frɛ́ndz ɑr hǽpij. áwər frɛ́ndz ɑr wɜ́rkɪŋ.",
    "áwər frɛ́ndz ɑ́r hǽpij. jɛ́s, ðej ɑ́r.",
    "bɪ́lt-ɪ́n fɒ́low-ə́p stɛ́p-baj-stɛ́p",
    "slájd awt əv bɛ́d. wɔ́k əp ðə hɪ́l.",
    "ɪt də́z sów. ɪt də́z wɜ́rk. jɛ́s, ʃij dɪ́d.",
    "aj wə́ndər wɒ́t juw níjd. wɒ́t ə déj!",
    "sə́m əv ðɛm frəm náw ɒ́n",
    "ðej ɑr nɒ́t rɛ́dij. nɒ́t ównlij ðǽt.",
    "ðɪs bʊ́k. ðæt bʊ́k. ðijz bʊ́ks. ðowz bʊ́ks.",
    "ðɪ́s ɪz hɪ́z. ðǽt ɪz ə bʊ́k. ðíjz ɑr hɪ́z. ðówz ɑr májn.",
    "ðǽt bʊ́k, nɒ́t ðɪ́s wə́n. ðíjz bʊ́ks, nɒ́t ðówz bʊ́ks.",
    "ðɪs ówld bʊ́k. ðowz ə́ðər bʊ́ks. ðɪs–ðæt.",
    "aj nów ðət ðǽt wɜ́rks.",
    "hɪz bʊ́k. ðə bʊ́k ɪz hɪ́z.",
    "húw dɪd ɪt? míj. aj sɔ́ hɪm.",
    "ə kǽn. ə wɪ́l. mɪ́lɪtɛ̀rij májt. ə mə́st. méj.",
    "ʃij kən wɜ́rk. ʃij wɪl wɜ́rk. ʃij majt wɜ́rk. ʃij məst wɜ́rk. ʃij mej wɜ́rk.",
    "dównt kǽnt ɪ́zənt nɒ́t",
    "krìjejtɪ́vɪtij—nɒ́t ðɪ́s",
    "ðɪ́s–ðǽt",
    "ðərz ə bʊ́k ðəts ówpən. ðǽts ɪt.",
    "ðə U.S. ənd ðə U.K.",
    "ówpənAI ówpənAIz ðij ówpənAI tɛ́st",
    "O_ɔ́θ",
    "dʒɛ́n_AI_ɒ̀ps",
    "V_nɛ́t",
    "Q_rɛ́lz",
    "Odéjtə",
    "(O_ɔ́θ), dʒɛ́n_AI_ɒ̀ps; V_nɛ́t Q_rɛ́lz Odéjtə",
    "O_ɔ́θ, V_nɛ́t",
    "O_ɔ́θ dʒɛ́n_AI_ɒ̀ps",
    "O_ɔ́θ source_identifier",
    "dʒɛ́n_AI_ɒ̀ps 2",
    "π_AI_ω_2",
    "sɪmǽntɪk sɪmǽntɪkəlij",
    "mɑ̀trijɒ́ʃkə ǽlɡərɪ̀ðəm",
    "ə prówɡræ̀m kɔ́ld fingerd",
    "béjsɪs dɪbéjt rɪléjʃənʃɪ̀p ɪ̀nəvéjʃənz",
    "ɪɡzǽmpəl rìjɪvæ̀ljuwéjʃən lájklijhʊ̀d sə́tʃ æz nów",
    "háj-stéjks ríj-ɪstǽblɪʃ (E.G., mɪ́sɪz. fɛ́ldmən)",
]]
INVALID_SAMPLES = [(D(s), r) for s, r in [
    ("wɛ́ər", "centering-schwa"),
    ("bʌt", "banned-vowels"),
    ("kwɑ́ntᵻtij", "banned-vowels"),
    ("ðə gɑ́rmənt", "ascii-g"),
    ("ɔl əv ðɛm", "unaccented-token"),
    ("nɒt rɛ́dij", "unaccented-token"),
    ("awər frɛ́ndz ɑr hǽpij", "unaccented-token"),
    ("ðɪ́s—nɒt", "unaccented-token"),
    ("ðɪs–nɒt", "unaccented-token"),
    ("U..S.", "mixed-capitals"),
    ("U.s.", "mixed-capitals"),
    ("OpenAI", "mixed-capitals"),
    ("Oméjd", "mixed-capitals"),
    ("Odéjtəz", "mixed-capitals"),
    ("O__ɔ́θ", "mixed-capitals"),
    ("O_déjtə", "unapproved-separated-word"),
    ("O_ɔθ", "unaccented-token"),
    ("V_nɛt", "unaccented-token"),
    ("Q_rɛlz", "unaccented-token"),
    ("dʒɛn_AI_ɒ̀ps", "unaccented-token"),
    ("dʒɛ́n_AI_ɒ́ps", "multiple-acutes"),
    ("dʒɛ́n_AI_ɒps", "unapproved-separated-word"),
    ("O_ɒ́θ", "unapproved-separated-word"),
    ("Z_nɛ́t", "unapproved-separated-word"),
    ("dʒɛ́n_XY_ɒ̀ps", "unapproved-separated-word"),
    ("gɛ́n_AI_ɒ̀ps", "ascii-g"),
    ("dʒɛ́n_AI_gɒ̀ps", "ascii-g"),
    ("dʒɛ́n_AI_gɒ̀ps_2", "ascii-g"),
    ("dʒɛn_AI_ɒ̀ps_2", "unaccented-token"),
    ("V_nɛt_2", "unaccented-token"),
    ("dʒɛ́n_AI_ɒ̀px", "illegal-char"),
    ("dʒɛ́n_AI_ɒ̀po", "invalid-glide-vowel"),
    ("O_ɛ́j", "epsilon-glide"),
    ("O_e\u0301j", "encoding-decomposed"),
    ("O_ɔ́ɹ", "banned-allophones"),
    ("O_ɔ́θ_V_nɛt", "unaccented-token"),
    ("dʒɛ́n_AI_ɒ̀ps_pjúwpɪl", "pupil-vowel"),
    ("owpənAI", "unaccented-token"),
    ("ópənAI", "invalid-glide-vowel"),
    ("gówAI", "ascii-g"),
    ("ówpə́nAI", "multiple-acutes"),
    ("ówpənAIs", "letter-name-suffix"),
    ("ðə ówpənAI", "the-context"),
    ("ˈleðər", "stress-marks"),
    ("wɜːld", "length-mark"),
    ("meɪd", "traditional-diphthong"),
    ("Méjd", "mixed-capitals"),
    ("USBs", "letter-name-suffix"),
    ("fʊtwɛr ɪz", "unaccented-token"),
    ("ɹɪ́lij", "banned-allophones"),
    ("kɒ́ŋkə́r", "multiple-acutes"),
    ("ðə leather dʒǽkət", "unaccented-token"),
    ("ðə ǽpəl", "the-context"),
    ("ðij júwnɪt", "the-context"),
    ("bɛ́jsɪs dɪbɛ́jt", "epsilon-glide"),
    ("rɪlɛ́jʃənʃɪp ɛ́j ɛ̀j", "epsilon-glide"),
    ("júwnəts", "reduced-i-spelling"),
    ("ə júwnəfɔ̀rm prɒ́sɛs", "reduced-i-spelling"),
    ("pówst-júwnəts", "reduced-i-spelling"),
    ("pjúwnətɪv", "reduced-i-spelling"),
    ("kəmjúwnəkèjt", "reduced-i-spelling"),
    ("jùwnəvɜ́rsətij", "reduced-i-spelling"),
    ("pjúwpɪl", "pupil-vowel"),
    ("(pjúwpɪlz,)", "pupil-vowel"),
    ("pówst-pjúwpɪl", "pupil-vowel"),
    ("ɪt's", "word-apostrophe"),
    ("wɛ́rər’z", "word-apostrophe"),
    ("mí dú mé", "invalid-glide-vowel"),
    ("méɪd óʊn áɪ áʊ ɔ́ɪ", "traditional-diphthong"),
    ("flɛ́ksəbəl", "ible-reduced-vowel"),
    ("rɪspɒ́nsəbəl", "ible-reduced-vowel"),
    ("vɪ̀zəbɪ́lɪtij", "ible-reduced-vowel"),
    ("æ̀ksɛsəbɪ́lɪtij", "ible-reduced-vowel"),
]]

VALID_LAYOUT_SAMPLES = [
    ("OAuth", "O_ɔ́θ"),
    ("GenAIOps", "dʒɛ́n_AI_ɒ̀ps"),
    ("VNet", "V_nɛ́t"),
    ("qrels", "Q_rɛ́lz"),
    ("OData", "Odéjtə"),
    ("(OAuth), (qrels)", "(O_ɔ́θ), (Q_rɛ́lz)"),
    ("'OAuth', \"VNet.\"", "'O_ɔ́θ', \"V_nɛ́t.\""),
    ("[GenAIOps]", "[dʒɛ́n_AI_ɒ̀ps]"),
    ("VNet_name", "VNet_name"),
    ("OAuth_key", "OAuth_key"),
    ("GenAIOps_mode", "GenAIOps_mode"),
    ("my_VNet", "my_VNet"),
    ("qrels_format", "qrels_format"),
    ("OData_foo_bar", "OData_foo_bar"),
    ("source_identifier", "source_identifier"),
    ("O_other", "O_other"),
    ("O_ɔ́θ", "O_ɔ́θ"),
    ("semantic", "sɪmǽntɪk"),
    ("semantically", "sɪmǽntɪkəlij"),
    ("Matryoshka algorithm", "mɑ̀trijɒ́ʃkə ǽlɡərɪ̀ðəm"),
    ("OpenAI's fingerd test", "ówpənAIz fingerd tɛ́st"),
    ("U.S. (e.g., Mrs. Feldman)", "U.S. (E.G., mɪ́sɪz. fɛ́ldmən)"),
    ("re-establish high-stakes", "ríj-ɪstǽblɪʃ háj-stéjks"),
    ("What's wrong?", "wɒ́ts rɔ́ŋ?"),
    ("O'Connor left.", "owkɒ́nər lɛ́ft."),
    ("T-shirt '70s", "T-ʃɜ́rt '70s"),
    ("USB's", "USBz"),
    ("pupil's pupils", "pjúwpəlz pjúwpəlz"),
    ("flexible", "flɛ́ksɪbəl"),
    ("visible and responsible", "vɪ́zɪbəl ənd rɪspɒ́nsɪbəl"),
    ("possibility", "pɒ̀sɪbɪ́lɪtij"),
    ("responsibility", "rɪspɒ̀nsɪbɪ́lɪtij"),
    ("market", "mɑ́rkət"),
    ("targets", "tɑ́rɡəts"),
    ("ticket", "tɪ́kət"),
    ("packets", "pǽkəts"),
    ("rocket", "rɒ́kət"),
    ("benefits", "bɛ́nɪfɪts"),
    # the ɪ half of the rule is practice, not a check: both shapes are accepted
    ("specific", "spɪsɪ́fɪk"),
    ("knowledge", "nɒ́lɪdʒ"),
    ("phenomena", "fənɒ́mənə"),
    ("(deterministic", "(dɪtɜ̀rmɪnɪ́stɪk"),
    ("knowledge", "nɒ́lɪdʒ"),
    ("strategies", "strǽtɪdʒijz"),
    ("open", "ówpən"),
    ("problem", "prɒ́bləm"),
    ("model", "mɒ́dəl"),
    ("fitness", "fɪ́tnəs"),
    ("irrelevant", "ɪrɛ́lɪvənt"),
    ("generic", "dʒɛ́nərɪk"),
]

INVALID_LAYOUT_SAMPLES = [
    ("Other", "O_ɔ́θ", {"punctuation-layout"}),
    ("Oauth", "O_ɔ́θ", {"punctuation-layout"}),
    ("OAuth", "O_ɒ́θ", {"punctuation-layout"}),
    ("OAuth", "O__ɔ́θ", {"punctuation-layout"}),
    ("OData", "O_déjtə", {"punctuation-layout"}),
    ("GenAIOps", "dʒɛ́n_AI_ɒps", {"punctuation-layout"}),
    ("qrels", "Q__rɛ́lz", {"punctuation-layout"}),
    ("VNet_name", "V_nɛ́t_name", {"punctuation-layout"}),
    ("OAuth_key", "O_ɔ́θ_key", {"punctuation-layout"}),
    ("GenAIOps_mode", "dʒɛ́n_AI_ɒ̀ps_mode", {"punctuation-layout"}),
    ("my_VNet", "my_V_nɛ́t", {"punctuation-layout"}),
    ("qrels_format", "Q_rɛ́lz_format", {"punctuation-layout"}),
    ("prefix/OAuth", "prefix/O_ɔ́θ", {"punctuation-layout"}),
    ("OAuth/key", "O_ɔ́θ/key", {"punctuation-layout"}),
    ("VNet.name", "V_nɛ́t.name", {"punctuation-layout"}),
    ("my-VNet", "my-V_nɛ́t", {"punctuation-layout"}),
    ("qrels-format", "Q_rɛ́lz-format", {"punctuation-layout"}),
    ("GenAIOps:mode", "dʒɛ́n_AI_ɒ̀ps:mode", {"punctuation-layout"}),
    ("_OAuth", "_O_ɔ́θ", {"punctuation-layout"}),
    ("OAuth_", "O_ɔ́θ_", {"punctuation-layout"}),
    ("_VNet_", "_V_nɛ́t_", {"punctuation-layout"}),
    ("_qrels", "_Q_rɛ́lz", {"punctuation-layout"}),
    ("(GenAIOps_)", "(dʒɛ́n_AI_ɒ̀ps_)", {"punctuation-layout"}),
    ("/OAuth", "/O_ɔ́θ", {"punctuation-layout"}),
    (r"\\VNet", r"\\V_nɛ́t", {"punctuation-layout"}),
    ("OAuth/VNet", "O_ɔ́θ/V_nɛ́t", {"punctuation-layout"}),
    ("OAuth-VNet", "O_ɔ́θ-V_nɛ́t", {"punctuation-layout"}),
    ("OAuth_VNet", "O_ɔ́θ_V_nɛ́t", {"punctuation-layout"}),
    ("OAuth_foo", "O_ɔ́θ_fúw", {"punctuation-layout"}),
    ("OAuth_O_id", "O_ɔ́θ_O_id", {"punctuation-layout"}),
    ("OAuth_foo_bar", "O_ɔ́θ_foo_bar", {"punctuation-layout"}),
    ("foo_OAuth_", "foo_O_ɔ́θ_", {"punctuation-layout"}),
    ("OAuth_OAuth", "OAuth_O_ɔ́θ", {"punctuation-layout"}),
    ("OAuth", "O_ɔ́θ_", {"punctuation-layout"}),
    ("OAuth_", "O_ɔ́θ", {"punctuation-layout"}),
    ("OAuth_foo", "O_ɔ́θfoo", {"punctuation-layout"}),
    ("OAuth_foo_bar", "O_ɔ́θ_fo_obar", {"punctuation-layout"}),
    ("OData_foo_bar", "Odéjtə_fo_obar", {"punctuation-layout"}),
    ("Other_", "O_ɔθ", {"punctuation-layout"}),
    ("source_identifier", "sourceidentifier", {"punctuation-layout"}),
    ("source_identifier", "source__identifier", {"punctuation-layout"}),
    ("source_identifier", "sourceidentifier_", {"punctuation-layout"}),
    ("foo_bar_baz", "foo_ba_rbaz", {"punctuation-layout"}),
    ("OAuth_VNet", "V_nɛ́t_O_ɔ́θ", {"punctuation-layout"}),
    ("OAuth-VNet", "O_ɔ́θ/V_nɛ́t", {"punctuation-layout"}),
    ("OAuth,", "O_ɔ́θ;", {"punctuation-layout"}),
    ("OAuth2", "O_ɔ́θ2", {"punctuation-layout"}),
    ("OAuth2", "O_ɔ́θ3", {"digits-changed", "punctuation-layout"}),
    ("OAuth", "O_ɔ́θ ", {"whitespace-layout"}),
    ("re-establish", "rìjɪstǽblɪʃ", {"punctuation-layout"}),
    ("Mrs. Feldman", "mɪ́sɪz fɛ́ldmən", {"punctuation-layout"}),
    ("Hello,  world!", "həlów wɜ́rld.", {"whitespace-layout", "punctuation-layout"}),
    ("Use 1980s.", "júwz 1970s.", {"digits-changed"}),
    ("one two", "wə́n", {"whitespace-layout", "token-count"}),
    (" one", "wə́n ", {"whitespace-layout"}),
    ("flexible", "flɛ́ksəbəl", {"ible-reduced-vowel"}),
    ("responsible", "rɪspɒ́nsəbəl", {"ible-reduced-vowel"}),
    ("responsibility", "rɪspɒ̀nsəbɪ́lɪtij", {"ible-reduced-vowel"}),
    ("visible", "vɪ́zəbəl", {"ible-reduced-vowel"}),
    ("market", "mɑ́rkɪt", {"e-reduction"}),
    ("packets", "pǽkɪts", {"e-reduction"}),
    ("rocket", "rɒ́kɪt", {"e-reduction"}),
]

VALID_JSON_SAMPLES = [
    [{"Question": "OAuth, GenAIOps, VNet, qrels, OData.",
      "trans_Question": "O_ɔ́θ, dʒɛ́n_AI_ɒ̀ps, V_nɛ́t, Q_rɛ́lz, Odéjtə."}],
    [{"Question": "OAuth and source_identifier",
      "trans_Question": "O_ɔ́θ ənd source_identifier"}],
    [{"Question": "VNet_name", "trans_Question": "VNet_name"}],
    [{"Question": "semantic and semantically",
      "trans_Question": "sɪmǽntɪk ənd sɪmǽntɪkəlij"}],
    [{"Question": "What's wrong?", "trans_Question": "wɒ́ts rɔ́ŋ?",
      "WrongAnswers": ["O'Connor left."], "trans_WrongAnswers": ["owkɒ́nər lɛ́ft."]}],
    [{"Question": "A pupil's pupils.", "trans_Question": "ə pjúwpəlz pjúwpəlz."}],
    [{"Question": "Tokens per minute and pay-per-use.",
      "trans_Question": "tówkənz pər mɪ́nət ənd péj-pər-júws."}],
        [{"Question": "This book. That book. These books. Those books.",
            "trans_Question": "ðɪs bʊ́k. ðæt bʊ́k. ðijz bʊ́ks. ðowz bʊ́ks."}],
        [{"Question": "That is a book. I know that that works. That's it.",
            "trans_Question": D("ðǽt ɪz ə bʊ́k. aj nów ðət ðǽt wɜ́rks. ðǽts ɪt.")}],
]

INVALID_JSON_SAMPLES = [
    ([{"Question": "VNet_name", "trans_Question": "V_nɛ́t_name"}],
     {"punctuation-layout"}),
    ([{"Question": "OAuth/key", "trans_Question": "O_ɔ́θ/key"}],
     {"punctuation-layout"}),
    ([{"Question": "OAuth", "trans_Question": "O_ɔθ"}],
     {"unaccented-token", "punctuation-layout"}),
    ([{"Question": "GenAIOps", "trans_Question": "dʒɛ́n_AI_gɒ̀ps"}],
     {"ascii-g", "punctuation-layout"}),
    ([{"Question": "Other", "trans_Question": "O_ɔ́θ"}], {"punctuation-layout"}),
    ([{"Question": "OAuth_foo", "trans_Question": "O_ɔ́θfoo"}],
     {"unapproved-separated-word", "punctuation-layout"}),
    ([{"Question": "OData", "trans_Question": "Oméjd"}], {"mixed-capitals"}),
    ([{"Question": "market", "trans_Question": "mɑ́rkɪt"}], {"e-reduction"}),
    ([{"Question": "All of them.", "trans_Question": "ɔl əv ðɛm."}], {"unaccented-token"}),
    ([{"Question": "Pupil.", "trans_Question": "pjúwpɪl."}], {"pupil-vowel"}),
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
