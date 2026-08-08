# Design Choices

This document explains the deliberate decisions behind the transcription system in [transcription_guide.md](transcription_guide.md) — and, for each, the alternatives that would also have been defensible. The guide says *what* to write; this file says *why*.

Three goals drove every choice, in priority order:

1. **Determinism** — two transcribers (human or LLM) following the guide must produce byte-identical output. Any rule that requires taste is a bug.
2. **Learner legibility** — the notation should be readable with minimal training, visually close to ordinary text, and free of clutter.
3. **Phonemic honesty about General American** — the system encodes the sound distinctions a GA speaker actually uses in connected speech, at the phoneme level, not below it.

When goals conflicted, the earlier one won.

## The overarching stance: broad, not narrow

**Chosen:** phonemic (broad) transcription — one symbol per distinctive sound.

**Also valid:** narrow phonetic transcription with allophonic detail: flapped [ɾ] in *water*, glottal [ʔ] in *button*, dark [ɫ] in *feel*, aspiration [tʰ].

**Why:** allophones are rule-governed — a reader who knows the rules can always add them, and a learner is better served by the underlying map than by surface noise. Narrow detail roughly doubles the symbol inventory and makes visually different transcriptions of what learners should perceive as one sound. This single decision cascades into several bans: no `ɾ`, no `ɫ`, no `ʔ`, no aspiration marks — `t` stays `t` in `wɔ́tər`.

## Vowels

### Glide notation: `ij uw ej ow aj aw ɔj`

**Chosen:** vowel + glide, after Geoff Lindsey's analysis (his CUBE notation for British English uses `ɪj ʉw ɛj ʌw`; this system simplifies the base letters for General American).

**Also valid:** the Gimson tradition used by most dictionaries (`iː uː eɪ oʊ aɪ aʊ ɔɪ`); or bare `i u e o` as in many American textbooks.

**Why:** the glide is real — and writing it makes linking fall out mechanically (`krijéjʃən`, `ɛ́rijə`) instead of needing extra rules. It warns learners (especially Spanish speakers) off pure monophthongs [i e o u]. And it eliminates the length mark `ː` entirely — one more piece of clutter gone.

### `ə` for STRUT

**Chosen:** one symbol for *cup* and *about*; stress carries the difference (`kə́lər`, `lə́v`).

**Also valid:** traditional `ʌ`, kept distinct in RP-descended notation and most textbooks.

**Why:** in GA the two vowels differ by stress far more than by quality — Merriam-Webster itself writes *color* as \ˈkə-lər\. One symbol removes a distinction learners cannot reliably hear in American speech, and frees `ʌ` to serve as an unambiguous error signal in validation.

### The `ɒ` / `ɑ` / `ɔ` area

**Chosen:** a three-way split: short `ɒ` (LOT), long `ɑ` (PALM, START, the *qua-* family), `ɔ` (THOUGHT + CLOTH) — the "length principle," with no length marks.

**Also valid:** pure GA two-way (`ɑ` for merged LOT=PALM, `ɔ` for THOUGHT); merger-maximal one-way (`ɑ` for everything, cot = caught); RP-style `ɒ / ɑː / ɔː`.

**Why:** the split is descriptive without resorting to `ː`, and it preserves information the reader can freely discard: pronouncing `ɒ` identically to `ɑ` yields ordinary GA; keeping them apart yields a more conservative accent. A documented reader's choice, not a prescription.

### `ɪ` or `ə` by morpheme, then spelling — instead of `ᵻ`

**Chosen:** in the weak-vowel gray zone, fixed morphemes decide first: the word-initial reduced prefixes *be-, de-, re-, pre-, se-, e-/ex-* and the endings *-ed, -es, -age, -ange* take `ɪ` (`bɪkɒ́z`, `dɪzájn`, `rɪméjnz`, `ɪkspɛ́rɪmənt`, `lǽŋɡwɪdʒ`, `ɔ́rɪndʒ`). Everywhere else, spelling decides: i/y → `ɪ`, any other letter → `ə`.

