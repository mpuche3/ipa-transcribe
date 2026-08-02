# English → IPA Transcription Guide

This document specifies how to transcribe English text into a learner-friendly, IPA-based phonetic notation. Follow it exactly: the goal is that any two transcribers (human or LLM) produce byte-identical output for the same input text.

## 1. Overview

The system is an **IPA-based respelling of rhotic (American-style) English** using **modern glide notation** (the style popularized by Dr. Geoff Lindsey): long vowels and diphthongs are written as vowel + glide (`ij, uw, ej, ow, aj, aw, ɔj`) instead of the traditional `iː, uː, eɪ, oʊ, aɪ, aʊ, ɔɪ`. Stress is marked with **accent marks placed on the vowel itself** — acute `´` for primary stress, grave `` ` `` for secondary stress — never with the IPA marks `ˈ ˌ`.

The text layout mirrors the source exactly: same words in the same order, same punctuation, all lowercase.

**Reference accent: General American.** Wherever varieties of English disagree — stress placement, vowel choice, yod, silent letters — follow the General American pronunciation (Merriam-Webster's first listing) and map it into this notation. One carve-out: in the weak `ɪ` ~ `ə` zone, where dictionaries contradict one another, the spelling tie-breaker of §4.4 decides — not the dictionary. Common traps:

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

1. Transcribe word by word; keep every punctuation mark, space, hyphen, apostrophe, digit, parenthesis, and quote exactly where it was.
2. Everything is lowercase — including proper nouns and sentence starts (*John* → `dʒɒ́n`). The only capitals allowed are letter-name tokens (rule 8).
3. Long vowels/diphthongs are vowel + glide: `ij uw ej ow aj aw ɔj`. Never use `ː`, `eɪ`, `oʊ`, etc. The one glide-less long vowel is `ɑ` (PALM: `fɑ́ðər`, `kɑ́m`).
4. The accent is rhotic: every written/underlying r is pronounced (`lɛ́ðər`, `wɜ́rld`, `ɡɑ́rmənt`).
5. No centering schwa before r: SQUARE = `ɛr` (`wɛ́r`), NEAR = `ɪr` (`nɪ́r`). And `ʌ` is never used — STRUT is written `ə`, stressed or not (`kə́lər`, `nə́mbər`).
6. Primary stress = acute on the first vowel symbol of the stressed syllable (`dʒǽkət`, `káwz`). Secondary stress = grave (`fʊ́twɛ̀r`, `mæ̀θəmǽtɪkəl`).
7. Content words always carry an accent — even monosyllables (`méjd`, `fíjl`). Function words appear in weak form with **no accent** (`əv`, `ənd`, `tə`, `ðə`, `kən`, `fɔr`).
8. Digits and years stay in written form (`2`, `1970s`, `'70s`); letters read by name stay as **capital** letters: `T-ʃɜ́rt`, `USB`. Equations, formulas, and units pass through verbatim: `e = mc^2`, `sin(x)`, `km/h` (§9).
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

- **No allophonic detail.** No flapping (*putting* → `pʊ́tɪŋ`, *water* → `wɔ́tər` — t stays t), no glottal stops `ʔ`, no dark l `ɫ`, no aspiration marks.
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

Splitting `ɒ` vs `ɑ` vs `ɔ` — **the length principle**: in this vowel area, write `ɑ` wherever the vowel tends to be **long**, and `ɒ` where it is short:

- `ɒ` = LOT words (short vowel): *hot, stop, top, body, object, problem, model, wash, watch, what, because* (`bəkɒ́z`).
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
| ajər / awər | fire / hour | `rəkwájər`, `ətájər`, `awər`, `páwər` |

Rules:

