# English → IPA Transcription Guide

This document specifies how to transcribe English text into a learner-friendly, IPA-based phonetic notation. Follow it exactly: the goal is that any two transcribers (human or LLM) produce byte-identical output for the same input text.

## 1. Overview

The system is an **IPA-based respelling of rhotic (American-style) English** using **modern glide notation** (the style popularized by Dr. Geoff Lindsey): long vowels and diphthongs are written as vowel + glide (`ij, uw, ej, ow, aj, aw, ɔj`) instead of the traditional `iː, uː, eɪ, oʊ, aɪ, aʊ, ɔɪ`. Stress is marked with **accent marks placed on the vowel itself** — acute `´` for primary stress, grave `` ` `` for secondary stress — never with the IPA marks `ˈ ˌ`.

The text layout mirrors the source: same words in the same order, same spacing and punctuation, all lowercase. The one punctuation exception is a word-internal apostrophe, which is omitted from phonetic words because it represents spelling, not sound (§5.4, §9).

**Reference accent: General American.** Wherever varieties of English disagree — stress placement, vowel choice, yod, silent letters — follow the General American pronunciation (Merriam-Webster's first listing) and map it into this notation. One carve-out: in the weak `ɪ` ~ `ə` zone, where dictionaries contradict one another, the tie-breaker of §4.4 (fixed morphemes, then spelling) decides — not the dictionary. Common traps:

| Word | Write (GA) | Avoid (British) |
|---|---|---|
| either / neither | `íjðər`, `níjðər` | `ájðər`, `nájðər` |
| schedule | `skɛ́dʒuwl` | `ʃɛ́dʒuwl` |
| advertisement | `æ̀dvərtájzmənt` | `ədvɜ́rtɪsmənt` |
| laboratory | `lǽbrətɔ̀rij` | `ləbɒ́rətrij` |
| mobile (adj.) | `mówbəl` | `mówbajl` |
| vitamin | `vájtəmɪn` | `vɪ́təmɪn` |
| leisure | `líjʒər` | `lɛ́ʒər` |
| herb | `ɜ́rb` (silent h) | `hɜ́rb` |
| garage | `ɡərɑ́ʒ` | `ɡǽrɑʒ` |
| -ization | `-əzéjʃən` (`ɔ̀rɡənəzéjʃən`) | `-ajzéjʃən` |

Three deliberate departures from pure GA remain: the `ɒ`/`ɑ` distinction is kept even though GA merges those vowels (§4.1); `æ` is kept before intervocalic r even though most GA speakers merge *marry* into *merry* (§4.3); and allophonic detail such as flapping is never written (§3). Each keeps a distinction in writing that the reader is free to merge in speech.
## 2. The system at a glance

One-glance symbol chart (details in §3–§5):

| | Symbols |
|---|---|
| Short vowels | `ɪ` kit · `ɛ` dress · `æ` trap · `ɒ` lot · `ə` strut + all weak vowels · `ʊ` foot · `ɔ` thought/cloth |
| Long vowels / diphthongs | `ij` fleece · `uw` goose · `ej` face · `ow` goat · `aj` price · `aw` mouth · `ɔj` choice · `ɑ` palm |
| Vowel + r | `ər` letter · `ɜr` nurse · `ɑr` start · `ɔr` north · `ɛr` square · `ɪr` near · `ʊr` cure |
| Consonants | `p b t d k ɡ tʃ dʒ f v θ ð s z ʃ ʒ h m n ŋ l r w j` |
| Stress | acute `´` = primary, grave `` ` `` = secondary, on the first vowel symbol; weak function words unmarked |

1. Transcribe word by word; keep every punctuation mark, space, hyphen, digit, parenthesis, and quote exactly where it was. Omit word-internal apostrophes from phonetic words (§5.4); preserve them in pass-through tokens such as `'70s`.
2. Everything is lowercase — including proper nouns and sentence starts (*John* → `dʒɒ́n`). The only capitals allowed are letter-name tokens (rule 8).
3. Long vowels/diphthongs are vowel + glide: `ij uw ej ow aj aw ɔj`. Never use `ː`, `eɪ`, `oʊ`, etc. The one glide-less long vowel is `ɑ` (PALM: `fɑ́ðər`, `kɑ́m`).
4. The accent is rhotic: every written/underlying r is pronounced (`lɛ́ðər`, `wɜ́rld`, `ɡɑ́rmənt`).
5. No centering schwa before r: SQUARE = `ɛr` (`wɛ́r`), NEAR = `ɪr` (`nɪ́r`). And `ʌ` is never used — STRUT is written `ə`, stressed or not (`kə́lər`, `nə́mbər`).
6. Primary stress = acute on the first vowel symbol of the stressed syllable (`dʒǽkət`, `káwz`). Secondary stress = grave (`fʊ́twɛ̀r`, `mæ̀θəmǽtɪkəl`).
7. Content words always carry an accent — even monosyllables (`méjd`, `fíjl`). Treat *all* (`ɔ́l`), *not* (`nɒ́t`), demonstratives (`ðɪ́s`, `ðǽt`, `ðíjz`, `ðówz`), and verbal particles (`ə́p`, `dáwn`, `áwt`, `ɒ́n`) as content-like. Choose function-word forms by grammatical role (§6): weak monosyllables have **no accent** (`əv`, `ənd`, `tə`, `ðə` / `ðij`, `kən`, `fɔr`); polysyllables keep their internal stress. Interrogative/exclamative *what* is `wɒ́t`; fused-relative *what* is bare `wɒt`. Conjunction/relative *that* remains `ðət`.
8. Digits and years stay in written form (`2`, `1970s`, `'70s`); letters read by name stay as **capital** letters: `T-ʃɜ́rt`, `USB`. A pronounced plural or possessive suffix is lowercase and phonetic: `USBz`, `PDFs`, `Xɪz`. Equations, formulas, and units pass through verbatim: `e = mc^2`, `sin(x)`, `km/h` (§9).
9. Use IPA letterforms: `ɡ` (U+0261) not `g`, `j` for the *y* sound, `r` not `ɹ`.
10. When varieties of English disagree, General American wins: `íjðər`, `skɛ́dʒuwl`, `ɜ́rb` (§1).

## 3. Consonants

| Symbol | Sound | Example |
|---|---|---|
| p b t d k ɡ | stops | `pǽnts`, `búwts`, `ɡɑ́rmənt` |
| tʃ dʒ | church, judge | `tʃɛ́r`, `dʒǽkət` |
| f v θ ð s z ʃ ʒ h | fricatives | `θrów`, `ðə`, `ʃíjp`, `júwʒəlij`, `hájd` |
| m n ŋ | nasals | `méjd`, `nówn`, `pə́ŋk`, `lɔ́ŋ` |
| l r w j | approximants | `lɛ́ðər`, `rúwm`, `wʊ́l`, `jɔr` |

Notes:

- **No allophonic detail, including reduction or deletion.** Preserve the consonants in a word's broad citation-form transcription even when they may be weakened or omitted in casual speech: *identifiers* → `ajdɛ́ntəfàjərz`, *departmental* → `dɪpɑ̀rtmɛ́ntəl`. Likewise, do not write flapping (*putting* → `pʊ́tɪŋ`, *water* → `wɔ́tər` — t stays t), glottal stops `ʔ`, dark l `ɫ`, or aspiration marks. This does not restore consonants that are absent from the standard General American pronunciation, such as the silent h in *vehicle* (`víjɪkəl`).
- *wh-* is plain `w` (`wɪ́tʃ`), never `ʍ`.
- *-ng* is `ŋ` finally (`lɔ́ŋ`) and `ŋɡ` where /ɡ/ is really pronounced (`sɪ́ŋɡəl`, `fɪ́ŋɡər`); *-nk* is `ŋk` (`pɪ́ŋk`, `θǽŋks`).
- Syllabic consonants are written with schwa: `téjbəl`, `kɒ́tən`, `rɪ́ðəm` — never `l̩ n̩ m̩`.

## 4. Vowels

### 4.1 Checked (short) vowels

