---
name: check-word-transcription
description: Audit requested word(s) against their transcriptions in the example corpus and correction ledger. Report findings before making any changes.
---

# Check word transcription

When the user asks to check or audit how one or more words are transcribed:

1. Find every occurrence of each requested word in the corpus: source/transcription pairs (`TXT_*` and matching `TRN_*` files) under `examples/`, and entries in `transcription-corrections.json`. Search without regard to capitalization, but match whole words and relevant hyphenated forms rather than unrelated substrings. Preserve enough surrounding context to identify the word's grammatical role and pronunciation.
2. For each matching source occurrence, inspect the corresponding position in its paired transcription. Report the file and a short context when useful. If a source file has no matching transcription file, or token alignment makes the corresponding transcription uncertain, state that explicitly instead of guessing.
3. Read `transcription_guide.md` and `design_choices.md` as needed to evaluate each form. Check `transcription-corrections.json` for applicable prior corrections and their explanations; consider whether the recorded context matches the occurrence.
4. Before making any edits, report briefly for each word: the transcriptions found, whether each is correct, and the specific guide rule or design choice violated by any incorrect form. End with one clear recommendation. If no occurrence is found, say so.
5. Stop after the report and wait for the user's explicit confirmation before changing any files. Do not interpret the request to check or audit as permission to edit.
6. After confirmation, make only the agreed corrections in the affected transcription file(s) and, if appropriate and agreed, the correction ledger. Preserve source/transcription alignment and existing formatting. For every changed transcription, run `validate_transcriptions.py --text "<transcription>"` on the corrected transcription text; also run the validator on any other supported input it applies to. Review the output and fix any newly introduced violations before finishing. Report exactly which files changed and the validation results.
