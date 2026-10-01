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

**Chosen:** a three-way split: short `ɒ` (LOT), long `ɑ` (PALM, START, the *qua-* family), long `ɔ` (THOUGHT + CLOTH) — the "length principle," with no length marks. The vowel inventory groups `ɑ` and `ɔ` as **long monophthongs (no glide)**, separately from short monophthongs and glide vowels. These are pedagogical categories within this notation, not a claim of fixed duration across American accents or phonetic contexts.

**Also valid:** pure GA two-way (`ɑ` for merged LOT=PALM, `ɔ` for THOUGHT); merger-maximal one-way (`ɑ` for everything, cot = caught); RP-style `ɒ / ɑː / ɔː`.

**Why:** the split is descriptive without resorting to `ː`, and it preserves information the reader can freely discard: pronouncing `ɒ` identically to `ɑ` yields ordinary GA; keeping them apart yields a more conservative accent. A documented reader's choice, not a prescription.

### `ɪ` or `ə` by morpheme, then spelling — instead of `ᵻ`

**Chosen:** in the weak-vowel gray zone, fixed morphemes decide first: the word-initial reduced prefixes *be-, de-, re-, pre-, se-, e-/ex-* and the endings *-ed, -es, -age, -ange* take `ɪ` (`bɪkɒ́z`, `dɪzájn`, `rɪméjnz`, `ɪkspɛ́rɪmənt`, `lǽŋɡwɪdʒ`, `ɔ́rɪndʒ`). Everywhere else, spelling decides: i/y → `ɪ`, any other letter → `ə`.

