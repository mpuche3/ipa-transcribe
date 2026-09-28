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

## 6. Reduced `e` — ɪ or ə (no general rule yet)
**Status:** the words ruled so far are applied; the *rule* is not settled.
**2026-09-28 additions (ruled and swept):** *relevant* / *relevance* `rɛ́lɪv-`, *independent* /
*independently* `ɪ̀ndɪp-`, *efficient* / *efficiency* / *efficiently* `ɪfɪ́ʃ-`, *inefficient*
`ɪ̀nɪfɪ́ʃ-`, *intelligence* `ɪntɛ́lɪdʒəns` (also dropping the spurious grave on `in-`), and the
*integrat-* family `ɪ̀ntɪɡr-`, *inconsequential* `ɪ̀nkɒ̀nsɪkwɛ́nʃəl`, *modest* `mɒ́dɪst` / *modestly*
`mɒ́dɪstlij`, *specifically* `spɪsɪ́fɪklij`. All keep the `ɪ` default; the first four were split
between the two corpora, the *integrat-* family was uniform `ə` in AI-103 (27 tokens) against a
6-to-3 `ɪ` majority in `examples/`, and the last three were single deviating tokens closed on the
rule so the corpus stays uniform. Each word has a ledger entry. **Also resolved off this file:**
*metadata* (now `mɛ̀tədéjtə`, M-W's `ˌme-tə-ˈdā-tə`), *inside* (unified on `ɪ̀nsájd`) and *genuinely*
(kept `dʒɛ́njuwənlij`, ruled separately from the adjective `dʒɛ́njuwɪn`).
The 2026-09-27 sweep reads a reduced `e` like `i`/`y` (→ `ɪ`, keeping `ə` before
`r l n m ŋ t`, with `t` added after the author rejected 15 forms: *market* `mɑ́rkət`,
*ticket* `tɪ́kət`, *benefit* `bɛ́nɪfət`). The author's ruling of the same day is that no clear rule
can be stated from this corpus, because M-W disagrees with the default in **both** directions:
`sɪ́nθɪsɪs` / `nɛ̀sɪsɛ́rɪlij` (rule `ɪ`, M-W `ˈsin(t)-thə-səs` / `ˌne-sə-ˈser-ə-lē`) against
`dɛ́fɪnɪt` (rule `ɪ` for a spelled `i`, M-W `ˈde-fə-nət`), while *hundred* `hə́ndrəd` and
*market* `mɑ́rkət` take a schwa on both readings.
**In force today:** only the **ə half** of the default is machine-checked, in paired mode — a reduced `e` before
`r l n m ŋ t` must be `ə` (`check_e_reduction()`); the **ɪ half is practice**, kept behind
`E_ENFORCE_KIT = False` in the validator, with the per-word rulings recorded in the ledger and §13. The three
corpus words realigned to the default are `sɪ́nθɪsɪs`, `hajpɒ́θɪsɪs` and `nɛ̀sɪsɛ́rɪlij`.
**Needed:** once the corpus is larger, restate the rule from the corpus — or drop the default and
keep the ledger as a pure per-word register.

## 7. The spelled-`i` shape in *brilliant* - one word or a class?
**Status:** *brilliant* was corrected by the author on 2026-09-28 from `brɪ́ljənt` to `brɪ́lijənt`.
That writes the medial `i` as the §4.5 glide link (`brɪ́l` + `ij` + `ənt`,
as in *area* `ɛ́rijə`, *material* `mətɪ́rijəl`). M-W's only listing is the
two-syllable `ˈbril-yənt`, so the correction is a ruling against the dictionary rather than a
derivation from it — and the shape recurs **19 times** in `examples/` (10 distinct forms, 13 files),
always without the `i`:

| corpus form | source words | tokens |
| --- | --- | --- |
| `fəmɪ́ljər` / `ə̀nfəmɪ́ljər` | *familiar* / *unfamiliar* | 8 |
| `mɪ́ljən` / `mɪ́ljənz` | *million* / *millions* | 4 |
| `bɪ́ljənz` (+ `fɔ́r-bɪ́ljən-dɒ́lər`) | *billions* | 3 |
| `trɪ́ljən` | *trillion* | 1 |
| `əpɪ́njən` | *opinion* | 1 |
| `kəmpǽnjən` | *companion* | 1 |
| `rɪzɪ́ljəns` | *resilience* | 1 |

M-W is uniform across all of them — `ˈmi(l)-yən`, `ˈbil-yən`, `ˈtril-yən`,
`fə-ˈmil-yər`, `ri-ˈzil-yəns`, `ə-ˈpin-yən`, `kəm-ˈpan-yən` —
one listing each, always consonant + `y`, never a written vowel of its own. (Words whose `ə`-glide
comes from a spelled `u` — *valuable* `vǽljəbəl`, *volume* `vɒ́ljəm`,
*particular*, *regular*, *argument* - are a different question and are NOT part of this item; nor is
*convenient* `kənvɪ́jnjənt`, where M-W itself writes the FLEECE `ē`.)

**Needed:** is `brɪ́lijənt` a one-word ruling (the author's own pronunciation has the extra syllable)
or a class rule for every word that spells `i` between a consonant and a vowel? If it is a class rule, the
sweep is 19 tokens in 11 files, plus a §4.5 guide amendment and a ledger entry per family member.

---

## Housekeeping (not decisions)
- The skill checkout `C:\Users\mpuch\.claude\skills\ipa-transcribe` is a second checkout of this
  repository and must be `git pull --ff-only`-ed after every push, or the skill runs on an old guide.