| Symbol | Lexical set | Examples |
|---|---|---|
| ɪ | KIT | `wɪ́tʃ`, `sɪ́lk`, `bɪ́ldɪŋ` |
| ɛ | DRESS | `dɛ́nɪm`, `lɛ́ðər`, `wɛ́ðər` |
| æ | TRAP | `dʒǽkət`, `blǽŋkət`, `ǽnɪməl` |
| ɒ | LOT | `kɒ́tən`, `bɒ́dij`, `spɒ́t`, `prɒ́bləm`, `wɒ́ʃɪz` |
| ə | STRUT (and all weak vowels, §4.4) | `pə́fər`, `kə́lər`, `nə́mbər`, `lə́v` |
| ʊ | FOOT | `wʊ́l`, `bʊ́k`, `pʊ́tɪŋ` |
| ɔ | THOUGHT + CLOTH | `smɔ́l`, `kɔ́l`, `tɔ́l`, `ɔ́fən`, `ɔ́f`, `lɔ́ŋ`, `sɔ́ft`, `əkrɔ́s`, `dɔ́ɡ` |

**Never use `ʌ`.** STRUT shares its symbol with the weak vowel: a stressed STRUT syllable is simply `ə` with an accent mark — `lə́v` (*love*), `mə́nij` (*money*), `sə́mər` (*summer*), `ə̀ndərstǽnd` (*understand*).

**The `-come` trap.** *become, income, outcome, overcome, welcome* all keep the STRUT vowel in `-come` (`bɪkə́m`, `ɪ́nkə̀m`, `áwtkə̀m`, `òwvərkə́m`, `wɛ́lkəm`), never the GOAT vowel of unrelated `-ome` words like *home, dome, chrome* (`hówm`, `dówm`, `krówm`) — the shared spelling invites the wrong glide.

Splitting `ɒ` vs `ɑ` vs `ɔ` — **the length principle**: in this vowel area, write `ɑ` wherever the vowel tends to be **long**, and `ɒ` where it is short:

- `ɒ` = LOT words (short vowel): *hot, stop, top, body, object, problem, model, wash, watch, what, because* (`bɪkɒ́z`).
- `ɑ` = PALM words (long vowel): *father* `fɑ́ðər`, *calm* `kɑ́m`, *palm* `pɑ́m`, *almond* `ɑ́mənd`, *spa* `spɑ́`, *façade* `fəsɑ́d`, *lager* `lɑ́ɡər`. The same length principle gives START its `ɑr` (§4.3) and puts `ɑ` in the *qua-* family, where the vowel runs long in American English: `kwɑ́lɪtij` (*quality*), `kwɑ́ntɪtij` (*quantity*), `kwɑ́ntɪfàj` (*quantify*), `ɪ̀nijkwɑ́lɪtij` (*inequality*), `kwɑ́lɪtèjtɪv`.
- `ɔ` = THOUGHT words (*all, call, law, thought, caught*) **and** CLOTH words (*off, often, soft, cost, lost, long, strong, wrong, across, dog*). If an American dictionary shows /ɔ/ (or /ɒ~ɔː/ variation resolved toward /ɔː/), write `ɔ`.
- **Operational test for `ɒ` vs `ɑ`:** check the British (RP) form — RP short /ɒ/ → `ɒ`, RP long /ɑː/ → `ɑ`. This RP lookup decides only which symbol to write — GA itself merges the two vowels; everything else about the word still follows GA (§1). (The *qua-* family above is the one deliberate exception: RP has /ɒ/ there, but this system follows the long American vowel.)

### 4.2 Free vowels (glide notation)

| Symbol | Lexical set | Examples | Never write |
|---|---|---|---|
| ij | FLEECE | `píjs`, `ʃíjp`, `fíjld`, `ríjdɪŋ` | iː, i: |
| uw | GOOSE | `blúw`, `búwts`, `rúwm` | uː, u: |
| ej | FACE | `méjd`, `stéjpəl`, `déj` | eɪ |
| ow | GOAT | `nówn`, `kówt`, `ównlij` | oʊ, əʊ |
| aj | PRICE | `tájp`, `hájd`, `stájl` | aɪ |
| aw | MOUTH | `káwz`, `ráwnd`, `dáwn` | aʊ |
| ɔj | CHOICE | `pɔ́jnt`, `mɔ́jstʃər`, `tʃɔ́js` | ɔɪ, oj |
| ɑ | PALM | `fɑ́ðər`, `kɑ́m`, `spɑ́` | ɑː, a: |

`ɑ` is the only free (long) vowel written without a glide — it is simply the long *ah*. See §4.1 for how to split it from short `ɒ`.

### 4.3 Vowels + r (always rhotic)

| Symbol | Lexical set | Examples |
|---|---|---|
| ər | lettER (unstressed) | `lɛ́ðər`, `fɜ́rnɪtʃər`, `ə́ðər` |
| ɜr | NURSE | `wɜ́rld`, `ʃɜ́rt`, `pɜ́rfəkt`, `lɜ́rnɪŋ` |
| ɑr | START | `ɡɑ́rmənt`, `skɑ́rf`, `ɑ́rm`, `kɑ́rpət` |
| ɔr | NORTH/FORCE | `wɔ́rm`, `ʃɔ́rt`, `fɔ́rs`, `sɔ́rs`, `dɔ́r` |
| ɛr | SQUARE | `wɛ́r`, `tʃɛ́r`, `ɛ́rijə`, `vɛ́rijəs` |
| ɪr | NEAR | `nɪ́r`, `mətɪ́rijəl`, `ʃæ̀ndəlɪ́r`, `pɪ́rijəd` |
| ʊr | CURE | `dʊ́rəbəl`, `dʊ́rɪŋ`, `ʃʊ́r`, `pjʊ́r`, `sɪkjʊ́rɪtij` |
| ajər / awər | fire / hour | `rɪkwájər`, `ətájər`, `áwər`, `páwər` |

Rules:

- **No r-vowel takes a centering `ə`.** Never write `ɛər`, `ɪər`, `ʊər`: *wear* `wɛ́r`, *near* `nɪ́r`, *sure* `ʃʊ́r`.
- DRESS + r and SQUARE are both plain `ɛr`: *very* `vɛ́rij`, *vary* `vɛ́rij`, *error* `ɛ́rər`, *care* `kɛ́r`, *area* `ɛ́rijə`.
- KIT + r and NEAR are both plain `ɪr`: *mirror* `mɪ́rər`, *spirit* `spɪ́rɪt`, *material* `mətɪ́rijəl`, *period* `pɪ́rijəd`.
- **Intervocalic TRAP override — apply before the M-W rule (§1).** When the lexical vowel is TRAP /æ/ and `r` is followed by another vowel within the word, always write `ǽr`, even when merged General American speech suggests `ɛ́r`. This is a general category, not a closed list: `kǽrəktər` (*character*), `kǽrij` (*carry*), `mǽrij` (*marry*), `pǽrəmàwnt` (*paramount*). Contrast non-TRAP words such as `pɛ́rənt` (*parent*) and `vɛ́rij` (*very/vary*). Readers whose accent merges *marry* with *merry* may pronounce written `ǽr` as `ɛ́r`.
- Unstressed NURSE/letter syllables are all plain `ər`: `sərprájz`, `pərhǽps`.

**Vowels before intervocalic r** (r between vowels inside a word):

| Write | Examples |
|---|---|
| ɛ́r | *very* `vɛ́rij`, *error* `ɛ́rər`, *parent* `pɛ́rənt` |
| ɪ́r | *mirror* `mɪ́rər`, *spirit* `spɪ́rɪt`, *serious* `sɪ́rijəs` |
| ǽr | *carry* `kǽrij`, *marry* `mǽrij`, *character* `kǽrəktər`, *paramount* `pǽrəmàwnt` — always write `ǽr` for lexical TRAP; readers may merge it with `ɛ́r` in speech |
| ɜ́r | *hurry* `hɜ́rij`, *courage* `kɜ́rɪdʒ`, *current* `kɜ́rənt` — STRUT + r merges into NURSE (no `ə́r` here) |
| ɒ́r | *borrow* `bɒ́row`, *sorry* `sɒ́rij`, *tomorrow* `təmɒ́row` |
| ɔ́r | *orange* `ɔ́rɪndʒ`, *story* `stɔ́rij`, *glory* `ɡlɔ́rij` |

