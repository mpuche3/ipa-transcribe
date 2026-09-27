# Pending decisions

Open questions that still need the author's ruling. Each item records the evidence and what a
sweep would cost; nothing in this file has been applied to the corpus. Last reviewed 2026-09-27.

## 1. Internal reduced `be- / de- / re- / pre- / se- / e- / ex-` prefixes — corpus follow-up
**Status:** the rule changed, the corpus did not follow yet.
§4.4 used to restrict the fixed prefixes to word-initial position. The author removed that
restriction on 2026-09-27, so a reduced prefix now takes `ɪ` wherever it sits — but the corpus
still writes `ə` in the internal cases, because that is what M-W's own listing of some of them
shows (for *represent*, literally `ˌre-pri-ˈzent`).

| family | corpus `ə` | corpus `ɪ` | M-W first listing |
| --- | --- | --- | --- |
| *represent* | 50 (`rɛ̀prəzɛ́ntətɪv` ×28, `rɛ̀prəzɛ́nts` ×9, `rɛ̀prəzɛntéjʃən(z)` ×4, …) | 5, all in AI-103 (`rɛ̀prɪzɛ́nt`, `rɛ̀prɪzɛ́nts`) | `ˌre-pri-ˈzent` |
| *reproduce / reproduction* | 5 (`rɛ̀prədə́ktɪv` ×3, `rɛ̀prədə́kʃən` ×2) | 0 | `ˌrē-prə-ˈdüs` |
| *undesirable* | 1 (`ə̀ndəzájərəbəl`) | 0 | `ˌən-di-ˈzī-rə-bəl` |

**Needed:** (a) a real morpheme audit of every internal reduced `be-`, `de-`, `re-`, `pre-`, `se-`,
`e-`, `ex-` prefix — the table above comes from a keyword scan, and the mechanical version of that
scan is noisy (`references` `rɛ́fərənsɪz` is correct, because *fer* is not a prefix); (b) then a
sweep with ledger entries per family. **Recommendation:** audit first and rule family by family —
*represent* alone is 50 tokens, and AI-103 is already split 5-to-32 on its own.

## 2. The `(-ə)r` bucket
28 words / 94 occurrences where the reduced schwa sits directly before `r`: *entire* `ɪntájər`,
*fire* `fájər`, *environments* `ɪnvájərənmənts`, *requires* `rɪkwájərz`. Deliberately left out of
the 2026-09-27 class sweeps because it is the syncope question, not the spelling question, and M-W
is inconsistent about it (`ˈfī(-ə)r` parenthesized, `ˈkäm-rə` compressed).
**Needed:** one ruling for the bucket as a whole.

## 3. §11 step 6 — consonant presence
The self-check bullet reads "every `r` from the spelling that is pronounced is present". The
dropped-consonant class is wider than `r`, and the validator cannot see it: `rájɪŋ` (dropped `t`),
`bájt` (dropped `y` in *byte*), `dɛ́lz` (dropped `v` in *delves*), `sədʒɛ́sts` (dropped `g` in
*suggests*) and `strájɪŋ` (dropped `k` in *striking*) all validate cleanly — the last two were found
and fixed on 2026-09-27, and a source-`k`/`ck` scan over the whole corpus found no third instance.
**Needed:** generalise the bullet from "every `r`" to "every consonant", with the audit recipe
(align source and transcription, diff the consonant letters of the source stem against the symbols
present, then discard the `ð`/`θ` and `-tion` → `ʃən` false positives).

## 4. `sə́bdʒɪkt` (*subject*)
M-W writes `ˈsəb-jikt` (plain `i`), but the spelling is `e`, so §4.4's spelling step gives `ə`.
The corpus writes `ɪ` in every token, so it was left as `ɪ` "for now" when the class was swept
(2026-09-20). The mirror case, *obstacle* `ɒ́bstəkəl`, was confirmed as `ə` because it is spelled
with `a`.
**Needed:** confirm `sə́bdʒɪkt` (or sweep to `sə́bdʒəkt`).

## 5. `Senghas` → `sɛ́ŋɡəs`
The surname in `TRN_NicaraguanSignLanguage.txt` was transcribed as `sɛ́ŋɡəs` from the spelling; no
source confirms the Nicaraguan pronunciation.
**Needed:** confirm the reading or leave it flagged.

## Housekeeping (not decisions)
- The skill checkout `C:\Users\mpuch\.claude\skills\ipa-transcribe` is a second checkout of this
  repository and must be `git pull --ff-only`-ed after every push, or the skill runs on an old guide.