- **No r-vowel takes a centering `ə`.** Never write `ɛər`, `ɪər`, `ʊər`: *wear* `wɛ́r`, *near* `nɪ́r`, *sure* `ʃʊ́r`.
- DRESS + r and SQUARE are both plain `ɛr`: *very* `vɛ́rij`, *vary* `vɛ́rij`, *error* `ɛ́rər`, *care* `kɛ́r`, *area* `ɛ́rijə`.
- KIT + r and NEAR are both plain `ɪr`: *mirror* `mɪ́rər`, *spirit* `spɪ́rɪt`, *material* `mətɪ́rijəl`, *period* `pɪ́rijəd`.
- `æ` survives before intervocalic r: `kǽrəktər` (*character*), `kǽrij` (*carry*) — a deliberate exception to the M-W rule (§1): most GA speakers merge these into `ɛr` (*marry* = *merry*), and either pronunciation is fine.
- Unstressed NURSE/letter syllables are all plain `ər`: `sərprájz`, `pərhǽps`.

**Vowels before intervocalic r** (r between vowels inside a word):

| Write | Examples |
|---|---|
| ɛ́r | *very* `vɛ́rij`, *error* `ɛ́rər`, *parent* `pɛ́rənt` |
| ɪ́r | *mirror* `mɪ́rər`, *spirit* `spɪ́rɪt`, *serious* `sɪ́rijəs` |
| ǽr | *carry* `kǽrij`, *character* `kǽrəktər` — many GA speakers merge these into `ɛ́r`; either is fine |
| ɜ́r | *hurry* `hɜ́rij`, *courage* `kɜ́rədʒ`, *current* `kɜ́rənt` — STRUT + r merges into NURSE (no `ə́r` here) |
| ɒ́r | *borrow* `bɒ́row`, *sorry* `sɒ́rij`, *tomorrow* `təmɒ́row` |
| ɔ́r | *orange* `ɔ́rəndʒ`, *story* `stɔ́rij`, *glory* `ɡlɔ́rij` |

### 4.4 Weak (unstressed) vowels

| Symbol | Where | Examples |
|---|---|---|
| ə | any reduced vowel spelled with a letter other than i/y (tie-breaker below); endings *-al, -on, -an, -ous, -ment, -est, -age*; prefixes *a-, de-, re-, be-, pro-, con-, ex-/e-* (`əks`/`əɡz`) | `əbáwt`, `dəzájnd`, `rəméjnz`, `əɡzǽmpəl`, `dʒǽkət`, `mɑ́rkət`, `téjbəl`, `kɒ́tən` |
| ɪ | reduced vowels spelled with i or y (tie-breaker below); endings *-ing, -ic, -ity, -ish, -ify, -ible*; the fixed exceptions *-ed* `ɪd`, *-es* `ɪz`; prefixes *in-, im-, dis-* | `ríjdɪŋ`, `níjdɪd`, `wɒ́ʃɪz`, `àjkɒ́nɪk`, `dərəbɪ́lɪtij`, `prɒ́fɪt`, `stájlɪʃ` |
| ij | happY: final *-y, -ey, -ie*; *-ly*; before another vowel | `bɒ́dij`, `kówzij`, `lájklij`, `ɛ́rijə` |
| uw | unstressed GOOSE | `vǽljuw`, `ɪntuw` (*into* — function word, no accent) |
| ow | unstressed GOAT | `fɒ́low`, `ǽrowz`, `rɛ́trow` |

**The `ɪ` ~ `ə` tie-breaker.** Many reduced syllables could be `ɪ` or `ə` and both are correct — this is the zone some dictionaries mark with `ᵻ` and contradict each other on. Never use `ᵻ`; decide deterministically, in this order:

1. The §6 weak-form table and §7 suffix table win where they apply.
2. Fixed morphological exceptions, regardless of spelling: *-ed* → `ɪd` (`níjdɪd`), *-es* → `ɪz` (`wɒ́ʃɪz`).
3. Otherwise follow the **spelling** of the reduced vowel: **i or y → `ɪ`** (`prɒ́fɪt`, `mɛ́dɪsɪn`, `ǽnəlɪst`); **any other letter → `ə`** (`dʒǽkət`, `mɑ́rkət`, `əɡzǽmpəl`, `kɜ́rədʒ`, `ɔ́rəndʒ`, `mɪ́nət`).
4. Vowel digraphs default to `ə`: *mountain* `máwntən`, *captain* `kǽptən`, *foreign* `fɔ́rən`. When one letter of the digraph is silent, the sounded letter decides: *biscuit* `bɪ́skɪt`, *circuit* `sɜ́rkɪt` (the u is silent, as in *build*).

The rule touches only genuinely reduced vowels — happY `ij` (`bɒ́dij`) and stressed vowels are unaffected. Within this zone the spelling outranks dictionary notation (§1).

### 4.5 Glide linking inside words

When a syllable ending in `ij / ej / aj / ɔj` is followed by another vowel, link with `j`:

- *area* → `ɛ́rijə`, *various* → `vɛ́rijəs`, *material* → `mətɪ́rijəl`, *linear* → `lɪ́nijər`, *creation* → `krijéjʃən`, *associated* → `əsówsijèjtɪd`.

Sequences with `uw / ow / aw` before a vowel are left as-is (`fɒ́lowɪŋ`, `awər`); the *-ual* ending is written `wəl` (`vɪ́ʒwəl`, `kǽʒəwəl`).

### 4.6 Yod (/j/ before uw) — American yod-dropping

General American drops /j/ after coronal consonants; this style follows that rule:

- **No yod after t, d, n, s, z, l, θ, r** when the consonant starts the same syllable: `núw` (*new*), `dúw` (*due*), `túwn` (*tune*), `stúwdənt` (*student*), `núwmərəs` (*numerous*), `əsúwm` (*assume*), `rúwl` (*rule*), `ǽtɪtùwd` (*attitude*), `ǽvənùw` (*avenue*).
- **Keep yod after the other consonants** (p, b, m, f, v, k, ɡ, h): `pjʊ́r`, `bjúwtəfəl`, `mjúwzɪk`, `fjúw`, `vjúw`, `kjúwb`, `ɑ́rɡjəmənt`, `hjúwmən`.
- **Keep yod when it starts its own unstressed syllable**, even after a coronal: `vǽljuw` (*value*), `mɛ́njuw` (*menu*), `kəntɪ́njuw` (*continue*).
- Unstressed *-ture / -dual / -duate* coalesce: `néjtʃər`, `fɜ́rnɪtʃər`, `ɡrǽdʒuəl`, `ɛ̀dʒukéjʃən`-type words use `dʒ`.
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

- **Content words** (nouns, main verbs, adjectives, adverbs, numerals, interjections) always carry exactly one acute — including monosyllables: `méjd`, `fíjl`, `wɔ́rm`, `ǽd`, `tíj`, `wə́n`.
- **Function words** in their weak form get **no accent at all**, even when the vowel is a strong one: `æz`, `bət`, `nɒt`, `səm`, `ɔl`, `wɒt`, `majt`, `wʊd`, `ðijz`, `dawn` (particle), `əp`. See the table in §6.
- **Wh-question words are accented** (`wɪ́tʃ`, `wɛ́n`, `wɛ́r`, `húw`, `wáj`, `háw`) — **except *what*, which is always bare `wɒt`** (fixed exception in this style).
- A word never has more than one acute. Longer words add graves for secondary stresses: `mæ̀θəmǽtɪkəl`, `rɛ̀prəzɛ́ntɪd`, `əsówsijèjtɪd`, `vɜ̀rsətɪ́lɪtij`, `ə̀nlájk`.

### 5.3 Compounds