### 4.4 Weak (unstressed) vowels

| Symbol | Where | Examples |
|---|---|---|
| ə | any reduced vowel spelled with a letter other than i/y (tie-breaker below); endings *-al, -on, -an, -ous, -ment, -est*; prefixes *a-, pro-, con-* | `əbáwt`, `prəfáwnd`, `dʒǽkət`, `mɑ́rkət`, `téjbəl`, `kɒ́tən` |
| ɪ | reduced vowels spelled with i or y (tie-breaker below); endings *-ing, -ic, -ity, -ish, -ify, -ible*; the fixed morphemes *-ed* `ɪd`, *-es* `ɪz`, *-age* `ɪdʒ`, *-ange* `ɪndʒ`; prefixes *in-, im-, dis-* and the reduced prefixes *be-, de-, re-, pre-, se-, e-/ex-* (`ɪks`/`ɪɡz`) | `ríjdɪŋ`, `níjdɪd`, `wɒ́ʃɪz`, `prɒ́fɪt`, `bɪkɒ́z`, `dɪzájnd`, `rɪméjnz`, `ɪɡzǽmpəl`, `lǽŋɡwɪdʒ` |
| ij | happY: final *-y, -ey, -ie*; *-ly*; before another vowel | `bɒ́dij`, `kówzij`, `lájklij`, `ɛ́rijə` |
| uw | unstressed GOOSE | `vǽljuw`, `mɛ́njuw` |
| ow | unstressed GOAT | `fɒ́low`, `ǽrowz`, `rɛ́trow` |

**The `ɪ` ~ `ə` tie-breaker.** Many reduced syllables could be `ɪ` or `ə` and both are correct — this is the zone some dictionaries mark with `ᵻ` and contradict each other on. Never use `ᵻ`; decide deterministically, in this order:

1. The §6 weak-form table and §7 suffix table win where they apply.
2. Fixed morphemes, regardless of spelling — endings: *-ed* → `ɪd` (`níjdɪd`), *-es* → `ɪz` (`wɒ́ʃɪz`), *-age* → `ɪdʒ` (`lǽŋɡwɪdʒ`, `kɜ́rɪdʒ`), reduced *-ange* → `ɪndʒ` (`ɔ́rɪndʒ` — stressed *-ange* is unaffected: `əréjndʒ`); word-initial reduced prefixes *be-, de-, re-, pre-, se-, e-/ex-* → `ɪ` (`bɪkɒ́z`, `bɪfɔ́r`, `dɪzájn`, `rɪméjnz`, `prɪzɛ́nt`, `sɪkjʊ́rɪtij`, `ɪɡzǽmpəl`, `ɪkspɛ́rɪmənt`). Only when reduced and word-initial: stressed *re-* keeps its full vowel (`rɛ́trow`), and word-internal syllables fall through to the spelling rule (`rɛ̀prəzɛ́ntɪd`).
3. Otherwise follow the **spelling** of the reduced vowel: **i or y → `ɪ`** (`prɒ́fɪt`, `mɛ́dɪsɪn`, `ǽnəlɪst`); **any other letter → `ə`** (`dʒǽkət`, `mɑ́rkət`, `mɪ́nət`).
4. Vowel digraphs default to `ə`: *mountain* `máwntən`, *captain* `kǽptən`, *foreign* `fɔ́rən`. When one letter of the digraph is silent, the sounded letter decides: *biscuit* `bɪ́skɪt`, *circuit* `sɜ́rkɪt` (the u is silent, as in *build*).

The rule touches only genuinely reduced vowels — happY `ij` (`bɒ́dij`) and stressed vowels are unaffected. Within this zone the tie-breaker outranks dictionary notation (§1).

**Syncope — parenthesized schwas are dropped.** When Merriam-Webster's first listing shows a medial schwa in parentheses — \(ə-)\ — the syllable is omitted, because the compressed form is how the word is spoken: *different* `dɪ́frənt`, *difference* `dɪ́frəns`, *sovereign* `sɒ́vrən`, *laboratory* `lǽbrətɔ̀rij`, *deliberate* (adj.) `dɪlɪ́brət`. When M-W lists the full form unparenthesized, the schwa stays: *natural* `nǽtʃərəl`. The fixed transcriptions of §6 and §7 outrank this rule — *-ally* is always `əlij` (`tɪ́pɪkəlij`), even where M-W parenthesizes it.

### 4.5 Glide linking inside words

When a syllable ending in `ij / ej / aj / ɔj` is followed by another vowel, link with `j`:

- *area* → `ɛ́rijə`, *various* → `vɛ́rijəs`, *material* → `mətɪ́rijəl`, *linear* → `lɪ́nijər`, *creation* → `krijéjʃən`, *associated* → `əsówsijèjtɪd`.

Sequences with `uw / ow / aw` before a vowel are left as-is (`fɒ́lowɪŋ`, `awər`); the *-ual* ending is written `wəl` (`vɪ́ʒwəl`, `kǽʒəwəl`).

### 4.6 Yod (/j/ before uw) — American yod-dropping

General American drops /j/ after coronal consonants; this style follows that rule:

- **No yod after t, d, n, s, z, l, θ, r** when the consonant starts the same syllable: `núw` (*new*), `dúw` (*due*), `túwn` (*tune*), `stúwdənt` (*student*), `núwmərəs` (*numerous*), `əsúwm` (*assume*), `rúwl` (*rule*), `ǽtɪtùwd` (*attitude*), `ǽvənùw` (*avenue*).
- **Keep yod after the other consonants** (p, b, m, f, v, k, ɡ, h): `pjʊ́r`, `bjúwtəfəl`, `mjúwzɪk`, `fjúw`, `vjúw`, `kjúwb`, `ɑ́rɡjəmənt`, `hjúwmən`.
- **Keep yod when it starts its own unstressed syllable**, even after a coronal: `vǽljuw` (*value*), `mɛ́njuw` (*menu*), `kəntɪ́njuw` (*continue*).
- Unstressed *-ture / -dual / -duate* coalesce: `néjtʃər`, `fɜ́rnɪtʃər`, `ɡrǽdʒuwəl`, `ɛ̀dʒəkéjʃən`-type words use `dʒ`.
- When unsure, follow the first pronunciation listed in an American dictionary (e.g. Merriam-Webster).
## 5. Stress marking

### 5.1 The marks and where they go