**Also valid:** the OED/Longman `ᵻ` (honest about the variability, but it defers the decision to the reader); always `ə` (full weak-vowel merger); pure spelling with no morpheme layer (this system's original rule — mechanical, but it forced `ə` into *because, before, design, language*, contradicting Merriam-Webster in some of the most frequent words in English); or following one dictionary's notation (they contradict each other precisely here).

**Why:** determinism without betraying the reference accent. M-W's first listings have \i\ in exactly these prefixes and in *-age/-ange*, and unmerged American speakers produce `ɪ` there; promoting that closed morpheme list above the spelling rule keeps the answer fully mechanical — no lookup, no taste — while fixing the words where the pure-spelling rule audibly misfired. Outside the list, the spelling rule still gives a mechanical answer and visually anchors the transcription to the written word.

**Extended to reduced medial `i` (2026-09-27).** The spelling layer settles a *medial* reduced syllable spelled `i` on the same terms, where the dictionaries write a schwa and the corpus had drifted: *anticipating* `æntɪ́sɪpèjtɪŋ` (M-W `an-ˈti-sə-ˌpāt-iŋ`), *domination* `dɒ̀mɪnéjʃən`, *imagination* `ɪmæ̀dʒɪnéjʃən`, *eliminate* `ɪlɪ́mɪnèjt`, *similar* `sɪ́mɪlər`, *hallucination* `həlùwsɪnéjʃən` (with *hallucinates* `həlúwsɪnèjts`) and *termination* `tərmɪnéjʃən`. Five tokens in `examples/` and fifteen in `AI-103-questions.json` were swept, and the corpus already used `ɪ` for the same environment (*combination* `kɒ̀mbɪnéjʃən` ×3, *determination* `dɪ̀tɜrmɪnéjʃən`, *eliminating* `ɪlɪ́mɪnèjtɪŋ` ×5, *similarity* `sɪ̀mɪlɛ́rɪtij`) — the same direction as the *principle* ruling.

**No guard, deliberately:** unlike `-ible`, this class is not decidable from the transcription, because the defect and the rule are the same character in the same position — `sɪ́mələr` and `sɜ́rvəs` differ only in which letter the source spells, and both vowels are legal there. `check_string` returns 0 issues for either form, so the judge is the source word: a guard would need the aligned source, and a blanket `[a-z]+ənéjʃən` rule would fire on legitimate `ə` (the `a` of *explanation* `ɛ̀ksplənéjʃən`, the `u` of *documentation* `dɒ̀kjəmɛntéjʃən`). The ledger entries and the §13 row carry the rule instead.
### The class sweep: a reduced `i`/`y` written `ə` becomes `ɪ` (2026-09-27)

**Chosen:** the §4.4 spelling tie-breaker applied to the whole class, in two passes. First the 62 words `examples/` and `AI-103-questions.json` spelled *both* ways were made uniform on the `ɪ` form — 312 tokens (44 in `examples/`, 268 in AI-103) — because a word written two ways is a defect whatever the rule says. Then the 101 words that wrote `ə` consistently were swept the same way: 284 tokens (60 examples, 224 AI-103). Every word is recorded in the ledger, following the `-ible` and `-uni-` precedent.

**Stress disagreements went to M-W.** Where two shapes differed only in stress, M-W decided the accent and the vowel rule still applied to any spelled-`i` reduction: *primarily* `prajmɛ́rɪlij` (M-W's grave on `-mer-`, plus `ɪ` for the medial `i`). Three words needed both decisions at once, neither corpus shape having both: *deterministic* `dɪtɜ̀rmɪnɪ́stɪk`, *diagnosis* `dàjəɡnówsɪs`, *prioritization* `prajɔ̀rɪtɪzéjʃən`.

**What is exempt, and why.** Two things are deliberately *not* swept. (a) The `-est` ending, which §4.4 sends to `ə` (`hájəst`) — the audit mis-traced it, because the schwa sits after a silent *gh*. (b) The `(-ə)r` bucket — 28 words / 94 occurrences where the schwa sits directly before `r` (*entire* `ɪntájər`, *fire* `fájər`, *environments* `ɪnvájərənmənts`); that is the syncope question, not this one, and is still open. A third exemption, the fixed `-ization` ending, was **withdrawn** on 2026-09-27 — see below.

**One word is syncope, not `ɪ`.** *family* is `fǽmlij`: M-W's first listing `ˈfam-lē` is already compressed, so the syllable drops rather than taking the ɪ (§4.4), as in *several* `sɛ́vrəl`. The author ruled it, and the ledger records it. It is the reminder that this class is decided by the same two-step tie-breaker, not by a blanket rule about the letter `i`.

**Why a sweep at all, and not a silent fix:** the validator is blind here (`sɜ́rvəs` and `sɜ́rvɪs` both pass), and the two files disagreed for real words (*analysis* ×30 vs ×2, *service* ×31 vs ×1, *confidence* ×17 vs ×8). The audit method is worth reusing: align source and transcription sequentially, trace each `ə` to its source vowel group, and treat an `i`/`y`-only group as a defect — while remembering that a dictionary's own listing can still compress the syllable away.

### Later same-day rulings (2026-09-27, author)

**The `-ization` exemption is withdrawn.** The pass above kept `-əzéjʃən` as a fixed §1 ending (88 tokens). The author ruled that wrong: the ending's reduced `i` takes `ɪ` like any other spelled `i`, exactly as `prajɔ̀rɪtɪzéjʃən` and `nɔ̀rməlɪzéjʃən` already did. 84 tokens swept — 23 in `examples/`, 61 in `AI-103-questions.json` — and the change is byte-neutral (`ɔ̀rɡənəzéjʃən` → `ɔ̀rɡənɪzéjʃən`, `ɒ̀ptɪməzéjʃən` → `ɒ̀ptɪmɪzéjʃən`, `sə̀mərəzéjʃən` → `sə̀mərɪzéjʃən`). §1's suffix table, the §13 exempt list and a new §13 row carry the rule; *optimization*'s ledger entry was updated in place.

**`camera` is syncope.** M-W's first listing `ˈkam-rə` is already compressed, so §4.4 drops the syllable: `kǽmərəz` → `kǽmrəz`. 4 tokens (1 in `examples/`, 3 in AI-103), recorded in the ledger and added to the *family*/*several* §13 row. ***memory*** — the third member (`ˈmem-rē`) — was ruled the same way the same day: `mɛ́mərij` → `mɛ́mrij` (56 tokens: 47 in `examples/`, 9 in AI-103), deliberately *against* the corpus majority, so the family is now uniform.

**`compliment` takes `ɪ`, `complement` keeps `ə`.** The tie-breaker reads the bare letter: *compliment(s)* is spelled `i` → `kɒ́mplɪmənts`, *complement(s)* is spelled `e` → `kɒ́mpləmənts` (M-W writes a schwa for both). No corpus token was affected — all four are *complement(s)* — so only the ledger entry changed. The same reading fixes *complimentary* `kɒ̀mplɪmɛ́ntərij`.

**The fixed *-es* ending was slipping in AI-103.** `mɪ́nɪmàjzəz` (*minimizes*), `stéjbɪlàjzəz` (*stabilizes*), `fréjzəz` (*phrases* ×5), `ɪnkríjsəz` (*increases*), `tʃúwzəz` (*chooses*), `dɪfɛ́nsəz` (*defenses*), `béjsəz` (*bases*), `pɔ́zəz` (*pauses*) and `fjúwzəz` (*fuses*) wrote `əz` where §4.4's fixed *-es* → `ɪz` applies after a sibilant: 14 tokens swept to `…ɪz`. Every `examples/` token was already correct, which is why no pair check ever flagged it.

**The fixed prefixes are not position-bound.** §4.4 used to say the `be-, de-, re-, pre-, se-, e-/ex-` prefixes take `ɪ` only when word-initial, and used *represent* `rɛ̀prəzɛ́ntɪd` as the spelling-rule counter-example. The author ruled the restriction wrong; the phrase and the counter-example are gone from the guide. The corpus follow-up is **pending**, and it is not small: the *represent* family alone is 50 `rɛ̀prə…` tokens (examples 18, AI-103 32 — `rɛ̀prəzɛ́ntətɪv` ×28, `rɛ̀prəzɛ́nts` ×9) against 5 that already write `rɛ̀prɪ…` (all in AI-103), *reproduce* adds `rɛ̀prədə́ktɪv` ×3 and `rɛ̀prədə́kʃən` ×2, and *undesirable* `ə̀ndəzájərəbəl` is the only `de-` case found. M-W writes plain `i` for all of them (`ˌre-pri-ˈzent`, `ˌən-di-ˈzī-rə-bəl`), so the `ɪ` form is what the corrected rule implies.

***presentation* is split as well, and ruled for the second listing.** `prɛ̀zəntéjʃən` ×4 matches M-W's *second* listing `ˌpre-zᵊn-ˈtā-shən`; the single *Habituation* token followed the *first* listing's accent pattern (`ˌprē-ˌzen-ˈtā-shən`) and had the wrong vowel symbol (PALM `ɑ̀` for DRESS `ɛ̀`). The author ruled the compressed second listing on 2026-09-27, so all 5 tokens read `prɛ̀zəntéjʃən` — an editorial exception to §1's first-listing rule, recorded as a §13 row and in the ledger.

### A reduced `e` takes `ɪ` like a spelled `i` — except before `r l n m ŋ t` (ruled and swept 2026-09-27)

**Chosen:** the §4.4 spelling tie-breaker now applies to the letter `e` too, with one carve-out. A reduced vowel spelled *e* takes `ɪ` wherever a spelled *i* or *y* would (*knowledge* `nɒ́lɪdʒ`, *specific* `spɪsɪ́fɪk`, *orchestration* `ɔ̀rkɪstréjʃən`, *categories* `kǽtɪɡɔ̀rij`, *strategies* `strǽtɪdʒij`), but keeps `ə` when the symbol following the vowel is `r`, `l`, `n`, `m`, `ŋ` or `t` (*other* `ə́ðər`, *table* `téjbəl`, *different* `dɪ́frənt`, *problem* `prɒ́bləm`, *fitness* `fɪ́tnəs`, *market* `mɑ́rkət`, *ticket* `tɪ́kət`). The fixed §6/§7 morphemes still outrank both layers (`because` `bɪkɒ́z`, `happiest` `hájəst`).

**Why adjacency decides, not syllabification.** The schwa's usual justification is a closed syllable — M-W writes `ˈmär-kət`, with the *e* in a checked syllable — but this notation writes no syllable boundaries, and no list of words may be added to the guide. The rule therefore reads the *next symbol*: a following `r l n m ŋ t` is what a checked rear vowel looks like in the transcription, and the test is fully mechanical. Every reduced *e* left over stands before a consonant the system treats as an onset (*knowledge* `-l-`, *specific* `-s-`), where the spelling layer gives `ɪ`.

**`t` was carved out the same day, on the author's review.** The first sweep wrote `ɪ` before `t` as well, which produced 15 forms the author rejected — *market, target, ticket, carpet, pocket, cabinet, benefit(s)* and their inflections. M-W writes a schwa in every one of them (`ˈmär-kət`, `ˈtär-gət`, `ˈtik-ət`, `ˈkär-pət`, `ˈpä-kət`, `ˈka-bə-nət`, `ˈbe-nə-ˌfit`), so `t` joins the exception list, and both the swept forms and the same environment that already wrote `ɪ` before the sweep — *rocket(s)*, *budget/budgeting/budgeted*, *planet*, *supermarket*, *benefit(s)* — were reverted to the schwa: 37 forms, 140 tokens. The carve-out makes the rule question the reference accent twice over, so it is recorded here and in the §13 row rather than left to the guard.

**Where the sweep stops.** Only vowels spelled `e` are in scope. The same *environment* in words spelled `i` or `y` is untouched — *profit* `prɒ́fɪt`, *quality* `kwɑ́lɪtij`, *edits* `ɛ́dɪts`, *cognitive* `kɒ́ɡnɪtɪv` — with *benefit(s)* `bɛ́nɪfət(s)` ruled the other way explicitly, because the author read the schwa for the consonant as well as for the letter. The internal reduced prefixes (*represent*, *delivery*, *retrieval*, *remaining*) are also out of scope: their `ɪ` is a fixed morpheme, and that corpus follow-up is still pending (above).

**An individual basis for now (author, 2026-09-27).** The author's own reading is that the `e` case resists a clear rule: M-W writes a plain schwa where the letter rule predicts `ɪ` (*synthesis* `ˈsin(t)-thə-səs`, *necessarily* `ˌne-sə-ˈser-ə-lē`) and a plain `i` where the spelling rule already gives `ɪ` (*definite* `ˈde-fə-nət`), and the same two letters take a schwa in *market* and *hundred*. So the decision stays **word by word** for the moment: the default above is what the swept corpus follows and what the guard enforces, a word that M-W writes with a schwa may be ruled the other way and registered in the ledger, and the general rule is restated once the corpus is large enough to show it. The t-class amendment (above) is itself an instance of that: 15 words were ruled back to the schwa on the author's review, not by re-deriving the rule.

**The guard, split in two (author, 2026-09-27).** `validate_transcriptions.py` enforces only the **ə half** of the rule, in paired mode, because only the source spelling says whether the reduced vowel is an `e`: `check_e_reduction` aligns the source's vowel groups to the transcription's nuclei one to one, skips any group covered by a fixed §6/§7 ending or by a fixed prefix, and requires `ə` before `r l n m ŋ t`. That half never contradicts the dictionary — a reduced `e` before a sonorant or `t` is a schwa in every word the corpus and M-W agree on (`mɑ́rkət`, `téjbəl`, `prɒ́bləm`, `fɪ́tnəs`, `hə́ndrəd`) — and it is what keeps the reverted `mɑ́rkɪt` / `pǽkɪts` shapes from returning. The **ɪ half is practice, not a check**: M-W writes a schwa in many of those words (`specific` `spə-`, `synthesis` `-thə-`, `necessarily` `-sə-`), so the author ruled that the class is decided word by word for now, and the code keeps the old behaviour behind `E_ENFORCE_KIT = False` (one line to flip when the corpus settles the rule). `spəsɪ́fɪk` and `spɪsɪ́fɪk` are therefore both accepted, and the ledger carries the ruled form. Words whose first segment is a fixed prefix are skipped so as not to pre-empt the pending prefix ruling, and a group/nucleus count mismatch abandons the pair rather than guessing.
### Parenthesized schwas are dropped (syncope)

**Chosen:** when M-W's first listing parenthesizes a medial schwa, it is not written: `dɪ́frənt`, `sɒ́vrən`, `lǽbrətɔ̀rij`. Unparenthesized full forms keep it: `nǽtʃərəl`. The fixed §6/§7 tables outrank the rule, so suffix transcriptions like *-ally* `əlij` stay stable.

**Also valid:** always writing the full form (citation style, closer to the spelling); or a lookup-free phonological rule (drop post-stress schwa before r/l/n), which would however contradict M-W where it lists the full form first (*natural*).

**Consequence:** the rule reads the word's own listing, not its base's, so a derived word can syncopate where its base does not: *real* `ríjəl` / *really* `ríjlij`, *careful* `kɛ́rfəl` / *carefully* `kɛ́rflij`. Applying the base's shape to the derived word would silently restore a syllable natives skip in the one form that matters.

**Exception by ruling, not by derivation:** a word can be kept in the full form because the author prefers it spoken that way, even where M-W parenthesizes the schwa. *answerable* is `ǽnsərəbəl`, not `ǽnsrəbəl`; `-able` words keep the three-syllable shape. Such rulings are recorded per word in `transcription-corrections.json`, which keeps this rule derivable while allowing deliberate exceptions.

**Exception by ruling in the other direction (2026-09-27):** the whole *danger* family is ruled compressed — `déjndʒər`, `déjndʒərəs`, `déjndʒərəslij`, `déjndʒərz` — not the `déjnədʒər` / `déjnədʒərəs` that §4.4 derives from M-W's `ˈdān-jər` and `ˈdān-jə-rəs`, whose medial schwa is unparenthesized in both. Fifteen derived tokens already read that way and only one noun token deviated (`déjnədʒər` in `TRN_TheY2KNonEvent.txt`), so that one was swept to `déjndʒər`; the ledger carries an entry for each member (*danger*, *dangerous*) so a later reader applying M-W does not “fix” them back. This is the one place where the system overrides the parenthesis rule toward compression, and it is a per-word ruling rather than a class rule — unlike the `-Vl + ing` group, no other word may be compressed on its authority.

**Exception by ruling toward the full form (2026-09-27):** the whole *general* family is ruled to **keep** the medial schwa — `dʒɛ́nərəl`, `dʒɛ́nərəlij`, `dʒɛ́nərəlàjzɪz`, `dʒɛ́nərəlàjzɪŋ`, `dʒɛ̀nərəlɪzéjʃən` — although M-W's first listing is compressed or bracketed in every member (`ˈjen-rəl`, Kids `ˈjen-(ə-)rəl`, `ˈjen-rə-lē`, `ˈjen-rə-ˌlīz`, `ˌjen-rə-lə-ˈzā-shən`), so §4.4 syncope would drop the syllable. The corpus already read that way in 11 of the 13 tokens; only *generally* was syncopated (`dʒɛ́nrəlij`, `TRN_Habituation.txt` and `TRN_TheSelfishGene.txt`), so those two tokens were restored to `dʒɛ́nərəlij` and the family is now uniform. It is the counterpart of *danger*: there the author overrode the parenthesis rule toward compression, here toward the full form, and in both cases the ruling is per word (registered in the ledger) rather than derivable from M-W. The *family*/*camera*/*memory* row keeps its own direction, so the two sibling families now sit on opposite sides of the same parenthesis — which is precisely why the class cannot be swept mechanically.

**Why:** connected speech is the point. The compressed forms are what GA speakers actually produce; writing the schwa invites learners to restore a syllable natives skip. The M-W parenthesis makes the call deterministic — the same single authority the system already leans on.

### Syncope before `l` in `-Vl + ing` forms — the parenthesis decides, not the letter (ruled 2026-09-26)

**Chosen:** apply §4.4 mechanically to every `-Vl + ing` form, reading M-W's *own* listing of that form. Three shapes, three outcomes: a bracketed `(ə-)` drops the syllable (*wobbling* `wɒ́blɪŋ`, *disabling* `dɪséjblɪŋ`, *labeling* `léjblɪŋ`, *canceling* `kǽnslɪŋ`, *enabling* `ɪnéjblɪŋ`, *sampling* `sǽmplɪŋ`); an already-compressed first listing stays compressed (*modeling* `mɒ́dlɪŋ`, *unsettling* `ə̀nsɛ́tlɪŋ`, *coupling* `kə́plɪŋ`); a schwa M-W writes in full is kept (*handling* `hǽndəlɪŋ`, *throttling* `θrɒ́təlɪŋ`, *signaling* `sɪ́ɡnəlɪŋ`, *untangling* `ə̀ntǽŋɡəlɪŋ`).

**Also valid:** an editorial exception keeping the full form everywhere — the corpus ran that way 8–3 for the drop group, and the `-able` ruling shows the pattern for such exceptions; or syncopating every `-Vl + ing` form regardless of the parenthesis, which is the simplest rule but contradicts M-W in *handling*, *throttling* and *signaling*.

**Why:** the corpus was split and the validator is blind here — `check_string` returns 0 issues for both `wɒ́bəlɪŋ` and `wɒ́blɪŋ`, so only a rule keeps the corpus consistent. Deciding by the parenthesis rather than the letter `l` keeps one principle for the whole guide: the same `(ə-)` that compresses *different* and *really* compresses *wobbling*, and the same unparenthesized schwa that preserves *natural* preserves *handling*. The corpus had erred in both directions — keeping a syllable M-W brackets in *wobbling*, and dropping one M-W writes in full in *handling* while already writing the schwa in *handles* `hǽndəlz`.

**Exception by ruling (2026-09-26):** *reconciling* is `rɛ́kənsàjlɪŋ`, not the `rɛ́kənsàjəlɪŋ` that the `(-ə)` row would derive from the base *reconcile* — M-W lists no participle pronunciation, and the author ruled the compressed form. It is recorded in the ledger like the `-able` exception, so an audit of this class does not "fix" it back.

### `-ible` is `ɪbəl`, `-able` is `əbəl` — a fixed ending outranks M-W's schwa (ruled 2026-09-26)

**Chosen:** every `-ible` word takes `ɪbəl`, and its derivatives `ɪblij` / `ɪbɪ́lɪtij`, while `-able` keeps `əbəl`: `flɛ́ksɪbəl`, `vɪ́zɪbəl`, `rɪspɒ́nsɪbəl`, `səsɛ̀ptɪbɪ́lɪtij` against `dʊ́rəbəl`, `mǽnɪdʒəbəl`. The §7 suffix table is fixed, so it decides before M-W's notation (`ˈflek-sə-bəl`, `ˈvi-zə-bəl`) — the same direction as the §4.4 tie-breaker, since the reduced vowel of `-ible` is spelled *i*.

**Also valid:** following M-W literally, which writes `flɛ́ksəbəl` / `vɪ́zəbəl` / `rɪspɒ́nsəbəl`. That is what the corpus had drifted into on 14 tokens, while the rest of the class already wrote `ɪ` — *possible* ×12, *impossible* ×4, *compatible* ×3, plus *tangible*, *digestible*, *credible*, *plausible*, *accessible*, *reversible*, *invisible*, *eligible* and *visible* ×13 — so the system was split on its own words rather than on a principle.

**Why:** one rule for the whole ending family, applied from the source spelling instead of by taste. Majority could not settle it, because the split ran by word: *responsible* leaned `ə` (6 to 2) while the `ɪ` group was larger but never unanimous, and the ledger already recorded `tangible` as `tǽndʒɪbəl` and `possible` as `pɒ́sɪbəl`, which made the `ə` tokens defects relative to rulings the author had already approved. The `-able` half of the pair is deliberately untouched: M-W compresses *table* to `téjbəl` and keeps *durable* at `dʊ́rəbəl`, and §4.4 already reads M-W's own listing for those.

**Guard:** `validate_transcriptions.py` applies the rule two ways, because `-able` legitimately writes `əbəl` and a transcription alone cannot tell the two endings apart. Pair mode (`check_ible_vowel`) reads the *source* token: if it ends in `-ible`, `-ibly`, `-ibles` or `-ibility`, the vowel before that `b` must not be `ə`. `--text` mode sees no source, so it carries the exact ruled stems (`IBLE_RULINGS`): `flɛ́ksə`, `vɪ́zə`, `spɒ́nsə`, `sɛ̀ptəbɪ́`, `krɛ̀dəbɪ́`, `dùwsəbɪ́`, `sɛsəbɪ́`. *Accountability* was corrected in the same sweep, but only its fixed `-ity` vowel was wrong — it is an `-able` word, so the pair rule does not apply and no sequence is listed for it.

**Sweep (2026-09-26, author approved):** 14 example tokens (`flɛ́ksəbəl` ×2, `rɪspɒ́nsəbəl` ×6 including `ɪ̀rɪspɒ́nsəbəl`, `vɪ́zəbəl`, `səsɛ̀ptəbɪ́lɪtij`, `krɛ̀dəbɪ́lətij`, `ə̀kawntəbɪ́lətij`, `rɪspɒ̀nsəbɪ́lɪtij` ×2) and 8 AI-103 tokens (`flɛ́ksəblij`, `flɛ̀ksəbɪ́lɪtij`, `vɪ̀zəbɪ́lɪtij`, `rìjprədùwsəbɪ́lɪtij` ×2, `æ̀ksɛsəbɪ́lɪtij` ×3); `TRN_ONE.txt` regenerated; ledger 190 → 195 entries.

### The reduced *be-* prefix is `bɪ-`: *behavior* (ruled 2026-09-26)

**Chosen:** the reduced word-initial *be-* is `bɪ-`, exactly like the other reduced prefixes — `bɪhéjvjərz`, `bɪhéjvər`, alongside `bɪkɒ́z`, `bɪfɔ́r`, `bɪhájnd`. M-W's *behavior* is `bi-ˈhā-vyər`: a reduced initial syllable, which the §4.4 fixed-morpheme step resolves to `ɪ` before the spelling rule is ever consulted.

**Also valid:** M-W's literal schwa reading, `bəhéjvjərz` — which is what one file had drifted into. It is not a defensible variant of the reference accent, merely the weak-vowel zone's other option applied without the morpheme layer that §4.4 already provides for `bɪkɒ́z` and `bɪfɔ́r`; treating *behavior* differently from *because* would split the same prefix by taste.

**Why:** the morpheme list exists to keep this zone mechanical, and the corpus was already 253-to-13 for `bɪ-`. The 13 exceptions were not spread across words or files: they were the whole *behavior* family in `TRN_TheSelfishGene.txt` (11 × `bəhéjvjərz`, 2 × `bəhéjvər`), while the rest of the corpus and `AI-103-questions.json` wrote `bɪ-` throughout. The same stem is decisive here — `bɪhéjvjərəl` ×3 already used `ɪ`, so the base form was the odd one out within its own family.

**Found by, not by the validator:** `check_string` reports no violation for `bəhéjvjərz` or `bɪhéjvjərz`, so this is another blind-spot class, like `rájɪŋ`, `flwj`, `vúw` and `rədə́kʃənɪst`. What surfaces it is an aligned dump of every source word starting `be` against its transcription, where the `bə-` tokens stand out immediately (13 against 253).

**No guard, deliberately:** unlike `-ible`, this class is not mechanically decidable from the transcription. A source-aware pair rule would fire on every *be-* word written `bə-`, which is rare but would still need a word list to stay honest, and an unsourced `--text` rule cannot tell a defective `bəhéjvjərz` from a legitimate `bə` (`əbáwt`). Thirteen tokens in one file did not justify that complexity; the ledger entry and the §13 row carry the rule instead.

**Sweep (2026-09-26, author approved):** 13 tokens in `examples/TRN_TheSelfishGene.txt` (byte-neutral `ə`→`ɪ`), `TRN_ONE.txt` regenerated, ledger 196 → 197 entries, and a §13 row placed directly after the reduced-prefix row.

### The `ɛ́j` class, and what a full audit of one file shows (2026-09-26)

**Chosen:** FACE is `ej` and nothing else; `ɛ` remains DRESS. A transcription that writes `ɛ́j` (`bɛ́jsɪs`, `dɪbɛ́jt`, `kəmjúwnɪkɛ́jʃən`, `rɪlɛ́jʃənʃɪp`) is not a variant of the reference accent but a different diphthong, so it is corrected to `éj` and mechanically rejected (`epsilon-glide`).

**Also valid:** nothing. This is the one class in the guide where the notation itself leaves no room — §4.2 lists `ij uw ej ow aj aw ɔj`, `ɛ` is a short monophthong, and the corpus writes `éj` 5085 times against 58. There is no dialect or dictionary reading in which DRESS plus a glide spells FACE.

**Why record it at all:** the validator could not see it. `invalid-glide-vowel` checks Latin base letters (`a e i o u`), and `ɛ` is not one, so `bɛ́jsɪs` passed every mechanical check while `béjsɪs` also passed. The class survived 19 file reviews and a 24 000-token consolidation, and 28 of its 58 instances sat in one file.

**How it was found:** not by the validator and not by spot checks, but by an audit that compares each source word's transcription *across files* and then scans every token against the classes already recorded in repo memory. Ten reviewer-flagged tokens were the entry point; the audit turned up forty more defects in the same file — misplaced primary stress (`dɪ́sɔrdərz` → `dɪsɔ́rdərz`), omitted secondary-stress graves (`ɪ́nsajts` → `ɪ́nsàjts`), LOT/PALM confusion (`kɑ́nsɛpt` → `kɒ́nsɛ̀pt`), a dropped `r` in a cluster (`kɒ̀ntrəvɜ́ʃəl` → `kɒ̀ntrəvɜ́rʃəl`), a dropped `g` (`sədʒɛ́stɪŋ` → `səɡdʒɛ́stɪŋ`), a lost `j` (`bɪhéjvər` → `bɪhéjvjər`), a dropped `u` nucleus (`dʒwəl` → `dʒuwəl`), and one word whose transcription was borrowed from its base (`evolutionarily` written as `evolutionary`, invisible to any string rule because the file wrote both as the same token).

**Guard:** `epsilon-glide` in `SEQUENCE_RULES`, with two invalid fixtures and one valid counterpart. It is a whole-text regex, so it also catches `ɛ̀j`. `--self-test` went from 123 to 126.

**Lesson worth keeping:** the mechanical checks were green on that file before and after. What found the defects was source-aligned comparison across files — two files spelling the same source word differently means at least one is wrong, and the majority plus §4.4 resolves most of them. Every class that survives a validator pass needs an audit that reads the source.

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

**Why:** fixing `ǽr` in writing preserves the distinction for speakers who have it and keeps transcription deterministic. Readers whose accent merges *marry* with *merry* may pronounce written `ǽr` as `ɛ́r`; that freedom belongs to speech, not to the transcription. One of the three documented departures from pure GA.

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

**Why:** the IPA letterform is unambiguous, and reserving ASCII `g` as an error in phonetic material makes machine validation strict. Lowercase ASCII `c q x y` are likewise banned from phonetic material for the same reason. Verbatim notation and identifiers retain their original characters, including `g` in `fingerd` (§9 of the guide).

## Stress

### Accent marks on the vowel — not `ˈ ˌ`

**Chosen:** acute = primary (`dʒǽkət`), grave = secondary (`mæ̀θəmǽtɪkəl`), on the first vowel symbol of the nucleus.

**Also valid:** IPA `ˈ ˌ` before the syllable; dictionary primes after the syllable; Trager–Smith-style multi-level accent systems.

**Why:** three reasons. Learners who know Spanish or Greek orthography read vowel accents natively. The mark sits exactly where the prominence is, rather than floating in the string. And — decisive for the determinism goal — `ˈ` placement requires deciding where syllables *begin*, an entire class of judgment calls (`con.trol` or `cont.rol`?) that vowel-attached accents never raise.

### Weak forms are transcribed

**Chosen:** function words use conventional connected-speech forms — `əv, tə, ðə / ðij, həz` — selected by grammatical role, with explicit contrast and clause-final strong forms handled by §6. Weak *the* is `ðə` before a consonant sound and `ðij` before a vowel sound; the choice follows pronunciation rather than spelling (`ðə jùwnɪvɜ́rsətij`, `ðij áwər`).

**Also valid:** citation forms throughout, which is what dictionaries show; or invariant weak `ðə`, reflecting the considerable variation in spontaneous American speech.

**Why:** connected speech is the point. Rhythm and reduction are where learners' comprehension fails, and a transcription of sentences (rather than isolated words) should show conventional reductions without trying to predict every speaker's intonation. The familiar `ðə` / `ðij` alternation gives learners a deterministic way to avoid vowel hiatus, even though native usage is not categorical. Bareness (no accent) is the written signal of weakness — but only for monosyllables: a polysyllabic function word keeps its word-internal acute (`ɪ́ntə`, `əbáwt`, `áwər`), because there the mark locates the stressed syllable, information a bare form would destroy (and `ə` is stressable in this system, so it is not recoverable).

### Grammatical role before weak-form lookup

**Chosen:** *all* is always `ɔ́l`, like *both* and *each*. Verbal particles are content-like and accented, whether adjacent to the verb or separated by its object: *turn on*, *turn it on*. Prepositions remain weak by default, including in prepositional verbs (*rely on*) and particle-plus-preposition constructions (*put up with*: accented *up*, weak *with*). Independent or explicitly contrastive *some* is `sə́m`; the indefinite determiner is `səm`. Interrogative/exclamative *what* is `wɒ́t`, including in contractions and embedded questions; fused-relative *what* is `wɒt`. Lexical *does / did* are `də́z / dɪ́d`, while auxiliaries are weak by default. *Do* follows the same pattern: auxiliary `də`, lexical and emphatic `dúw` (see below).

**Also valid:** an invariant word list regardless of grammar; or a full prosodic transcription based on a particular recording.

**Why:** a bare word list hides distinctions learners need: *line them up on the board* contains both a particle and a preposition, and *some pieces* differs from independent *some*. The written acute encodes conventional word stress, not necessarily sentence focus. Thus a particle stays accented even when the following object is more prominent in speech, just as every noun retains its written accent. *All* is assigned an invariant acute for consistency with the other quantifiers, not because it must always be prominent. The guide provides grammatical tests and default readings for ambiguous particle/preposition and embedded-*what* constructions. This is a text-based convention, not a claim to recover a unique spoken intonation.

**What stays weak:** a full vowel does not imply an acute, and the monosyllabic possessive determiners (`maj`, `jɔr`, `hɪz`, `ɪts`, `ðɛr`) stay bare. Copular *be* behaves like auxiliary *be*: *they are happy* and *they are working* both use `ɑr`. Explicit contrast and clause-final ellipsis can require `ɑ́r` etc.; being a copula alone cannot. *our* is the one exception — see the next subsection.

**Independent and lexical uses:** independent possessive *his* is accented (`hɪ́z`), unlike determiner *his* (`hɪz`). Personal pronouns used as independent answers also take strong accented forms (*who did it? me.*), but a pronoun is not automatically accented just because it is sentence-final (*I saw him*). Likewise, the weak modal list applies only to modals: nominal/verbal *can*, nominal/verbal *will*, nominal *might*, nominal *must*, and the month/name *May* are content words with full accented pronunciations. These clarifications apply the existing role-first principle, not a blanket change to pronouns or modals.

### *our* keeps the acute of its word-internal stress

**Chosen:** the possessive determiner *our* is `áwər` in neutral use — not bare `awər` (author ruling, 2026-10-01). The monosyllabic possessive determiners stay bare (`maj`, `jɔr`, `hɪz`, `ɪts`, `ðɛr`), and copular *are* stays weak `ɑr`; the independent possessive *ours* follows the independent-possessive rule and is `áwərz`. The noun *hour(s)* is unchanged (`áwər`, `áwərz`), so determiner *our* and noun *hour* are homographs — the source word disambiguates them, and both are /aʊər/.

**Also valid:** the previous reading, which left neutral *our* bare and reserved `áwər` for explicit contrast; the corpus wrote the bare form in all 34 occurrences.

**Why:** the bare form is for monosyllables (§5.2), and the guide already makes a polysyllabic function word keep the acute of its word-internal stress — `ɪ́ntə`, `əbáwt`, `ówvər`. `awər` was the single exception, kept bare only by a carve-out sentence that called the `ajər / awər` sequence one syllable. *our* is the only possessive determiner that is not a monosyllable, so deleting the carve-out leaves one rule instead of a rule plus an exception, aligns *our* with the rest of its own nucleus (`páwər`, `fláwər`, `áwərz`), and needs no new machinery: the acute still marks word stress, not sentence focus.

**Validation boundary:** `awər` was removed from the checker's weak-form allowlist, so a bare `awər` now fails the paired and strict checks as an unaccented token (new invalid fixture; the old valid sample now uses `áwər`). The change is decidable from the transcription alone — a reduced *our* is written `ɑr`, never `awər` — which is why this ruling can be guarded mechanically, unlike the per-word rulings delivered against a derivation (*general*, *danger*). 34 corpus tokens were swept (6 example files, mirrored in `TRN_ONE.txt`); `AI-103-questions.json` has no source *our*.

### Auxiliary *do* is weak; lexical and emphatic *do* keep the acute

**Chosen:** auxiliary *do* is `də` — weak by default in statements, negatives, and questions — exactly like auxiliary *does* `dəz` and *did* `dɪd`. `dúw` is kept for lexical *do* (*what to do*, *do the work*), explicit contrast, affirmative emphatic do-support (*I do want to proceed* `aj dúw wɒ́nt tə prəsíjd`), and clause-final ellipsis (*yes, they do*). *I do not want to proceed* is `aj də nɒ́t wɒ́nt tə prəsíjd`.

**Also valid:** the previous rule, treating *do* as a fixed exception always accented even as an auxiliary (closer to M-W's citation stress \ˈdü\); or a genuinely prosodic transcription marking whatever the speaker stresses in a given recording.

**Why:** the fixed exception was the only member of its paradigm with no weak form — the checker's allowlist already carried `dəz dɪd həv həz həd əm ɪz ɑr` — and it made the notation contradict what learners hear: `dúw nɒ́t` teaches a full vowel where connected speech has a reduced one. It also produced an internal contradiction between the guide's own examples: *Who did it?* was written with weak auxiliary `dɪd`, while *where do you come from?* was written with accented auxiliary `dúw`, in the same grammatical slot. No new machinery is needed — the strong form uses the three triggers already written for *does* and *did*. The pair `aj dúw wɒ́nt tə prəsíjd` / `aj də nɒ́t wɒ́nt tə prəsíjd` now teaches the actual prosodic contrast, and determinism survives because the test is grammatical rather than impressionistic.

**Validation boundary:** `də` was added to the checker's weak-form allowlist, with a fixture asserting the new pair. The checker cannot distinguish an auxiliary `dúw` from a lexical one — both are legal accented tokens — so this stays a source-review decision, recorded as the ledger entry `do (auxiliary)`. Any sweep must match the source word *do*, never the string `dúw`, which also spells *due to* and *doing*.

### Not is accented; demonstratives follow grammatical role

**Chosen:** independent *not* is always `nɒ́t`, including in *not only*. Neutral demonstrative determiners are unaccented with full vowels: *this / that / these / those* are `ðɪs / ðæt / ðijz / ðowz`, including before modifiers (*that old book*). Independent or explicitly contrastive uses take `ðɪ́s / ðǽt / ðíjz / ðówz`. Conjunction/relative *that* remains weak `ðət`; demonstrative *that's* and negative contractions retain their existing accents.

**Also valid:** accenting all demonstratives regardless of grammatical role; or transcribing their actual prominence from a particular recording.

**Why:** accenting *not* aligns the independent negative with other adverbs and already-accented negative contractions. The same role-dependent rule for all four demonstratives parallels determiner vs. independent *his* and *some*. Leaving neutral determiners bare better guides learners toward ordinary phrase rhythm without suggesting prominence on every demonstrative before a noun. Full vowels do not require an acute: demonstrative *that book* is `ðæt bʊ́k`, not `ðət bʊ́k`. Independent *that is a book* takes `ðǽt` by convention, although actual spoken prominence may fall on *book*. Explicit contrast also takes an acute (*THAT book, not THIS one*); mere reference to something previously mentioned does not establish contrast. The update affects whole words, not substrings of words such as *nothing* or *notice*.

**Validation boundary:** the checker rejects bare `ɔl` and `nɒt`, but accepts both bare and accented demonstratives. Its weak-form allowlist is not permission to use the weak spelling everywhere: `ðɪs / ðæt / ðijz / ðowz` require neutral determiner uses. Particle/preposition, determiner/pronoun, independent-answer, interrogative/relative, and lexical/auxiliary distinctions require source review; a clean mechanical result does not certify those decisions.

## Text conventions

### Word-internal apostrophes are omitted

**Chosen:** contractions, possessives, and names are transcribed as single phonetic words without their spelling apostrophe: `ɪts` (*it's*), `wɛ́rərz` (*wearer's*), `ðéjv` (*they've*), `owkɒ́nər` (*O'Connor*). Apostrophes remain only when they are quotation punctuation or part of a pass-through token such as `'70s`.

**Also valid:** preserving the source apostrophe inside every transcription.

**Why:** an apostrophe has no sound, and contractions such as *they're* (`ðɛ́r`) provide no phonologically meaningful place to put one. Omitting it makes the output deterministic and matches the system's broad-phonemic stance. Word-level alignment is unchanged: each contraction is still one token.

### All lowercase; capitals mean "say the letter name"

**Also valid:** preserving source capitalization; bracketing spelled-out tokens.

**Why:** outside verbatim notation, case carries no sound, so freeing it creates a clean channel: a capital represents a letter name (`USB`, `T-ʃɜ́rt`), even when attached to a phonetic word (`ówpənAI`). Preserving spoken words' source capitalization would make *A* (the word) and *A* (the letter) collide. Attached letter names do not exempt the phonetic component from stress and vowel checks.

### Letter-name endings are lowercase and phonetic

**Chosen:** keep the capital letter-name stem and append its regular spoken plural or possessive allomorph: `USBz`, `PDFs`, `Xɪz`. Select `s` / `z` / `ɪz` from the final sound of the last letter name, exactly as for an ordinary English word, and omit any spelling apostrophe.

**Also valid:** preserving the source ending (`USBs`); fully transcribing the letter names (`jùwɛ̀sbíjz`); or separating the ending typographically (`USB-z`).

**Why:** mixed case cleanly preserves the two kinds of information already encoded by the system: capitals say “read these letters by name,” while lowercase symbols describe the suffix actually heard. Direct attachment keeps the source token aligned without inventing a hyphen, and phonetic allomorph selection distinguishes forms such as `USBz`, `PDFs`, and `Xɪz` deterministically.

### Digits, formulas, and notation pass through

**Also valid:** spelling everything out (`1970s` → `nàjntijn sɛ́vəntijz`).

**Why:** notation has multiple valid readings; expanding it breaks 1:1 token alignment with the source and injects guesses. Whether a token is notation is semantic rather than typographic: `NASA` can be a pronounced acronym or an identifier, while `sin` can be an English word or a function name. The transcriber decides from context first, then either transcribes spoken language or preserves symbolic material. The validator deliberately does not claim to solve this classification problem.

### Combining accents (`æ` + U+0301), precomposed only for `á é í ó ú`

**Also valid:** full NFC normalization — a single code point (U+01FD) for æ-acute.

**Why:** it matches the existing corpus byte-for-byte and keeps "accent" a separable, checkable layer on top of "letter." The cost is real — many toolchains silently NFC-normalize — so the validator polices it and the README documents the one-line repair.

## Reference accent

### General American, Merriam-Webster first listing

**Also valid:** RP/SSB (Lindsey's own CUBE target — ironically, the glide notation's home accent); a fully merger-maximal GA; or accent-agnostic notation.

**Why:** GA is the accent most learners target and most media exposes them to, and M-W's first listing supplies a single deterministic authority for everything outside the weak `ɪ`~`ə` zone (where the morpheme-then-spelling tie-breaker rules). The three documented departures — `ɒ`/`ɑ`, `ǽr`, unwritten flapping — all *preserve optionality* rather than contradict GA: each keeps a distinction in writing that the reader may merge in speech.

---

### The 2026-09-28 corpus audit: five classes the validator cannot see

**How it was found.** The mechanical suite was green before the audit and stayed green after it: `--self-test` 147/147, 19 pair checks 0, `check_string(TRN_ONE)` 0, `check_json_file(AI-103)` 0. Everything below came from reading the *source* against the transcription, with four methods worth reusing:

1. **Cross-file consistency on punctuation-stripped tokens.** Comparing raw tokens gives ~1000 phantom rows, because a trailing comma or period makes the same word look like two forms; stripping the outside punctuation leaves only real disagreements (*dɪrɛ́kt* ×5 in `examples/` against *dərɛ́kt* ×9 in AI-103). Two files spelling one source word differently means at least one is wrong.
2. **Per-source-word counts in `examples/` against AI-103.** The two corpora drift apart independently, so one is often the witness for the other.
3. **Targeted fixed-morpheme scans** (§7 endings: `-es`, `-ed`, `-age`) driven from the *source* tail, which is what makes them decidable at all.
4. **M-W first-listing verification when a claim would change many tokens.** This killed a false alarm: *difficulty* is `ˈdi-fi-(ˌ)kəl-tē` with a **parenthesized** secondary stress, so both `dɪ́fɪkəltij` (11 tokens) and `dɪ́fɪkə̀ltij` are correct and nothing was swept.

**Chosen:** 319 tokens changed — 77 in `examples/`, 242 in `AI-103-questions.json` — in five classes: (a) the fixed `-es` → `ɪz` and `-ed` → `ɪd` endings, which had drifted in AI-103 only (50 + 47 tokens); (b) the missing grave on the `un-` prefix where M-W writes `ˌən-` (65 tokens; *until*/*unless* are the exceptions and `ə̀ntɪ́l` was the reverse error); (c) the reduced `i`/`y` layer in AI-103 (*direct* family, *manage* family, *privilege*); (d) word-level sound errors (`dɪvɜ́rs` → `dajvɜ́rs`, `ɛ̀ntájər` → `ɪntájər`, `sɜ́rfɪs` → `sɜ́rfəs`, `lájklɪhʊ̀d` → `lájklijhʊ̀d`, `ɪntɜ́rprɪt` → `ɪntɜ́rprət`); and (e) stress/grave placement (`ðɛ́rfɔr` → `ðɛ́rfɔ̀r`, `hàwɛ́vər` → `hawɛ́vər`, `ɒ́ntə` → `ɒ́ntùw`, `ɪ́nsàjd` → `ɪnsájd`). Three dropped segments were also restored (`kájd` → `kájnd`, `stréjnər` → `stréjndʒər`, `dɪlɪ́brətij` → `dɪlɪ́brətlij`).

**Also valid:** leaving the drift in place. It survived a green validator and two full class sweeps (2026-09-27) precisely because none of it is mechanically visible — a wrong stress accent, a missing grave and a missing consonant all produce legal tokens.

**Why the author has to rule on some of it.** The `e` case is the zone the guide already declares word by word, and the audit found the corpus split *inside itself* there: `ɪ̀ndəpɛ́ndənt` ×7 in `examples/` against `ɪ̀ndɪpɛ́ndənt` ×5 in AI-103, `əfɪ́ʃənsij` ×6 against `ɪfɪ́ʃənsij`, `ɪ̀ntəɡréjʃən` ×16 against `ɪ̀ntɪɡréjʃən` ×1. Both sides cannot be right, and the two rules that could settle it (M-W's schwa, the `ɪ` default) point opposite ways — so the 2026-09-28 rulings on *relevant*, *independent*, *efficiency*, *intelligence* and the *integrat-* family are recorded per word in the ledger, and the general rule stays open.

**Per-word rulings against a derivation, in both directions (2026-09-28).** *genuine* is `dʒɛ́njuwɪn`, not M-W's first listing `ˈjen-yə-wən`; *comfortable* is `kə́mftərbəl`, not M-W's `ˈkəm(p)-fər-tə-bəl`; *accountability* is `əkàwntəbɪ́lɪtij`, which reverses the shape the 2026-09-26 `-ible` sweep had written; *complex* (adjective) follows M-W's first listing `käm-ˈpleks` while the corpus had used the noun-like stress; *technology* loses a grave; *accessibility* takes the `əks-` of *accessible* rather than the `æ̀ks-` of *access*. Each is a ledger entry, following the *danger* and *general* precedent: a word ruled against its own derivation must be recorded, or a later reader applying the rule will "fix" it back.

**Not swept, and why.** The reduced-prefix follow-up (the *represent* family, 50 tokens) and the `(-ə)r` bucket are the two standing items in `pending-decisions.md`; the audit re-confirmed them but added nothing.

**Second batch — the four items the audit had deferred, ruled the same day (44 tokens).** *metadata* `mɛ́tədèjtə` → `mɛ̀tədéjtə` (×31, AI-103): the author chose M-W's `ˌme-tə-ˈdā-tə` over the widespread first-syllable stress, so *this* word is derived rather than ruled, unlike the per-word list above. *inside*: the corpus split between `ɪnsájd` and `ɪ̀nsájd`, and since M-W's `(ˌ)in-ˈsīd` parenthesizes the secondary stress both are licensed — the author picked `ɪ̀nsájd`, so the 8 examples tokens were swept (the earlier pass had only fixed `ɪ́nsàjd`, whose acute was on the wrong syllable). *genuinely* stays `dʒɛ́njuwənlij`, ruled separately from the adjective `dʒɛ́njuwɪn` rather than harmonised with it. And the last three `e`-case words were closed on the e-rule default, "made consistent across the corpus": *inconsequential* `ɪ̀nkɒ̀nsɪkwɛ́nʃəl`, *modest* `mɒ́dɪst` / *modestly* `mɒ́dɪstlij`, *specifically* `spɪsɪ́fɪklij` — each matching a related form the corpus already wrote (`spɪsɪ́fɪk` ×14). Ledger 524 → 528 entries (the *genuinely* entry already existed and agreed, so it was left alone).

**Two tokens the author caught directly (2026-09-28).** *comfortably* was `kə́mfərtəblij`; the adverb is `kə́mftərblij`, which is what M-W's *first* listing already says (`ˈkəm(p)(f)-tər-blē`, the `-tə-` and `-fər-` shapes being variants listed after it) and what the compressed *comfortable* `kə́mftərbəl` predicts — so that one is derived, not ruled. *brilliant* was `brɪ́ljənt`, and there the author ruled against M-W's single listing `ˈbril-yənt` in favour of writing the medial `i`: `brɪ́lijənt`, the §4.5 link shape `brɪ́l` + `ij` + `ənt` (compare *area* `ɛ́rijə`, *material* `mətɪ́rijəl`). Both are ledger entries; the second raises a class question — the same spelled-`i` shape in *million*, *billions*, *trillion*, *opinion*, *companion*, *familiar* and *resilience* - which is parked in `pending-decisions.md` §7 rather than swept on a guess. `TRN_ONE.txt` was regenerated with the notebook's own transform (225403 → 225402 bytes, 297 lines / 23997 tokens) after proving the pre-edit file equalled that transform of the pre-edit `examples/`.

---

*If you disagree with a choice here, the guide's machine-checkable constraints (§11) make it safe to fork: change the rule, update the validator to match, and your corpus stays internally consistent.*
