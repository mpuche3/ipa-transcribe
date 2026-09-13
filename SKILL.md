---
name: ipa-transcribe
description: Transcribe English text into learner-friendly IPA using Lindsey-style glide vowels (ij uw ej ow aj aw ɔj) and acute/grave stress accents on the vowel. Use when the user asks to transcribe, phonetically annotate, or add IPA pronunciations to English text in this style.
---

# English → IPA transcription (glide-vowel style)

## Workflow

1. **Read `transcription_guide.md` in this skill directory in full before transcribing anything.** It is the complete, self-contained spec: symbol chart, vowel/consonant tables, stress rules, weak forms, heteronyms, formatting and encoding rules, worked examples, and a step-by-step procedure (§11).

2. **Transcribe** following the guide's §11 procedure. Non-negotiable invariants:
   - All lowercase; the only capitals are letter-name tokens (`USB`, `T-ʃɜ́rt`). Their pronounced plural or possessive endings attach in lowercase phonetic form, selected from the last letter name's final sound (`USBz`, `PDFs`, `Xɪz`).
   - Exactly one acute per unhyphenated content word — even monosyllables (`méjd`, `wɜ́rk`); apply the rule separately to each element of a hyphenated compound. *All* is always `ɔ́l`, *not* is always `nɒ́t`, and demonstratives are accented in both determiner and independent uses (`ðɪ́s`, `ðǽt`, `ðíjz`, `ðówz`); conjunction/relative *that* stays `ðət`. Verbal particles are accented (`ə́p`, `dáwn`, `áwt`, `ɒ́n`), but prepositions stay weak by default. Select §6 forms by grammatical role: weak monosyllables are bare (`əv`, `ənd`, `tə`), while polysyllabic function words retain internal stress. Independent/contrastive *some* is `sə́m`, indefinite determiner *some* is `səm`; interrogative/exclamative *what* is `wɒ́t` (also in embedded questions), fused-relative *what* is `wɒt`; contractions inherit the distinction (`wɒ́ts` / `wɒts`). Lexical *does / did* are `də́z / dɪ́d`, auxiliaries weak by default; *do* remains always accented. Possessive *our* and both copular and auxiliary *be* remain weak by default, except for explicit contrast or applicable clause-final strong forms. A full vowel does not imply an acute, and an acute does not necessarily indicate sentence focus. Weak *the* is `ðə` before a consonant sound and `ðij` before a vowel sound; both are unaccented.
   - Independent possessives are accented: determiner *his* is `hɪz`, independent *his* is `hɪ́z`. Personal pronouns used as independent answers or explicitly focused take strong accented forms; sentence-final position alone does not trigger an accent (*I saw him* keeps weak *him*). The modal table applies only to modal uses, not lexical *can / will / might / must* or the month/name *May*. Use their full accented content-word forms (§6). Negative contractions remain unchanged; match whole words when updating *not* or demonstratives.
   - Banned everywhere: `ʌ`, `ᵻ`, `ˈ ˌ ː`, `ɹ`, ASCII `g`, and the sequences `ɛər / ɪər / ʊər`.
   - Classify ambiguous tokens from context before transcribing: spoken English and pronounced acronyms become phonetic; equations, formulas, code, identifiers, units, and other symbolic material pass through unchanged. Token shape alone is not decisive (`NASA` may be `nǽsə` or an identifier; *sine* is `sájn`, while `sin(x)` is preserved). Output aligns 1:1 with the source tokens. Omit word-internal apostrophes from phonetic words (`ɪts`, `ðéjv`, `dównt`), but preserve them in quotation punctuation and pass-through tokens (`'70s`).

3. **Validate** every transcription with the bundled checker (run from this skill's directory, or reference the script by absolute path):

   ```
   python validate_transcriptions.py --text "<transcription>"
   ```

   Fix each applicable violation and re-run; normally the result should be 0. For JSON files whose items pair source fields with `trans_*` fields, pass file or directory paths instead — that mode also requires complete source/transcription pairs and checks token count, exact whitespace, punctuation/symbol layout, and digits. Grammatical-role and notation classification remain semantic judgments: re-check context-dependent weak/accented forms against the source even when validation passes. If the only remaining issue is a generic capitalization or character warning on a token clearly established by context as verbatim code or notation, keep the token unchanged and report the validator limitation rather than phoneticizing it to silence the warning. Run `--self-test` once to confirm the environment (expect all cases to pass).

4. **Encoding trap:** many toolchains silently NFC-normalize `æ` + combining acute (U+0301) into the single precomposed character U+01FD, which this style forbids — the validator reports it as `precomposed-ae`. If that fires on a file you wrote, repair it:

   ```
   python -c "import pathlib,sys; p=pathlib.Path(sys.argv[1]); p.write_text(p.read_text(encoding='utf-8').replace(chr(0x1FD), chr(0xE6)+chr(0x301)), encoding='utf-8')" <file>
   ```

## Notes

- The style is rhotic (r pronounced everywhere) with glide-notation long vowels; stress is marked by acute (primary) and grave (secondary) accents on the vowel itself — never with `ˈ ˌ`.
- **General American is the reference accent**: wherever English varieties disagree (stress, vowels, yod, silent letters — *either*, *schedule*, *herb*), follow the GA pronunciation, per the guide's §1 table. American yod-dropping applies: `núw`, `stúwdənt`, but `mjúwzɪk`, `hjúwmən`.
- Before mapping dictionary pronunciations, apply the guide's intervocalic TRAP override: when lexical TRAP /æ/ precedes an `r` followed by another vowel, write `ǽr` even if merged GA suggests `ɛ́r`. In particular, *paramount* is `pǽrəmàwnt`, not `pɛ́rəmàwnt` (§4.3).
- The judgment calls that most often go wrong are all covered in the guide — check there before guessing: heteronyms like *record*/*use* (§8), auxiliary vs. main verb (*had had*) and conjunction vs. demonstrative (*that that*) (§12, examples 4–5), particles vs. prepositions and the roles of *some*, *what*, and *does / did* (§6; §12, examples 7–8), independent possessives, pronoun answers, and lexical homonyms of modals (§12, examples 9–11), clause-final strong forms (*looking ǽt?*) (§6), and the LOT `ɒ` / PALM `ɑ` / THOUGHT `ɔ` split (§4.1), and the weak `ɪ`~`ə` tie-breaker — fixed morphemes first (reduced prefixes *be-, de-, re-, pre-, se-, e-/ex-* and endings *-ed/-es/-age/-ange* → `ɪ`: `bɪkɒ́z`, `dɪzájn`, `lǽŋɡwɪdʒ`), then spelling: i/y → `ɪ`, any other letter → `ə` (`prɒ́fɪt` vs `mɑ́rkət`) (§4.4).
- When batch-producing transcriptions, validate the whole output file at the end rather than trusting spot checks.