- **Primary stress:** acute accent `´` (combining U+0301).
- **Secondary stress:** grave accent `` ` `` (combining U+0300).
- The mark sits on the **first vowel symbol of the syllable nucleus** — never on a glide or consonant:
  - `áj`, `éj`, `ów`, `úw`, `íj`, `áw`, `ɔ́j` (accent on the first letter, not on j/w)
  - `ɛ́r`, `ɪ́r`, `ɜ́r`, `ɑ́r`, `ɔ́r` (accent on the vowel, not on r)
  - `júwzd` — the accent goes on `u` (the first *vowel*; `j` is a consonant here).

### 5.2 Which words get marked

The acute marks conventional word stress in this system, **not necessarily the main prominence of the sentence**. Marking every content word does not mean emphasizing each one in speech. Likewise, a full vowel can be unstressed: `maj`, `awər`, and `ɑr` need no acute in neutral use. Vowel reduction, word stress, and sentence focus are separate decisions.

- **Unhyphenated content words** (nouns, lexical verbs, adjectives, adverbs, numerals, interjections) always carry exactly one acute — including monosyllables: `méjd`, `fíjl`, `wɔ́rm`, `ǽd`, `tíj`, `wə́n`. Treat *all*, *not*, demonstratives, independent possessives, independent *some*, and verbal particles as content-like (§6). Copular *be* is an explicit exception: it stays weak by default, just like auxiliary *be*. In hyphenated compounds, apply the rule separately to each element (§5.3).
- **Function words** in their weak form get **no accent at all**, even when the vowel is full: `æz`, `bət`, `səm` (indefinite determiner), `wɒt` (fused relative), `majt` (modal), `wʊd`, `hɪz` (possessive determiner), `ɒn` (preposition). See §6 for role-dependent forms and fixed exceptions. This bare form is for monosyllables only: a function word of two or more syllables keeps the acute of its word-internal stress even when weak — `ɪ́ntə` (*into*), `əbáwt` (*about*), `ówvər` (*over*). The `ajər / awər` nuclei count as one syllable for this convention, so neutral *our* stays bare: `awər`; explicit contrast takes `áwər`.
- **Wh-question words are accented** (`wɪ́tʃ`, `wɛ́n`, `wɛ́r`, `húw`, `wáj`, `háw`, `wɒ́t`), including in embedded questions. Interrogative and exclamative *what* takes `wɒ́t`; fused-relative *what* takes `wɒt` (§6). Contractions inherit that distinction: interrogative *what's* `wɒ́ts`, fused-relative *what's* `wɒts`.
- An unhyphenated word never has more than one acute. Longer words add graves for secondary stresses: `mæ̀θəmǽtɪkəl`, `rɛ̀prəzɛ́ntɪd`, `əsówsijèjtɪd`, `vɜ̀rsətɪ́lɪtij`, `ə̀nlájk`. A hyphenated compound may contain one acute in each content-word element (§5.3).

### 5.3 Compounds

- **Solid compounds** (one written word): acute on the first element, grave on the second: `fʊ́twɛ̀r`, `bʊ́kʃɛ̀lf`, `nájtstæ̀nd`, `mówtərsàjkəl`, `sə́bkə̀ltʃər`, `wɜ́rldwàjd`.
- **Hyphenated compounds:** each element is transcribed and accented on its own, hyphen kept: `fríj-stǽndɪŋ`, `blúw-tɪ́ntɪd`, `wɔ́l-tə-wɔ́l`, `lɔ́ŋ-lǽstɪŋ`.
- Suffix-driven secondary stress: *-ate* verbs and *-ize* verbs take a grave on the suffix: `rɛ́ɡjəlèjt`, `vɪ́ʒwəlàjz`.

### 5.4 Contractions

- Omit word-internal apostrophes and transcribe the whole pronounced form as one phonetic word. The apostrophe encodes spelling, not a sound: *it's* and *its* are both `ɪts`; *wearer's* is `wɛ́rərz`; *O'Connor* is `owkɒ́nər`.
- A contraction or possessive carries the stress of its host: `ɪts` stays unaccented, while `wɛ́rərz` keeps the acute of *wearer*.
- Existential *there's* is weak `ðərz`; locative *there's* takes `ðɛ́rz`. Relative *that's* is weak `ðəts` (*a book that's open*), while demonstrative *that's* is `ðǽts` (*that's another chapter*). Choose by grammatical role, not by the contraction alone.
- This includes role-dependent *what*: *what's wrong?* → `wɒ́ts rɔ́ŋ?`, but *take what's left* → `téjk wɒts lɛ́ft`.
- Pronoun + auxiliary contractions whose pronoun has a free vowel take an acute: `ðéjv` (*they've*), `ðɛ́r` (*they're*), `júwr` (*you're*), `wíjr` (*we're*), `ájl` (*I'll*).
- Negative contractions are content-like and accented: `dównt`, `kǽnt`, `wównt`, `ɪ́zənt`.

## 6. Weak and accented forms by grammatical role (reference)

Classify the word's **grammatical role before choosing its form**. Use the weak entries below in neutral running text, except where a role-dependent or fixed accented form is specified. Weak monosyllables are unaccented; polysyllables retain word-internal stress (§5.2). Explicit contrast, citation, and the clause-final cases below take strong accented forms. Do not infer emphasis just from a full vowel or capitalization at the start of a sentence.

| Category | Forms |
|---|---|
| Articles | *a* `ə` · *an* `ən` · *the* `ðə` before a consonant sound, `ðij` before a vowel sound |
| Conjunctions | *and* `ənd` · *or* `ɔr` · *but* `bət` · *if* `ɪf` · *as* `æz` · *than* `ðən` · *that* (conj./relative) `ðət` |
| Prepositions | *of* `əv` · *to* `tə` (also before vowels: `tə ǽd`) · *into* `ɪ́ntə` (polysyllabic — keeps its acute, §5.2) · *in* `ɪn` · *on* `ɒn` · *at* `ət` · *by* `baj` · *for* `fɔr` · *from* `frəm` · *with* `wɪð` |
| Directional prepositions | *up* `əp` (*up the hill*) · *down* `dawn` (*down the road*) · *out* `awt` (*out the door*, American usage). These bare forms are not verbal-particle forms. |
| Pronouns | *I* `aj` · *you* `juw` · *he* `hij` · *she* `ʃij` · *it* `ɪt` · *we* `wij` · *they* `ðej` · *me* `mij` · *him* `hɪm` · *her* `hər` · *us* `əs` · *them* `ðɛm` — neutral connected-speech forms; independent answers and explicit focus take strong accented forms (see below). |
| Possessive determiners | *my* `maj` · *your* `jɔr` · *his* `hɪz` · *its* `ɪts` · *our* `awər` · *their* `ðɛr`. A full vowel does not require an acute; contrastive *our* is `áwər`. Independent possessive *his* is `hɪ́z`, not the determiner form (see below). |
| Demonstratives | *this* `ðɪ́s` · *these* `ðíjz` · *that* `ðǽt` · *those* `ðówz` — accented both as determiners and as independent pronouns. Conjunction/relative *that* remains weak `ðət`. |
| *be* | *am* `əm` · *is* `ɪz` · *are* `ɑr` · *was* `wəz` · *were* `wər` · *be* `bij` · *been* `bɪn` — weak by default in both copular and auxiliary uses: *they are happy* and *they are working* both use `ɑr`. Explicit contrast and clause-final ellipsis take strong forms. |
| *have* | *have* `həv` · *has* `həz` · *had* `həd` — as auxiliaries (followed by a past participle). Main-verb *have / has / had* — possession, experience, consumption, any lexical meaning — are content words: *I have a car* → `aj hǽv ə kɑ́r`; *she has had breakfast* → `ʃij həz hǽd brɛ́kfəst`; *we had a great time* → `wij hǽd ə ɡréjt tájm`. Obligation *have to / has to* devoice: `hǽf tə`, `hǽs tə`. (See Example 4.) |
| *do* | *do* `dúw` (fixed exception: always accented, including as an auxiliary). Auxiliary *does* `dəz` · *did* `dɪd`; lexical *does* `də́z` · *did* `dɪ́d`: *she does the work*, *she did the work*, *it does so*. Auxiliaries also take the accented forms under explicit contrast, affirmative emphatic do-support (*it does work*), or clause-final ellipsis (*yes, she did*). |
| Modals | *can* `kən` · *could* `kʊd` · *will* `wɪl` · *would* `wʊd` · *shall* `ʃəl` · *should* `ʃʊd` · *may* `mej` · *might* `majt` · *must* `məst` — only in modal uses; lexical homonyms are content words (see below). |
| Other | *not* `nɒ́t` (always accented) · *some* `səm` as an indefinite determiner; independent or explicitly contrastive *some* `sə́m` · *all* `ɔ́l` (always accented) · *there* (existential) `ðər`; locative *there* is content: `ðɛ́r` · interrogative/exclamative *what* `wɒ́t`; fused-relative *what* `wɒt` |

Quantifiers/adverbs like *all* `ɔ́l`, *any* `ɛ́nij`, *every* `ɛ́vrij`, *both* `bówθ`, *each* `íjtʃ`, *only* `ównlij`, *very* `vɛ́rij`, *well* `wɛ́l`, *still* `stɪ́l`, *just* `dʒə́st` count as **content words** and are accented. *All* keeps its acute in every use, including *all the pieces* and *at all*. This is a notation convention, not a claim that it always bears sentence focus.

**Not and demonstratives.** Always write the independent word *not* as `nɒ́t`, including in *not only*. Negative contractions keep their existing accented forms (§5.4). All four demonstratives are accented in both determiner and independent uses: *this book* `ðɪ́s bʊ́k`, *what's this?* `wɒ́ts ðɪ́s?`, *these books* `ðíjz bʊ́ks`, *those are mine* `ðówz ɑr májn`. This aligns *this / these / those* with demonstrative *that*; conjunction/relative *that* remains `ðət`. These are fixed word-stress conventions, not instructions to put sentence focus on every negative or demonstrative. Match whole words, not substrings: *nothing*, *notice*, and negative contractions are not rewritten as separate *not* tokens.

**Independent possessives and pronoun answers.** Possessive determiners stay weak in neutral use (*his book* `hɪz bʊ́k`), but independent possessives are accented (*the book is his* `ðə bʊ́k ɪz hɪ́z`, *a friend of his* `ə frɛ́nd əv hɪ́z`). *Mine, yours, hers, ours,* and *theirs* are likewise accented. Personal pronouns take their strong accented form when they stand as an independent answer or are explicitly focused: *who did it? me.* → `húw dɪd ɪt? míj.` Use the full strong pronunciation where it differs from the weak one, such as contrastive *her* `hɜ́r`, not an acute added to weak `hər`. Do not accent a pronoun merely because it ends a sentence: neutral *I saw him* is `aj sɔ́ hɪm`.

**Lexical homonyms of modals.** The modal row is not a word-wide weak-form dictionary. Nouns and lexical verbs follow the content-word rule: *can* `kǽn` (*a can*, *to can food*), *will* `wɪ́l` (*a will*, *to will something*), *might* `májt` (*military might*), *must* `mə́st` (*a must*), and *May* `méj` (month or personal name). Their modal uses retain the weak forms above. Decide from meaning and grammar, not capitalization alone; a sentence-initial *May* can still be a modal. The same role-first principle applies to lexical *have / has / had / does / did*.

**Verbal particles are accented.** Treat the particle in a phrasal verb as content-like: *up* `ə́p`, *down* `dáwn`, *out* `áwt`, *on* `ɒ́n`, *off* `ɔ́f`, *in* `ɪ́n`, *back* `bǽk`, *away* `əwéj`, etc. This applies both next to the verb and when separated by an object: *turn on the light*, *turn the light on*, *turn it on*. The particle keeps its written acute even when the object carries the main spoken prominence. Do not extend this rule to every preposition in a multiword verb: *look at*, *rely on*, and *listen to* retain weak prepositions.

| Construction | Role and transcription |
|---|---|
| *put on a watch* | particle: `pʊ́t ɒ́n ə wɒ́tʃ` |
| *find out* | particle: `fájnd áwt` |
| *line them up on the board* | particle *up*, preposition *on*: `lájn ðɛm ə́p ɒn ðə bɔ́rd` |
| *rely on them* | preposition: `rɪláj ɒn ðɛm` |
| *put up with it* | particle *up*, preposition *with*: `pʊ́t ə́p wɪð ɪt` |
| *walk up the hill* | directional preposition: `wɔ́k əp ðə hɪ́l` |
| *slide out of bed* | directional complex preposition *out of*: `slájd awt əv bɛ́d` |

Object movement (*turn on the light* → *turn the light on*) is useful evidence for a particle, not a universal test. Intransitive particles need no object (*give up*), and idiomatic meaning alone does not make a preposition a particle (*rely on*). Use the construction's meaning and grammar; if the text permits multiple readings, use the ordinary literal prepositional reading unless context establishes a particle construction. Standalone directional or temporal adverbs also take an acute: *look up*, *come in*, *go out*, *from now on* (`frəm náw ɒ́n`). In hyphenated derivatives, the particle element keeps its acute: *follow-up* `fɒ́low-ə́p`, *built-in* `bɪ́lt-ɪ́n`; actual prepositions in compounds remain weak (*step-by-step* `stɛ́p-baj-stɛ́p`, §5.3).

**Some.** Use bare `səm` before a noun in an indefinite, noncontrastive noun phrase (*some pieces*, *some old pieces*). Use `sə́m` when it stands independently (*some were chipped*, *take some*, *some of them*) or is explicitly contrastive (*some pieces, not all*). Do not infer contrast merely because other possibilities exist.

**What.** Direct and embedded interrogatives take `wɒ́t`: *what do you need?*, *I wonder what you need*. Exclamatives also take `wɒ́t`: *what a day!* A fused relative denotes a thing rather than asks a question and takes `wɒt`: *take what you need* (= *the things that you need*). Where an embedded construction genuinely permits both readings, use the fused-relative form unless the context establishes a question. Apply the same distinction to contractions: *what's wrong?* `wɒ́ts rɔ́ŋ?`, *take what's left* `téjk wɒts lɛ́ft`. Do not change words containing *what*, such as *whatever*, by substring replacement.

**The article *the*.** Choose its weak form from the first **sound** of the next word, not its first written letter: `ðə bʊ́k`, `ðij ǽpəl`, `ðə jùwnəvɜ́rsətij` (*the university*), `ðij áwər` (*the hour*). Apply the same sound test when the next token passes through unchanged: `ðij 8`, `ðij FBI`, but `ðə USB`. Both weak forms are unaccented. Genuine emphasis or citation takes the strong form `ðíj` (*not a solution, the solution*).

**Strong forms at clause ends:** a stranded preposition with no following complement, or an auxiliary or *be* form whose complement is elided, takes its strong, accented form: *what are you looking at?* → `wɒ́t ɑr juw lʊ́kɪŋ ǽt?`; *where do you come from?* → `wɛ́r dúw juw kə́m frɒ́m?`; *yes, it is.* → `jɛ́s, ɪt ɪ́z.` Strong forms: *at* `ǽt`, *of* `ɒ́v`, *to* `túw`, *for* `fɔ́r`, *from* `frɒ́m`, *is* `ɪ́z`, *are* `ɑ́r`, *was* `wɒ́z`, *has* `hǽz`, *can* `kǽn`, *have* `hǽv`, *would* `wʊ́d`, *does* `də́z`, *did* `dɪ́d`. This is not a rule to accent every function word before punctuation.

## 7. Suffix cheat sheet

| Spelling | Transcription | Example |
|---|---|---|
| -ing | `ɪŋ` | `ríjdɪŋ` |
| -ed | `t` / `d` / `ɪd` | `dréjpt`, `tǽnd`, `níjdɪd` |
| -s / -es | `s` / `z` / `ɪz` | `bʊ́ks`, `káwz`, `wɒ́ʃɪz` |
| -y / -ies | `ij` / `ijz` | `bɒ́dij`, `æktɪ́vɪtijz` |
| -ly / -ally / -ily | `lij` / `əlij` / `ɪlij` | `lájklij`, `tɪ́pɪkəlij`, `íjzɪlij` |
| -er / -or / -est | `ər` / `ər` / `əst` | `kúwlər`, `vɛ́ktər`, `sɪ́mpləst` |
| -ity / -ities | `ɪtij` / `ɪtijz` | `dʊ̀rəbɪ́lɪtij`, `kwɑ́ntɪtijz` |
| -age | `ɪdʒ` | `kɜ́rɪdʒ`, `bɛ́vrɪdʒ`, `lǽŋɡwɪdʒ` |
| -tion / -ssion | `ʃən` | `krijéjʃən`, `dɪskə́ʃən` |
| -sion (voiced) | `ʒən` | `dɪsɪ́ʒən`, `vɜ́rʒən` |
| -ture / -sure | `tʃər` / `ʒər` | `fɜ́rnɪtʃər`, `mɛ́ʒər` |
| -able / -ible | `əbəl` / `ɪbəl` | `dʊ́rəbəl`, `ɪnkrɛ́dɪbəl` |
| -ous / -al / -ful / -less / -ness | `əs` / `əl` / `fəl` / `ləs` / `nəs` | `rɪbɛ́ljəs`, `nǽtʃərəl`, `júwsfəl`, `tájmləs`, `kówzijnəs` |
| -ment / -ent / -ant / -ence / -ance | `mənt` / `ənt` / `ənt` / `əns` / `əns` | `stéjtmənt`, `dɪ́frənt`, `ɪmpɔ́rtənt`, `dɪ́frəns` |
| -ate (verb, 3+ syllables) | `èjt` | `rɛ́ɡjəlèjt`, `əsówsijèjt` |
| -ate (noun/adj.) | `ət` | `dɪlɪ́brət` |
| -ize / -ized | `àjz` / `àjzd` | `vɪ́ʒwəlàjz`, `vɪ́ʒwəlàjzd` |
| -ic / -ical | `ɪk` / `ɪkəl` | `àjkɒ́nɪk`, `tɪ́pɪkəl` |
| -ism / -ist | `ɪzəm` / `ɪst` | `ríjəlɪzəm`, `ɑ́rtɪst` |

Two-syllable *-ate* verbs carry the **primary** stress on the suffix instead — no grave: `krijéjt` (*create*), `rɪléjt` (*relate*).

## 8. Heteronyms — same spelling, two pronunciations

Disambiguate by part of speech (or tense) from context **before** transcribing:

| Spelling | One reading | The other |
|---|---|---|
| record | noun `rɛ́kərd` | verb `rɪkɔ́rd` |
| present | noun/adj. `prɛ́zənt` | verb `prɪzɛ́nt` |
| object | noun `ɒ́bdʒɛkt` | verb `əbdʒɛ́kt` |
| use | noun `júws` | verb `júwz` |
| close | adj. `klóws` | verb `klówz` |
| live | adj. `lájv` | verb `lɪ́v` |
| read | present `ríjd` | past/participle `rɛ́d` |
| lead | verb / leash `líjd` | the metal `lɛ́d` |
| minute | time unit `mɪ́nət` | tiny `majnúwt` |

The list is not exhaustive — any noun/verb pair with shifting stress (*permit, conduct, increase, project, contract…*) follows the *record* pattern: the noun stresses the first syllable, the verb the second.

Related but grammar-driven rather than spelling-driven: *have / has / had*, *that*, *there*, *some*, *what*, *does / did*, and particle/preposition pairs switch between weak and accented forms by syntactic role — see §6. *Do* itself stays accented as a fixed exception; copular and auxiliary *be* both stay weak by default.

## 9. Text formatting rules

1. **Lowercase everything** — sentence-initial words, proper nouns, acronym-derived words: *John* → `dʒɒ́n`. The single exception is capital letters in letter-name tokens (rule 5).
2. **Preserve punctuation and spacing** exactly: `. , ? ! ; : ( ) " -` and any others. One source word → one transcribed token in the same position. The only exception is the word-internal apostrophe described in rule 3.
3. **Omit apostrophes inside phonetic words:** *it's* → `ɪts`, *wearer's* → `wɛ́rərz`, *don't* → `dównt`, *O'Connor* → `owkɒ́nər`. Preserve apostrophes that act as quotation marks and those inside pass-through digit or notation tokens (`'70s`).
4. **Digits, years, decades, and numbers stay as written**: `2`, `100`, `1970s`, `'70s`. Do not spell them out phonetically.
5. **Letters read by name stay as CAPITAL letters.** Outside verbatim notation (rule 8), an uppercase letter is the unambiguous signal "say this letter's name": *T-shirt* → `T-ʃɜ́rt`, *X-ray* → `X-réj`, *USB* → `USB`, *AI* → `AI`. Attach pronounced plural and possessive endings directly to this capital stem in lowercase phonetic form. Choose the regular English allomorph from the final sound of the last letter name: `s` after a voiceless non-sibilant (*PDFs* → `PDFs`, because *F* ends in /f/); `ɪz` after a sibilant (*X's* → `Xɪz`); otherwise `z` (*USBs* or *USB's* → `USBz`, *PCs* → `PCz`). The spelling apostrophe is omitted under rule 3. Acronyms pronounced as words are ordinary words — fully phonetic and lowercase, including their endings (*NASA* → `nǽsə`, *NASAs* → `nǽsəz`; *laser* → `léjzər`).
   A spoken word followed directly by letter names stays one token: *OpenAI* → `ówpənAI`, *OpenAI's* → `ówpənAIz`. Keep the phonetic part's stress and vowel rules; the capital part represents letter names, not untranscribed spelling. Do not insert a space or hyphen absent from the source. The article follows the initial sound of the phonetic part: `ðij ówpənAI tɛ́st`.
