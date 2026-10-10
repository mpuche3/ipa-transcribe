---
name: check-word-transcription-2
description: Audit how given word(s) are transcribed across the repo corpus and report before changing anything.
disable-model-invocation: true
---
Check these word(s): `$ARGUMENTS`

Find every occurrence of the word(s) in the repo corpus — the `TXT_*` / `TRN_*` pairs in `examples/`, plus `transcription-corrections.json`. For each hit, compare the transcription against `transcription_guide.md` (and `design_choices.md` where relevant).

Report first, edit nothing: give a very brief analysis per word — the transcriptions found, whether each is correct, and the specific rule broken if not — then one clear recommendation. Apply changes only after I confirm, and re-run `validate_transcriptions.py` on any file you touch.