**Also valid:** the OED/Longman `ᵻ` (honest about the variability, but it defers the decision to the reader); always `ə` (full weak-vowel merger); pure spelling with no morpheme layer (this system's original rule — mechanical, but it forced `ə` into *because, before, design, language*, contradicting Merriam-Webster in some of the most frequent words in English); or following one dictionary's notation (they contradict each other precisely here).

**Why:** determinism without betraying the reference accent. M-W's first listings have \i\ in exactly these prefixes and in *-age/-ange*, and unmerged American speakers produce `ɪ` there; promoting that closed morpheme list above the spelling rule keeps the answer fully mechanical — no lookup, no taste — while fixing the words where the pure-spelling rule audibly misfired. Outside the list, the spelling rule still gives a mechanical answer and visually anchors the transcription to the written word.

### Parenthesized schwas are dropped (syncope)

**Chosen:** when M-W's first listing parenthesizes a medial schwa, it is not written: `dɪ́frənt`, `sɒ́vrən`, `lǽbrətɔ̀rij`. Unparenthesized full forms keep it: `nǽtʃərəl`. The fixed §6/§7 tables outrank the rule, so suffix transcriptions like *-ally* `əlij` stay stable.

**Also valid:** always writing the full form (citation style, closer to the spelling); or a lookup-free phonological rule (drop post-stress schwa before r/l/n), which would however contradict M-W where it lists the full form first (*natural*).

**Why:** connected speech is the point. The compressed forms are what GA speakers actually produce; writing the schwa invites learners to restore a syllable natives skip. The M-W parenthesis makes the call deterministic — the same single authority the system already leans on.

### happY as `ij`

**Chosen:** `bɒ́dij`, `lájklij`.

**Also valid:** `i` (the dictionary "happy-tensing" symbol) or `ɪ` (older RP tradition).

**Why:** final -y is tense in GA — the FLEECE vowel — and reusing `ij` keeps the inventory smaller.

## Vowels before r

### `ɛr ɪr ʊr` — no centering schwa

**Chosen:** `wɛ́r`, `nɪ́r`, `ʃʊ́r`.

**Also valid:** `ɛər ɪər ʊər` — the RP-lineage spelling that mirrors non-rhotic centering diphthongs.

**Why:** in rhotic GA there is no centering glide; the `ə` was an artifact of describing non-rhotic accents. Dropping it saves a symbol per word and is phonemically truthful. A consequence worth owning: DRESS/SQUARE and KIT/NEAR merge before r — which GA has anyway (*very* = *vary*; *mirror* rhymes with *nearer*).

### `ər ɜr` — not hooked `ɚ ɝ`

**Chosen:** plain vowel + r sequences.

**Also valid:** the r-colored symbols `ɚ ɝ` (Kenyon & Knott and much American linguistics); syllabic `r̩`.

**Why:** two fewer exotic glyphs, decomposable for search and validation, consistent with the `ɑr ɔr ɛr ɪr` pattern — and it is what Merriam-Webster prints (\ˈwərd\).

### `ǽr` kept in *carry / marry*

**Chosen:** `kǽrij`, `kǽrəktər`, as a labeled exception to the Merriam-Webster rule.

**Also valid:** merging into `ɛr`, which is what most GA speakers do (M-W prints \ˈker-ē\).

**Why:** reader's choice again — no confusion is possible in either direction, and keeping `ǽr` preserves the distinction for speakers who have it. One of the three documented departures from pure GA.

## Consonants

### `r`, not `ɹ`

**Also valid:** `ɹ` is the phonetically correct IPA letter for the English approximant.

**Why:** with no trill in the language there is no contrast to protect; every dictionary writes `r`; learners read it instantly. `ɹ` buys precision nobody needs at the cost of alienness — and banning it gives the validator another error signal.

### `tʃ dʒ` as two characters

**Also valid:** the deprecated ligatures `ʧ ʤ`; Americanist `č ǰ`.

**Why:** current IPA practice, better font support, and the components are truthful — *church* really does begin with a t-like closure into ʃ.

### `j` and `w` doing double duty

**Chosen:** `j` = the *y* consonant **and** the front offglide; `w` = the *w* consonant **and** the back offglide.

**Also valid:** dedicated offglide symbols (`ɪ̯ ʊ̯`), or Americanist `y` for yod.

**Why:** the offglide and the consonant are the same gesture, so one letter each keeps the whole system resting on a single insight. Using `y` for yod would collide with English spelling intuitions about y-as-vowel.

### `ɡ` (U+0261), never ASCII `g`

**Why:** the IPA letterform is unambiguous, and reserving ASCII `g` as always-an-error makes machine validation trivially strict. Lowercase ASCII `c q x y` are likewise banned from phonetic material for the same reason.

## Stress

### Accent marks on the vowel — not `ˈ ˌ`

**Chosen:** acute = primary (`dʒǽkət`), grave = secondary (`mæ̀θəmǽtɪkəl`), on the first vowel symbol of the nucleus.

**Also valid:** IPA `ˈ ˌ` before the syllable; dictionary primes after the syllable; Trager–Smith-style multi-level accent systems.

**Why:** three reasons. Learners who know Spanish or Greek orthography read vowel accents natively. The mark sits exactly where the prominence is, rather than floating in the string. And — decisive for the determinism goal — `ˈ` placement requires deciding where syllables *begin*, an entire class of judgment calls (`con.trol` or `cont.rol`?) that vowel-attached accents never raise.

### Weak forms are transcribed

**Chosen:** function words appear as actually spoken in running text — `əv, tə, ðə / ðij, həz` — with strong forms at clause ends and a fixed table (§6) for determinism. Weak *the* is `ðə` before a consonant sound and `ðij` before a vowel sound; the choice follows pronunciation rather than spelling (`ðə jùwnəvɜ́rsətij`, `ðij áwər`).

**Also valid:** citation forms throughout, which is what dictionaries show; or invariant weak `ðə`, reflecting the considerable variation in spontaneous American speech.

**Why:** connected speech is the point. Rhythm and reduction are where learners' comprehension fails, and a transcription of sentences (rather than isolated words) should show the sentence phonology. The familiar `ðə` / `ðij` alternation gives learners a deterministic way to avoid vowel hiatus, even though native usage is not categorical. Bareness (no accent) is the written signal of weakness — but only for monosyllables: a polysyllabic function word keeps its word-internal acute (`ɪ́ntə`, `əbáwt`), because there the mark locates the stressed syllable, information a bare form would destroy (and `ə` is stressable in this system, so it is not recoverable).

## Text conventions

### Word-internal apostrophes are omitted

**Chosen:** contractions, possessives, and names are transcribed as single phonetic words without their spelling apostrophe: `ɪts` (*it's*), `wɛ́rərz` (*wearer's*), `ðéjv` (*they've*), `owkɒ́nər` (*O'Connor*). Apostrophes remain only when they are quotation punctuation or part of a pass-through token such as `'70s`.

**Also valid:** preserving the source apostrophe inside every transcription.

**Why:** an apostrophe has no sound, and contractions such as *they're* (`ðɛ́r`) provide no phonologically meaningful place to put one. Omitting it makes the output deterministic and matches the system's broad-phonemic stance. Word-level alignment is unchanged: each contraction is still one token.

### All lowercase; capitals mean "say the letter name"

**Also valid:** preserving source capitalization; bracketing spelled-out tokens.

**Why:** case carries no sound, so freeing it creates a clean channel: any capital is unambiguously a letter-name token (`USB`, `T-ʃɜ́rt`). Preserving capitalization would make *A* (the word) and *A* (the letter) collide.

### Digits, formulas, and notation pass through

**Also valid:** spelling everything out (`1970s` → `nàjntijn sɛ́vəntijz`).

**Why:** notation has multiple valid readings; expanding it breaks 1:1 token alignment with the source and injects guesses. The test in the guide: if you would have to decide how to read it aloud, it stays as written.

### Combining accents (`æ` + U+0301), precomposed only for `á é í ó ú`

**Also valid:** full NFC normalization — a single code point (U+01FD) for æ-acute.

**Why:** it matches the existing corpus byte-for-byte and keeps "accent" a separable, checkable layer on top of "letter." The cost is real — many toolchains silently NFC-normalize — so the validator polices it and the README documents the one-line repair.

## Reference accent

### General American, Merriam-Webster first listing

**Also valid:** RP/SSB (Lindsey's own CUBE target — ironically, the glide notation's home accent); a fully merger-maximal GA; or accent-agnostic notation.

**Why:** GA is the accent most learners target and most media exposes them to, and M-W's first listing supplies a single deterministic authority for everything outside the weak `ɪ`~`ə` zone (where the morpheme-then-spelling tie-breaker rules). The three documented departures — `ɒ`/`ɑ`, `ǽr`, unwritten flapping — all *preserve optionality* rather than contradict GA: each keeps a distinction in writing that the reader may merge in speech.

---

*If you disagree with a choice here, the guide's machine-checkable constraints (§11) make it safe to fork: change the rule, update the validator to match, and your corpus stays internally consistent.*