6. **Never insert or delete words.** The transcription must align 1:1 with the source text.
   Preserve abbreviation punctuation too: *U.S.* → `U.S.`, *Mrs.* → `mɪ́sɪz.`. When expanding an abbreviation would break token alignment, use a letter-name rendering with the original punctuation: *e.g.* → `E.G.`, not two tokens meaning *for example*. Preserve an orthographic hyphen even in *re-establish* → `ríj-ɪstǽblɪʃ`; each transcribed element follows §5.3.
7. **Obvious misspellings:** transcribe the intended word (*woter* → `wɔ́tər`), keeping the 1:1 alignment. Never render a typo phonetically.
8. **Classify by meaning, then handle notation.** First decide from context whether a token is spoken English, a letter-name token, or symbolic material. Transcribe spoken English, including acronyms pronounced as words. Preserve symbolic material verbatim: equations, formulas, function calls, variables, units, chemical formulas, code, and identifiers. Case is preserved inside notation (`e`, `NaCl`, `camelCase`); the lowercase phonetic rule does not apply there. Capitalization and punctuation are clues, not decisive tests — the same spelling can require different treatment in different contexts.

| Context | Treatment | Why |
|---|---|---|
| *NASA launched it* | `nǽsə lɔ́ntʃt ɪt` | *NASA* is pronounced as an English word |
| *enter `NASA` as the identifier* | preserve `NASA` | the token is an identifier being referenced |
| *the sine is positive* | transcribe *sine* as `sájn` | the concept is expressed as an English word |
| *evaluate `sin(x)`* | preserve `sin(x)` | it is a function call |
| *use camel case* | transcribe the English words | the phrase names a convention in prose |
| *set `camelCase` to true* | preserve `camelCase` | it is a code identifier |
| *a program called fingerd* | `ə prówɡræ̀m kɔ́ld fingerd` | *fingerd* names the software identifier; do not partly phoneticize it as `fɪ́ŋɡərD` |