- **Solid compounds** (one written word): acute on the first element, grave on the second: `fʊ́twɛ̀r`, `bʊ́kʃɛ̀lf`, `nájtstæ̀nd`, `mówtərsàjkəl`, `sə́bkə̀ltʃər`, `wɜ́rldwàjd`.
- **Hyphenated compounds:** each element is transcribed and accented on its own, hyphen kept: `fríj-stǽndɪŋ`, `blúw-tɪ́ntɪd`, `wɔ́l-tə-wɔ́l`, `lɔ́ŋ-lǽstɪŋ`.
- Suffix-driven secondary stress: *-ate* verbs and *-ize* verbs take a grave on the suffix: `rɛ́ɡjəlèjt`, `vɪ́ʒwəlàjz`.

### 5.4 Contractions

- Keep the apostrophe exactly as written and transcribe around it.
- `ɪt's` (*it's*), `ɪts` (*its*), `wɛ́rər's` (*wearer's*) — possessive/`it`-contractions stay unaccented if the host word is unaccented.
- Pronoun + auxiliary contractions whose pronoun has a free vowel take an acute: `ðéjv` (*they've*), `ðɛ́r` (*they're*), `júwr` (*you're*), `wíjr` (*we're*), `ájl` (*I'll*).
- Negative contractions are content-like and accented: `dównt`, `kǽnt`, `wównt`, `ɪ́zənt`.

## 6. Weak forms of function words (reference)

Use these forms, unaccented, whenever the word is a function word in running text. (Strong/accented forms are only for genuine emphasis or when the word is cited as a word — rare in ordinary prose.)

| Category | Forms |
|---|---|
| Articles | *a* `ə` · *an* `ən` · *the* `ðə` (also before vowels) |
| Conjunctions | *and* `ənd` · *or* `ɔr` · *but* `bət` · *if* `ɪf` · *as* `æz` · *than* `ðən` · *that* (conj./relative) `ðət` |
| Prepositions | *of* `əv` · *to* `tə` (also before vowels: `tə ǽd`) · *in* `ɪn` · *on* `ɒn` · *at* `ət` · *by* `baj` · *for* `fɔr` · *from* `frəm` · *with* `wɪð` |
| Particles | *up* `əp` · *down* `dawn` · *out* `awt` (as particle) |
| Pronouns | *I* `aj` · *you* `juw` · *he* `hij` · *she* `ʃij` · *it* `ɪt` · *we* `wij` · *they* `ðej` · *me* `mij` · *him* `hɪm` · *her* `hər` · *us* `əs` · *them* `ðɛm` |
| Possessives | *my* `maj` · *your* `jɔr` · *his* `hɪz` · *its* `ɪts` · *our* `awər` · *their* `ðɛr` |
| Demonstratives | *this* `ðɪs` · *these* `ðijz` · *that* (det.) `ðǽt` · *those* `ðowz` |
| *be* | *am* `əm` · *is* `ɪz` · *are* `ɑr` · *was* `wəz` · *were* `wər` · *be* `bij` · *been* `bɪn` |
| *have* | *have* `həv` · *has* `həz` · *had* `həd` — as auxiliaries (followed by a past participle). Main-verb *have / has / had* — possession, experience, consumption, any lexical meaning — are content words: *I have a car* → `aj hǽv ə kɑ́r`; *she has had breakfast* → `ʃij həz hǽd brɛ́kfəst`; *we had a great time* → `wij hǽd ə ɡréjt tájm`. Obligation *have to / has to* devoice: `hǽf tə`, `hǽs tə`. (See Example 4.) |
| *do* | *do* `dúw` (always accented) · *does* `dəz` · *did* `dɪd` |
| Modals | *can* `kən` · *could* `kʊd` · *will* `wɪl` · *would* `wʊd` · *shall* `ʃəl` · *should* `ʃʊd` · *may* `mej` · *might* `majt` · *must* `məst` |
| Other | *not* `nɒt` · *some* `səm` · *all* `ɔl` · *there* (existential) `ðər`; locative *there* is content: `ðɛ́r` · *what* `wɒt` |

Quantifiers/adverbs like *any* `ɛ́nij`, *every* `ɛ́vrij`, *both* `bówθ`, *each* `íjtʃ`, *only* `ównlij`, *very* `vɛ́rij`, *well* `wɛ́l`, *still* `stɪ́l`, *just* `dʒə́st` count as **content words** and are accented.

**Strong forms at clause ends:** a function word stranded at the end of a clause — a preposition with no following complement, or a final auxiliary — takes its strong, accented form: *what are you looking at?* → `wɒt ɑr juw lʊ́kɪŋ ǽt?`; *where do you come from?* → `wɛ́r dúw juw kə́m frɒ́m?`; *yes, it is.* → `jɛ́s, ɪt ɪ́z.` Strong forms: *at* `ǽt`, *of* `ɒ́v`, *to* `túw`, *for* `fɔ́r`, *from* `frɒ́m`, *is* `ɪ́z`, *are* `ɑ́r`, *was* `wɒ́z`, *has* `hǽz`, *can* `kǽn`, *have* `hǽv`, *would* `wʊ́d`.

## 7. Suffix cheat sheet

| Spelling | Transcription | Example |
|---|---|---|
| -ing | `ɪŋ` | `ríjdɪŋ` |
| -ed | `t` / `d` / `ɪd` | `dréjpt`, `tǽnd`, `níjdɪd` |
| -s / -es | `s` / `z` / `ɪz` | `bʊ́ks`, `káwz`, `wɒ́ʃɪz` |
| -y / -ies | `ij` / `ijz` | `bɒ́dij`, `æktɪ́vɪtijz` |
| -ly / -ally / -ily | `lij` / `əlij` / `ɪlij` | `lájklij`, `tɪ́pɪkəlij`, `íjzɪlij` |
| -er / -or / -est | `ər` / `ər` / `əst` | `kúwlər`, `vɛ́ktər`, `sɪ́mpləst` |
| -ity / -ities | `ɪtij` / `ɪtijz` | `dərəbɪ́lɪtij`, `kwɑ́ntɪtijz` |
| -age | `ədʒ` | `kɜ́rədʒ`, `bɛ́vrədʒ`, `lǽŋɡwədʒ` |
| -tion / -ssion | `ʃən` | `krijéjʃən`, `dɪskə́ʃən` |
| -sion (voiced) | `ʒən` | `dəsɪ́ʒən`, `vɜ́rʒən` |
| -ture / -sure | `tʃər` / `ʒər` | `fɜ́rnɪtʃər`, `mɛ́ʒər` |
| -able / -ible | `əbəl` / `ɪbəl` | `dʊ́rəbəl`, `ɪnkrɛ́dɪbəl` |
| -ous / -al / -ful / -less / -ness | `əs` / `əl` / `fəl` / `ləs` / `nəs` | `rəbɛ́ljəs`, `nǽtʃərəl`, `júwsfəl`, `tájmləs`, `kówzijnəs` |
| -ment / -ent / -ant / -ence / -ance | `mənt` / `ənt` / `ənt` / `əns` / `əns` | `stéjtmənt`, `dɪ́fərənt`, `ɪmpɔ́rtənt`, `dɪ́fərəns` |
| -ate (verb, 3+ syllables) | `èjt` | `rɛ́ɡjəlèjt`, `əsówsijèjt` |
| -ate (noun/adj.) | `ət` | `dɪlɪ́bərət` |
| -ize / -ized | `àjz` / `àjzd` | `vɪ́ʒwəlàjz`, `vɪ́ʒwəlàjzd` |
| -ic / -ical | `ɪk` / `ɪkəl` | `àjkɒ́nɪk`, `tɪ́pɪkəl` |
| -ism / -ist | `ɪzəm` / `ɪst` | `ríjəlɪzəm`, `ɑ́rtɪst` |

Two-syllable *-ate* verbs carry the **primary** stress on the suffix instead — no grave: `krijéjt` (*create*), `rəléjt` (*relate*).

## 8. Heteronyms — same spelling, two pronunciations

Disambiguate by part of speech (or tense) from context **before** transcribing:

| Spelling | One reading | The other |
|---|---|---|
| record | noun `rɛ́kərd` | verb `rəkɔ́rd` |
| present | noun/adj. `prɛ́zənt` | verb `prəzɛ́nt` |
| object | noun `ɒ́bdʒɛkt` | verb `əbdʒɛ́kt` |
| use | noun `júws` | verb `júwz` |
| close | adj. `klóws` | verb `klówz` |
| live | adj. `lájv` | verb `lɪ́v` |
| read | present `ríjd` | past/participle `rɛ́d` |
| lead | verb / leash `líjd` | the metal `lɛ́d` |
| minute | time unit `mɪ́nət` | tiny `majnúwt` |

The list is not exhaustive — any noun/verb pair with shifting stress (*permit, conduct, increase, project, contract…*) follows the *record* pattern: the noun stresses the first syllable, the verb the second.

Related but grammar-driven rather than spelling-driven: *have / has / had*, *that*, *there*, and *do* switch between weak and accented forms by syntactic role — see §6.

## 9. Text formatting rules

1. **Lowercase everything** — sentence-initial words, proper nouns, acronym-derived words: *John* → `dʒɒ́n`. The single exception is capital letters in letter-name tokens (rule 5).
2. **Preserve all punctuation and spacing** exactly: `. , ? ! ; : ( ) ' " -` and any others. One source word → one transcribed token in the same position.
3. **Apostrophes stay**: `ɪt's`, `wɛ́rər's`, `dównt`.
4. **Digits, years, decades, and numbers stay as written**: `2`, `100`, `1970s`, `'70s`. Do not spell them out phonetically.
5. **Letters read by name stay as CAPITAL letters.** Since capitals occur nowhere else in a transcription, an uppercase letter is the unambiguous signal "say this letter's name": *T-shirt* → `T-ʃɜ́rt`, *X-ray* → `X-réj`, *USB* → `USB`, *AI* → `AI`. Acronyms pronounced as words are ordinary words — fully phonetic and lowercase (*NASA* → `nǽsə`, *laser* → `léjzər`).
6. **Never insert or delete words.** The transcription must align 1:1 with the source text.
7. **Obvious misspellings:** transcribe the intended word (*woter* → `wɔ́tər`), keeping the 1:1 alignment. Never render a typo phonetically.
8. **Notation passes through verbatim** — equations, formulas, function names, variables, units, chemical formulas, code: *e = mc^2* → `e = mc^2`, *sin(x)* → `sin(x)`, *km/h* → `km/h`, *H2O* → `H2O`. Case is preserved inside notation (`e` stays lowercase — the capitals rule applies only to letter names in prose, like `T-ʃɜ́rt`). When the source spells the concept as an English word, transcribe it: *sine* → `sájn`, *equals* → `íjkwəlz`, *squared* → `skwɛ́rd`. Test: if you would have to decide how to read it aloud, it is notation — leave it exactly as written.

## 10. Encoding notes

- Primary stress = combining acute **U+0301**; secondary = combining grave **U+0300**, typed immediately after the vowel letter.
- For plain Latin vowels use the precomposed characters (matches existing data): `á é í ó ú` / `à è ì ò ù`.
- IPA letters take the combining mark directly after them: `ǽ` (`æ`+U+0301), `ɛ́ ɔ́ ɪ́ ʊ́ ə́ ɒ́ ɜ́ ɑ́` and grave counterparts `ɛ̀ ɔ̀ ɪ̀ ʊ̀ ə̀ æ̀ ɒ̀`.
- Always use IPA `ɡ` (U+0261), `ə` (U+0259), `ŋ` (U+014B), `ð` (U+00F0), `θ` (U+03B8), `ʃ` (U+0283), `ʒ` (U+0292).

## 11. Step-by-step procedure

1. Take the source sentence; lowercase it mentally but keep every punctuation mark and digit in place.
2. For each word, decide: **function word?** → copy its weak form from §6, unaccented. Special check for *have / has / had*: followed by a past participle → auxiliary, weak (`həv / həz / həd`); the only verb in the clause, or taking a direct object → main verb, accented (`hǽv / hǽz / hǽd`).
3. Otherwise, retrieve the word's General American pronunciation — when varieties disagree, GA wins (§1); for heteronyms like *record* or *use*, pick by part of speech (§8) — then map it into this notation:
   - long vowels/diphthongs → glide spellings (§4.2),
   - r-vowels → rhotic spellings (§4.3),
   - LOT → `ɒ`, PALM (long *ah*) → `ɑ`, THOUGHT/CLOTH → `ɔ` (§4.1), STRUT → `ə`,
   - reduced vowels → `ə`/`ɪ`/`ij` via the spelling tie-breaker (§4.4), suffixes per §7, yod per §4.6.
4. Mark stress: one acute per content word on the first vowel symbol of the stressed syllable; graves for secondary stresses and second elements of solid compounds (§5).
5. Reassemble with the original punctuation, spacing, digits, and apostrophes.
6. **Self-check:**
   - No `ˈ ˌ ː eɪ oʊ aɪ aʊ ɔɪ iː uː ɜː ɑː ɹ g ᵻ ʌ` anywhere (letter-name tokens are uppercase, so a lowercase `g` is always wrong), and no `ɛər` / `ɪər` / `ʊər` sequences (they are `ɛr` / `ɪr` / `ʊr`).
   - Every content word has exactly one acute; every function word from §6 has none.
   - Every *have / has / had* re-checked: past participle follows it → weak auxiliary; direct object or only verb → accented main verb (§6).
   - Every `r` from the spelling that is pronounced is present.
   - No uppercase letters outside letter-name tokens (§9); digits untouched; punctuation identical to source.

### Machine-checkable constraints

Most of the guide's bans are regex-checkable. A valid transcription must have **zero matches** for every pattern below (run them over the transcribed string only):

| Pattern(s) | Catches |
|---|---|
| `[ˈˌː]` | IPA stress and length marks |
| `[ɹɾʔɫ]` | banned consonant allophones — use plain `r`, `t`, `l` |
| `[ʌᵻ]` | banned vowels — STRUT is `ə`, and `ᵻ` is never used |
| `g` | ASCII g — must be `ɡ` (U+0261); letter-name tokens are uppercase, so lowercase `g` is never valid |
| `ɛər` `ɪər` `ʊər` | centering schwa before r — write `ɛr`, `ɪr`, `ʊr` |
| `eɪ` `əʊ` `oʊ` `aɪ` `aʊ` `ɔɪ` | traditional diphthong spellings — write `ej ow aj aw ɔj` |
| `[iuɜɑɔɒɛ]ː` | length-marked vowels |
| `wɒ́t` | *what* must be bare `wɒt` |
| `ǽ` (U+01FD, precomposed) | NFC artifact — write `æ` + combining acute (U+0301) instead |

Checks that need tokenization rather than a single regex:

- `[A-Z]` matches are allowed only inside letter-name tokens (§9).
- Every combining accent (U+0301 / U+0300) must directly follow a vowel symbol (`a e i o u` arrive precomposed as `á é í ó ú`; `æ ɛ ɪ ɔ ɒ ʊ ə ɜ ɑ` take the combining mark).
- A token with no accent must be a §6 weak form, a digit/letter-name token, notation (§9), or punctuation.
- The token count must equal the source text's token count.

## 12. Worked examples

**Example 1 — weak forms and glide vowels**

> The floor lamp is typically tall and slender.

`ðə flɔ́r lǽmp ɪz tɪ́pɪkəlij tɔ́l ənd slɛ́ndər.`

**Example 2 — digits, contraction, wh-word, yod, CURE**

> What's the newest design from the 1980s that you'd wear during a cool autumn evening?

`wɒt's ðə núwəst dəzájn frəm ðə 1980s ðət júwd wɛ́r dʊ́rɪŋ ə kúwl ɔ́təm íjvnɪŋ?`

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

`maj fɑ́ðər júwzd ə USB drájv tə rəkɔ́rd ðə rəzə́lts — wɛ́r dəz ðə mə́nij kə́m frɒ́m?`

*father* takes long `ɑ` (§4.1); *used* and *record* are heteronyms resolved as verbs (`júwzd`, `rəkɔ́rd`, §8); *USB* keeps its capitals (§9); *results*, *money*, *come* show stressed `ə́` for STRUT; and clause-final *from* takes its strong form `frɒ́m` (§6).

## 13. Common errors — never do these

| ❌ Wrong | ✅ Right | Why |
|---|---|---|
| `ˈleðər`, `ˌʌnˈlaɪk` | `lɛ́ðər`, `ə̀nlájk` | no ˈ ˌ marks; use acute/grave on the vowel |
| `meɪd`, `oʊnli`, `iːkwəl` | `méjd`, `ównlij`, `íjkwəl` | no length marks or traditional diphthongs |
| `lɛ́ðə`, `wɜ́ːld` | `lɛ́ðər`, `wɜ́rld` | the accent is rhotic — never drop r |
| `wɛ́ər`, `nɪ́ər`, `ðɛər` | `wɛ́r`, `nɪ́r`, `ðɛr` | no centering ə before r — SQUARE/NEAR are plain `ɛr` / `ɪr` |
| `kʌ́lər`, `bʌt`, `sʌ́bkʌ̀ltʃər` | `kə́lər`, `bət`, `sə́bkə̀ltʃər` | `ʌ` is never used — STRUT is `ə` |
| `fɒ́ðər`, `kɒ́m`, `ɒ́mənd` | `fɑ́ðər`, `kɑ́m`, `ɑ́mənd` | PALM words have the long vowel — write `ɑ` (§4.1) |
| `aj́`, `ój` (accent on glide) | `áj`, `ɔ́j` | accent goes on the first vowel symbol |
| `gɑ́rmənt` with `g` | `ɡɑ́rmənt` | use IPA ɡ (U+0261) |
| `kwɑ́ntᵻtij` | `kwɑ́ntɪtij` | ᵻ is not part of this alphabet — use ɪ |
| `wɒ́t`, `ðij` | `wɒt`, `ðə` | *what* and *the* are always bare weak forms |
| `Méjd`, `DƷɒn` | `méjd`, `dʒɒ́n` | lowercase everywhere except letter-name tokens |
| `usb`, `t-ʃɜ́rt` | `USB`, `T-ʃɜ́rt` | letter-read tokens are capitalized (§9) |
| `íj = ɛ́m síj skwɛ́rd` for "e = mc^2" | `e = mc^2` | notation passes through verbatim (§9) |
| `túw dajmɛ́nʃənz` for "2 dimensions" | `2 dajmɛ́nʃənz` | digits stay as digits |
| accent on `əv, ənd, tə, kən…` | bare weak forms | function words carry no accent |
| missing accent on `fíjl, méjd, wə́n…` | acute present | content monosyllables are always accented |
| `júws` for the verb *use*, `rɛ́kərd` for the verb *record* | `júwz`, `rəkɔ́rd` | heteronyms — disambiguate by part of speech (§8) |
| `həz həd ə prəfáwnd ɪ́mpækt` | `həz hǽd ə prəfáwnd ɪ́mpækt` | the second *had* is a main verb (experienced), not an auxiliary — main-verb *have/has/had* carry stress (§6) |
| `ɪɡzǽmpəl`, `mɑ́rkɪtɪŋ`, `íjzəlij` | `əɡzǽmpəl`, `mɑ́rkətɪŋ`, `íjzɪlij` | weak `ɪ`~`ə` vowels follow the spelling tie-breaker (§4.4) |
