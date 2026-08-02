---
name: ipa-transcribe
description: Transcribe English text into learner-friendly IPA using Lindsey-style glide vowels (ij uw ej ow aj aw ɔj) and acute/grave stress accents on the vowel. Use when the user asks to transcribe, phonetically annotate, or add IPA pronunciations to English text in this style.
---

# English → IPA transcription (glide-vowel style)

## Workflow

1. **Read `transcription_guide.md` in this skill directory in full before transcribing anything.** It is the complete, self-contained spec: symbol chart, vowel/consonant tables, stress rules, weak forms, heteronyms, formatting and encoding rules, worked examples, and a step-by-step procedure (§11).

2. **Transcribe** following the guide's §11 procedure. Non-negotiable invariants:
   - All lowercase; the only capitals are letter-name tokens (`USB`, `T-ʃɜ́rt`).
   - Exactly one acute per content word — even monosyllables (`méjd`, `wɜ́rk`); §6 weak-form function words carry no accent at all (`əv`, `ənd`, `tə`, `wɒt`).
   - Banned everywhere: `ʌ`, `ᵻ`, `ˈ ˌ ː`, `ɹ`, ASCII `g`, and the sequences `ɛər / ɪər / ʊər`.
   - Digits, punctuation, apostrophes, and notation (equations, formulas, units: `e = mc^2`, `sin(x)`, `km/h`) pass through unchanged; output aligns 1:1 with the source tokens.

3. **Validate** every transcription with the bundled checker (run from this skill's directory, or reference the script by absolute path):

   ```
   python validate_transcriptions.py --text "<transcription>"
   ```

   Fix each reported violation and re-run until it reports 0. For JSON files whose items pair source fields with `trans_*` fields, pass file or directory paths instead — that mode also checks source/transcription token parity. Run `--self-test` once to confirm the environment (expect `19/19 passed`).

4. **Encoding trap:** many toolchains silently NFC-normalize `æ` + combining acute (U+0301) into the single precomposed character U+01FD, which this style forbids — the validator reports it as `precomposed-ae`. If that fires on a file you wrote, repair it:

   ```
   python -c "import pathlib,sys; p=pathlib.Path(sys.argv[1]); p.write_text(p.read_text(encoding='utf-8').replace(chr(0x1FD), chr(0xE6)+chr(0x301)), encoding='utf-8')" <file>
   ```

## Notes

- The style is rhotic (r pronounced everywhere) with glide-notation long vowels; stress is marked by acute (primary) and grave (secondary) accents on the vowel itself — never with `ˈ ˌ`.
- **General American is the reference accent**: wherever English varieties disagree (stress, vowels, yod, silent letters — *either*, *schedule*, *herb*), follow the GA pronunciation, per the guide's §1 table. American yod-dropping applies: `núw`, `stúwdənt`, but `mjúwzɪk`, `hjúwmən`.
- The judgment calls that most often go wrong are all covered in the guide — check there before guessing: heteronyms like *record*/*use* (§8), auxiliary vs. main verb (*had had*) and conjunction vs. demonstrative (*that that*) (§12, examples 4–5), clause-final strong forms (*looking ǽt?*) (§6), and the LOT `ɒ` / PALM `ɑ` / THOUGHT `ɔ` split (§4.1).
- When batch-producing transcriptions, validate the whole output file at the end rather than trusting spot checks.