This classification is a semantic judgment for the transcriber or LLM; no token-shape rule can settle every case. The validator checks mechanical constraints after that decision but cannot prove that a token was correctly classified. In particular, `--text` has no source context, and its notation heuristics may not recognize every valid code or scientific token. Do not change a contextually correct transcription merely to satisfy a generic capitalization or character warning on a verbatim token; re-check the source meaning instead.

## 10. Encoding notes

- Primary stress = combining acute **U+0301**; secondary = combining grave **U+0300**, typed immediately after the vowel letter.
- For plain Latin vowels use the precomposed characters (matches existing data): `á é í ó ú` / `à è ì ò ù`.
- IPA letters take the combining mark directly after them: `ǽ` (`æ`+U+0301), `ɛ́ ɔ́ ɪ́ ʊ́ ə́ ɒ́ ɜ́ ɑ́` and grave counterparts `ɛ̀ ɔ̀ ɪ̀ ʊ̀ ə̀ æ̀ ɒ̀`.
- Always use IPA `ɡ` (U+0261), `ə` (U+0259), `ŋ` (U+014B), `ð` (U+00F0), `θ` (U+03B8), `ʃ` (U+0283), `ʒ` (U+0292).

## 11. Step-by-step procedure

1. Take the source sentence; lowercase it mentally but keep every punctuation mark and digit in place, except word-internal apostrophes in phonetic words (§5.4).
2. For each word, decide its **grammatical role**, then select the corresponding §6 form. Check particles vs. prepositions, determiner vs. independent/contrastive *some*, interrogative/exclamative vs. fused-relative *what*, determiner vs. independent *his*, pronouns used as independent answers, and lexical vs. auxiliary/modal uses. *All*, *not*, *do*, and demonstratives are always accented; conjunction/relative *that* stays weak. Copular and auxiliary *be*, and possessive determiners including *our*, stay weak by default; apply explicit contrast and clause-final strong-form rules where appropriate. For *the*, choose `ðə` before a consonant sound and `ðij` before a vowel sound. Special check for *have / has / had*: followed by a past participle → auxiliary, weak (`həv / həz / həd`); the only verb in the clause, or taking a direct object → main verb, accented (`hǽv / hǽz / hǽd`).
3. Classify each remaining token from context (§9): spoken English → retrieve its General American pronunciation; letter name → preserve as capitals and attach any pronounced `s` / `z` / `ɪz` suffix in lowercase; notation/code/identifier → preserve verbatim. For spoken English, when varieties disagree, GA wins (§1); for heteronyms like *record* or *use*, pick by part of speech (§8) — then map it into this notation:
   - long vowels/diphthongs → glide spellings (§4.2),
   - r-vowels → rhotic spellings (§4.3),
   - LOT → `ɒ`, PALM (long *ah*) → `ɑ`, THOUGHT/CLOTH → `ɔ` (§4.1), STRUT → `ə`,
   - reduced vowels → `ə`/`ɪ`/`ij` via the §4.4 tie-breaker (fixed morphemes, then spelling), suffixes per §7, yod per §4.6.
