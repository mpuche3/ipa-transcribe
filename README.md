# ipa-transcribe

A complete, self-contained system for transcribing English text into learner-friendly IPA — General American, Lindsey-style glide vowels, Spanish-style stress accents — plus an automatic validator. Written so that any LLM (or human) following the guide produces byte-identical output for the same input.

> What's the newest design from the 1980s that you'd wear during a cool autumn evening?

> `wɒts ðə núwəst dɪzájn frəm ðə 1980s ðət júwd wɛ́r dʊ́rɪŋ ə kúwl ɔ́təm íjvnɪŋ?`

## What's inside

| File | Role |
|---|---|
| `transcription_guide.md` | The full spec — symbol charts, stress rules, weak forms, heteronyms, worked examples, machine-checkable constraints |
| `SKILL.md` | Claude Code skill entry point (workflow and invariants) |
| `validate_transcriptions.py` | Zero-dependency Python checker for transcriptions |
| `design_choices.md` | Why the notation looks the way it does — each decision and its valid alternatives |

## Install as a Claude Code skill

Windows:

```
git clone https://github.com/mpuche3/ipa-transcribe "%USERPROFILE%\.claude\skills\ipa-transcribe"
```

macOS / Linux:

```
git clone https://github.com/mpuche3/ipa-transcribe ~/.claude/skills/ipa-transcribe
```

Restart Claude Code, then ask it to transcribe any English text (or invoke `/ipa-transcribe`). The skill reads the guide, transcribes, and validates its own output with the bundled checker. Update later with a plain `git pull`.

## Use without Claude

The guide is a standalone spec: paste `transcription_guide.md` into any LLM as the instructions for a transcription task, or read it yourself — it is written to be followed by humans too.

Validate output with plain Python (no dependencies):

```
python validate_transcriptions.py --text "ðə flɔ́r lǽmp ɪz tɔ́l."    # one string
python validate_transcriptions.py path/to/questions                 # JSON batches + source-layout checks
python validate_transcriptions.py --self-test                       # sanity check (expect 42/42)
```

## The style at a glance

| Decision | Choice |
|---|---|
| Reference accent | General American — when varieties disagree, Merriam-Webster's first pronunciation wins |
| Long vowels / diphthongs | glide notation `ij uw ej ow aj aw ɔj` plus long `ɑ` — never `iː eɪ oʊ` |
| Stress | acute = primary, grave = secondary, on the vowel itself: `dʒǽkət`, `mæ̀θəmǽtɪkəl` — never `ˈ ˌ` |
| STRUT | `ə` even when stressed (`kə́lər`, `lə́v`) — `ʌ` is never used |
| SQUARE / NEAR | plain `ɛr` / `ɪr` (`wɛ́r`, `nɪ́r`) — no centering schwa |
| Yod | American yod-dropping: `núw`, `stúwdənt` — but `mjúwzɪk`, `hjúwmən` |
| Function words | weak forms, unaccented: `əv ənd tə ðə / ðij həz wɒt` — *the* follows the next sound; strong forms at clause ends |
| Apostrophes | omitted inside phonetic words: *it's* `ɪts`, *they've* `ðéjv`; preserved in pass-through tokens such as `'70s` |
| Digits, letter names, notation | pass through as written: `1970s`, `USB`, `e = mc^2`, `sin(x)` |

Three distinctions are kept in writing that readers may merge in their own speech: `ɒ` vs `ɑ` (GA merges them), `ǽr` in *carry/marry* (most GA speakers say `ɛr`), and flapping is never written.

## Encoding note

Accents on IPA letters are combining marks (U+0301 acute, U+0300 grave). Some editors and toolchains silently NFC-normalize `æ` + U+0301 into the single character `ǽ` (U+01FD), which the validator flags as `precomposed-ae`. Repair a file with:

```
python -c "import pathlib,sys; p=pathlib.Path(sys.argv[1]); p.write_text(p.read_text(encoding='utf-8').replace(chr(0x1FD), chr(0xE6)+chr(0x301)), encoding='utf-8')" FILE
```

## License

MIT — see [LICENSE](LICENSE).
