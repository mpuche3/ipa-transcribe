# ipa-transcribe

A complete, self-contained system for transcribing English text into learner-friendly IPA — General American, Lindsey-style glide vowels, Spanish-style stress accents — plus an automatic validator. Written so that any LLM (or human) following the guide produces byte-identical output for the same input.

> What's the newest design from the 1980s that you'd wear during a cool autumn evening?

> `wɒ́ts ðə núwəst dɪzájn frəm ðə 1980s ðət júwd wɛ́r dʊ́rɪŋ ə kúwl ɔ́təm íjvnɪŋ?`

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
python validate_transcriptions.py --self-test                       # sanity check (all cases must pass)
```

## The style at a glance

| Decision | Choice |
|---|---|
| Reference accent | General American — when varieties disagree, Merriam-Webster's first pronunciation wins |
| Long monophthongs (no glide) | `ɑ` PALM and `ɔ` THOUGHT + CLOTH, without length marks |
| Glide vowels | `ij uw ej ow aj aw ɔj` — never `iː eɪ oʊ` |
| Stress | acute = primary, grave = secondary, on the vowel itself: `dʒǽkət`, `mæ̀θəmǽtɪkəl` — never `ˈ ˌ` |
| STRUT | `ə` even when stressed (`kə́lər`, `lə́v`) — `ʌ` is never used |
| SQUARE / NEAR | plain `ɛr` / `ɪr` (`wɛ́r`, `nɪ́r`) — no centering schwa |
| Yod | American yod-dropping: `núw`, `stúwdənt` — but `mjúwzɪk`, `hjúwmən` |
| Function words | choose by grammatical role; weak monosyllables are bare (`əv ənd tə ðə / ðij həz`), polysyllables retain internal stress; *the* follows the next sound; explicit contrast and applicable clause-final forms are strong |
| Accent conventions | *all*, *not*, verbal particles, and *do* are accented; demonstratives are bare as neutral determiners, accented when independent or explicitly contrastive |
| Role-dependent stress | distinguish *some pieces* / independent *some*, determiner / independent *his*, interrogative/exclamative / fused-relative *what*, and lexical / auxiliary or modal uses; independent pronoun answers take strong accented forms |
| Apostrophes | omitted inside phonetic words: *it's* `ɪts`, *they've* `ðéjv`; preserved in pass-through tokens such as `'70s` |
| Digits, letter names, notation | classify from context; letter names stay capitalized, including after a phonetic word (`ówpənAI`), with phonetic lowercase endings (`USBz`, `PDFs`, `Xɪz`); preserve symbolic material as written (`1970s`, `e = mc^2`, `sin(x)`, `camelCase`, `fingerd`) |

The acute marks conventional word stress, not necessarily the main sentence prominence. *Not* is `nɒ́t`. Neutral demonstrative determiners are `ðɪs`, `ðæt`, `ðijz`, `ðowz` (*that book* `ðæt bʊ́k`); independent or explicitly contrastive uses take `ðɪ́s`, `ðǽt`, `ðíjz`, `ðówz` (*that is a book* `ðǽt ɪz ə bʊ́k`). Conjunction/relative *that* remains `ðət`. Full vowels can remain unstressed: possessive *our* `awər` and both copular and auxiliary *are* `ɑr` stay bare by default. *Line them up on the board* has accented particle `ə́p` but weak preposition `ɒn`. Interrogative *what's wrong?* uses `wɒ́ts`; fused-relative *take what's left* uses `wɒts`. Independent *his* and pronoun answers are accented, but sentence-final pronouns are not automatically strong. Modal weak forms do not apply to lexical senses such as *a can*, *a will*, *military might*, *a must*, or the month/name *May*. See §6 of the guide for the complete rules and ambiguity defaults.

Notation is a semantic category, not a token shape. The same spelling may be spoken in one context and symbolic in another: *NASA launched it* uses `nǽsə`, while `NASA` used as an identifier stays `NASA`; prose *sine* becomes `sájn`, while the function call `sin(x)` stays unchanged. The transcriber or LLM makes this decision from context. The validator checks mechanical form but cannot prove that notation or grammatical-role classification was correct. A permitted weak spelling does not license it in every context: particle/preposition, determiner/pronoun, interrogative/relative, and lexical/auxiliary distinctions still require source review.

Three distinctions are kept in writing that readers may merge in their own speech: `ɒ` vs `ɑ` (GA merges them), `ǽr` in *carry/marry* (most GA speakers say `ɛr`), and flapping is never written.

## Encoding note

Accents on IPA letters are combining marks (U+0301 acute, U+0300 grave). Some editors and toolchains silently NFC-normalize `æ` + U+0301 into the single character `ǽ` (U+01FD), which the validator flags as `precomposed-ae`. Repair a file with:

```
python -c "import pathlib,sys; p=pathlib.Path(sys.argv[1]); p.write_text(p.read_text(encoding='utf-8').replace(chr(0x1FD), chr(0xE6)+chr(0x301)), encoding='utf-8')" FILE
```

## License

MIT — see [LICENSE](LICENSE).