4. Mark stress: one acute per unhyphenated content word, including verbal particles, *all*, *not*, and demonstratives, on the first vowel symbol of the stressed syllable; in hyphenated compounds, apply this separately to each element. Apply the role-dependent forms, weak copular *be* exception, and fixed exceptions of §6. Use graves for secondary stresses and second elements of solid compounds (§5).
5. Reassemble with the original punctuation, spacing, and digits; omit word-internal apostrophes from phonetic words but preserve them in pass-through tokens and as quotation marks (§9).
6. **Self-check:**
   - No `ˈ ˌ ː eɪ oʊ aɪ aʊ ɔɪ iː uː ɜː ɑː ɹ g ᵻ ʌ` in phonetic material, and no `ɛər` / `ɪər` / `ʊər` sequences (they are `ɛr` / `ɪr` / `ʊr`). Verbatim notation and identifiers keep their original characters (§9).
   - Every unhyphenated content word and verbal particle has exactly one acute; *all*, *not*, and demonstratives always carry an acute. Weak monosyllables are bare, not every word listed in §6: check role-dependent, polysyllabic, strong, and fixed accented forms. Each content-word element of a hyphenated compound has its own acute (§5.3).
   - Re-check *some*, *what* (including contractions), *his*, independent pronoun answers, lexical homonyms of auxiliaries/modals, and particles against their source context. Do not accent *our* or copular *be* merely because the vowel is full or *be* is not an auxiliary; sentence-final pronouns are not automatically accented.
   - Every weak *the* matches the next sound: `ðə` before a consonant, `ðij` before a vowel (§6).
   - Every *have / has / had* re-checked: past participle follows it → weak auxiliary; direct object or only verb → accented main verb (§6).
   - Every `r` from the spelling that is pronounced is present.
   - No uppercase letters outside letter-name tokens (§9); digits untouched; punctuation identical to source except for omitted word-internal apostrophes.

### Machine-checkable constraints

Most of the guide's bans are regex-checkable. Phonetic material must have **zero matches** for every pattern below; verbatim notation and identifiers are exempt (§9):

| Pattern(s) | Catches |
|---|---|
| `[ˈˌː]` | IPA stress and length marks |
| `[ɹɾʔɫ]` | banned consonant allophones — use plain `r`, `t`, `l` |
| `[ʌᵻ]` | banned vowels — STRUT is `ə`, and `ᵻ` is never used |
| `g` | ASCII g — must be `ɡ` (U+0261) in phonetic material; preserve it in verbatim identifiers such as `fingerd` |
| `ɛər` `ɪər` `ʊər` | centering schwa before r — write `ɛr`, `ɪr`, `ʊr` |
| `eɪ` `əʊ` `oʊ` `aɪ` `aʊ` `ɔɪ` | traditional diphthong spellings — write `ej ow aj aw ɔj` |
| `[iuɜɑɔɒɛ]ː` | length-marked vowels |
| `ǽ` (U+01FD, precomposed) | NFC artifact — write `æ` + combining acute (U+0301) instead |

Checks that need tokenization rather than a single regex:

- `[A-Z]` matches are allowed only inside letter-name tokens (§9), including punctuated letter sequences such as `U.S.` and `E.G.`. An unpunctuated letter-name token may end in lowercase `s`, `z`, or `ɪz` when that is the regular plural or possessive allomorph selected by the final sound of its last letter name (`PDFs`, `USBz`, `Xɪz`).
   Letter names may also follow a phonetic word without a separator (`ówpənAI`, `ówpənAIz`); validate the phonetic component and letter-name component separately. This does not permit preserving a spoken word's source capitalization (`OpenAI`) or bypassing phonetic checks (`owpənAI`).
- Every combining accent (U+0301 / U+0300) must directly follow a vowel symbol (`a e i o u` arrive precomposed as `á é í ó ú`; `æ ɛ ɪ ɔ ɒ ʊ ə ɜ ɑ` take the combining mark).
- Within phonetic words, every Latin vowel base must have its required glide: `i` → `ij`, `u` → `uw`, `e` → `ej`, `o` → `ow`, `a` → `aj` or `aw`. The validator checks this after removing stress accents, so it also rejects accented traditional forms such as `méɪd`, `óʊn`, and `ɔ́ɪ`. Pass-through notation and letter-name tokens are exempt.
- A token with no accent must be a permitted §6 weak form, a digit/letter-name token, notation (§9), or punctuation. Bare `ɔl`, `nɒt`, `ðɪs`, `ðijz`, and `ðowz` are not permitted. Membership in the weak-form list permits a spelling, not every grammatical use of it: `əp / dawn / awt` remain valid prepositional forms, not particle forms; `wɒt / wɒts`, `səm`, `hɪz`, personal pronouns, and auxiliary/modal spellings each require the appropriate context.
- A phonetic word must contain no straight or curly apostrophe. Apostrophes remain valid as quotation punctuation and inside pass-through tokens such as `'70s`.
- Weak *the* must be `ðə` before a consonant sound and `ðij` before a vowel sound. The validator checks this when the next token is phonetic; pass-through digits, letter names, and notation require the transcriber to apply the sound test.
- In JSON mode, every source field must have a corresponding transcription, and `WrongAnswers` / `trans_WrongAnswers` arrays must have equal lengths.
- In JSON mode, source and transcription must have the same token count and exact whitespace runs. Within each paired token, digit sequences and the order of Unicode punctuation/symbol characters must match. Apostrophes are excluded from this layout comparison because phonetic words omit them (§5.4).

**Semantic limit:** validation cannot determine whether an ambiguous source token should be spoken or preserved as notation, nor whether a word is a particle, preposition, interrogative, relative, determiner, pronoun, lexical verb, or auxiliary. Those decisions must be made from context before validation (§6, §9). Both weak and accented spellings can pass mechanically while only one fits the source. Validator notation recognition is intentionally incomplete and must not override a clearly established code, identifier, formula, or other symbolic reading.

## 12. Worked examples

**Example 1 — weak forms and glide vowels**

> The floor lamp is typically tall and slender.

`ðə flɔ́r lǽmp ɪz tɪ́pɪkəlij tɔ́l ənd slɛ́ndər.`

**Example 2 — digits, contraction, wh-word, yod, CURE**

> What's the newest design from the 1980s that you'd wear during a cool autumn evening?

`wɒ́ts ðə núwəst dɪzájn frəm ðə 1980s ðət júwd wɛ́r dʊ́rɪŋ ə kúwl ɔ́təm íjvnɪŋ?`

**Example 3 — derivation walkthrough**

*associated* → syllables **ə**(unstressed) + **sów**(primary) + **sij**(glide link, §4.5) + **èj**(secondary, *-ate*) + **tɪd**(*-ed* after t) → `əsówsijèjtɪd`

*mathematical* → **mæ̀**(secondary) + **θə** + **mǽ**(primary) + **tɪ** + **kəl** → `mæ̀θəmǽtɪkəl`

**Example 4 — auxiliary vs. main verb**

> If I had had water, I would have shared it.

`ɪf aj həd hǽd wɔ́tər, aj wʊd həv ʃɛ́rd ɪt.`

The first *had* is the perfect auxiliary — weak `həd` (§6); the second is the main verb "possess" — strong `hǽd` with an acute.

**Example 5 — conjunction vs. demonstrative, *too* vs. *to***

> I realised that that was wrong, too late.

