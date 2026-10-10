---
name: write-and-transcribe-essay
description: Write an essay on the supplied topic and save it with its IPA transcription. Use when the user asks to write and transcribe an essay.
---

Write a clear, factual essay about the topic the user provides. If no topic is supplied, ask for it before writing.

Always begin with a short, plain-text title on its own first line. Use paragraphs for the body: no subtitles, bullets, or numbered lists. Put each paragraph on one line immediately after the preceding line. Do not include any empty or whitespace-only lines, including between the title and body or between paragraphs.

Save the essay as `examples/TXT_<TopicName>.txt`, then create the matching `examples/TRN_<TopicName>.txt`. Transcribe the title too, keeping it on the first line of the TRN file. Both files must have identical line structure and no blank lines. These output paths are relative to the repository root, not this skill directory.

Before transcribing, read [the transcription guide](../../../transcription_guide.md) and [the correction ledger](../../../transcription-corrections.json); follow them and validate the transcription with [the validator](../../../validate_transcriptions.py). Check that both files start with the short title (source and transcription respectively), have matching lines, and contain no empty or whitespace-only lines. Continue until both files are complete and validation passes.