`aj ríjəlàjzd ðət ðǽt wəz rɔ́ŋ, túw léjt.`

The first *that* introduces the clause — weak `ðət`; the second is a demonstrative pronoun — strong `ðǽt`. The degree adverb *too* is a content word (`túw`), unlike the weak preposition *to* (`tə`).

**Example 6 — PALM, stressed ə, letter-names, heteronyms, clause-final strong form**

> My father used a USB drive to record the results — where does the money come from?

`maj fɑ́ðər júwzd ə USB drájv tə rɪkɔ́rd ðə rɪzə́lts — wɛ́r dəz ðə mə́nij kə́m frɒ́m?`

*father* takes long `ɑ` (§4.1); *used* and *record* are heteronyms resolved as verbs (`júwzd`, `rɪkɔ́rd`, §8); *USB* keeps its capitals (§9); *results*, *money*, *come* show stressed `ə́` for STRUT; and clause-final *from* takes its strong form `frɒ́m` (§6).

**Example 7 — particles, prepositions, and quantifiers**

> Some pieces were chipped. Some were fine. I lined them all up on the board.

`səm píjsɪz wər tʃɪ́pt. sə́m wər fájn. aj lájnd ðɛm ɔ́l ə́p ɒn ðə bɔ́rd.`

The determiner *some* is weak; independent *some* is accented. *All* and particle *up* carry acutes, while preposition *on* stays bare.

**Example 8 — grammatical roles, not full vowels**

> What did she do? She did what our friends needed. They are happy.

`wɒ́t dɪd ʃij dúw? ʃij dɪ́d wɒt awər frɛ́ndz níjdɪd. ðej ɑr hǽpij.`

The question uses interrogative *what* and auxiliary *did*. The answer uses lexical *did* and fused-relative *what* (= *the thing that*). Possessive *our* and copular *are* stay bare despite their full vowels.

**Example 9 — not, demonstratives, and independent possessives**

> These are not his books. This book is his.

`ðíjz ɑr nɒ́t hɪz bʊ́ks. ðɪ́s bʊ́k ɪz hɪ́z.`

Both demonstratives and *not* are accented by convention. Determiner *his* is weak before *books*; independent *his* is accented. Neither copular *be* form needs an acute.

**Example 10 — independent answer vs. sentence-final pronoun**

> Who did it? Me. I saw him.

`húw dɪd ɪt? míj. aj sɔ́ hɪm.`

The independent answer *me* is strong and accented; neutral object *him* stays weak even at the end of the sentence.

**Example 11 — modal vs. lexical homonym**

> They can buy a can. It is a must.

`ðej kən báj ə kǽn. ɪt ɪz ə mə́st.`

The first *can* is a weak modal; the second is an accented noun with its full vowel. Nominal *must* is also accented.

## 13. Common errors — never do these

| ❌ Wrong | ✅ Right | Why |
|---|---|---|
| `ˈleðər`, `ˌʌnˈlaɪk` | `lɛ́ðər`, `ə̀nlájk` | no ˈ ˌ marks; use acute/grave on the vowel |
| `meɪd`, `oʊnli`, `iːkwəl` | `méjd`, `ównlij`, `íjkwəl` | no length marks or traditional diphthongs |
| `lɛ́ðə`, `wɜ́ːld` | `lɛ́ðər`, `wɜ́rld` | the accent is rhotic — never drop r |
| `wɛ́ər`, `nɪ́ər`, `ðɛər` | `wɛ́r`, `nɪ́r`, `ðɛr` | no centering ə before r — SQUARE/NEAR are plain `ɛr` / `ɪr` |
| `pɛ́rəmàwnt` | `pǽrəmàwnt` | *paramount* has lexical TRAP before intervocalic `r`; the `ǽr` override applies before the M-W rule (§4.3) |
| `kʌ́lər`, `bʌt`, `sʌ́bkʌ̀ltʃər` | `kə́lər`, `bət`, `sə́bkə̀ltʃər` | `ʌ` is never used — STRUT is `ə` |
| `fɒ́ðər`, `kɒ́m`, `ɒ́mənd` | `fɑ́ðər`, `kɑ́m`, `ɑ́mənd` | PALM words have the long vowel — write `ɑ` (§4.1) |
| `aj́`, `ój` (accent on glide) | `áj`, `ɔ́j` | accent goes on the first vowel symbol |
| `gɑ́rmənt` with `g` | `ɡɑ́rmənt` | use IPA ɡ (U+0261) |
| `kwɑ́ntᵻtij` | `kwɑ́ntɪtij` | ᵻ is not part of this alphabet — use ɪ |
| `wɒt ɪz ðɪ́s?` | `wɒ́t ɪz ðɪ́s?` | interrogative *what* is accented; fused-relative *what* stays bare in *take what you need* |
| `ət ɔl` | `ət ɔ́l` | *all* is always accented |
| `nɒt rɛ́dij` | `nɒ́t rɛ́dij` | independent *not* always carries an acute, even when it is not the sentence focus |
| `ðɪs`, `ðijz`, `ðowz` | `ðɪ́s`, `ðíjz`, `ðówz` | demonstratives are accented in determiner and independent uses, like demonstrative *that* |
| `ðə bʊ́k ɪz hɪz` | `ðə bʊ́k ɪz hɪ́z` | independent possessive *his* is accented; determiner *his* remains weak in *his book* |
| `pʊ́t ɒn ə wɒ́tʃ` | `pʊ́t ɒ́n ə wɒ́tʃ` | particle *on* is accented; prepositional *on* stays weak in *rely on them* |
| `səm wər tʃɪ́pt` | `sə́m wər tʃɪ́pt` | independent *some* is accented; indefinite determiner *some* stays weak |
| `ʃij dɪd ðə wɜ́rk` | `ʃij dɪ́d ðə wɜ́rk` | lexical *did* is accented; auxiliary *did* stays weak by default |
| `ðə ǽpəl`, `ðij júwnɪt` | `ðij ǽpəl`, `ðə júwnɪt` | weak *the* follows the next sound, not the next letter (§6) |
| `ɪt's`, `wɛ́rər'z` | `ɪts`, `wɛ́rərz` | omit word-internal apostrophes from phonetic words (§5.4) |
| `Méjd`, `DƷɒn` | `méjd`, `dʒɒ́n` | lowercase everywhere except letter-name tokens |
| `usb`, `t-ʃɜ́rt` | `USB`, `T-ʃɜ́rt` | letter-read tokens are capitalized (§9) |
| `USBs`, `USB's`, `PDFz`, `Xs` | `USBz`, `USBz`, `PDFs`, `Xɪz` | letter-name suffixes are lowercase and follow the final pronounced sound (§9) |
| `íj = ɛ́m síj skwɛ́rd` for "e = mc^2" | `e = mc^2` | notation passes through verbatim (§9) |
| `túw dajmɛ́nʃənz` for "2 dimensions" | `2 dajmɛ́nʃənz` | digits stay as digits |
| accent on neutral `əv, ənd, tə, kən…` | bare weak forms | weak monosyllabic function words carry no accent; role-dependent, contrastive, and clause-final strong forms follow §6 |
| missing accent on `fíjl, méjd, wə́n…` | acute present | content monosyllables are always accented |
| `júws` for the verb *use*, `rɛ́kərd` for the verb *record* | `júwz`, `rɪkɔ́rd` | heteronyms — disambiguate by part of speech (§8) |
| `həz həd ə prəfáwnd ɪ́mpækt` | `həz hǽd ə prəfáwnd ɪ́mpækt` | the second *had* is a main verb (experienced), not an auxiliary — main-verb *have/has/had* carry stress (§6) |
| `əɡzǽmpəl`, `dəzájn`, `lǽŋɡwədʒ` | `ɪɡzǽmpəl`, `dɪzájn`, `lǽŋɡwɪdʒ` | the reduced prefixes *be-, de-, re-, pre-, se-, e-/ex-* and the ending *-age* take `ɪ` (§4.4) |
| `mɑ́rkɪtɪŋ`, `íjzəlij` | `mɑ́rkətɪŋ`, `íjzɪlij` | outside the fixed morphemes, weak `ɪ`~`ə` follows the spelling tie-breaker (§4.4) |
