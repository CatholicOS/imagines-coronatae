# ASS addendum to SPEC.md

Read `SPEC.md` first — it defines everything. This file states only what differs for
**Acta Sanctae Sedis (ASS, 1865–1908)**, the predecessor gazette to AAS.

## Differences

1. **Set `"series": "ASS"`** on every record you emit. (AAS records carry `"series": "AAS"`.)
   Use the field names `volume`, `year`, `page` — NOT `aas_volume`/`aas_year`/`aas_page`.
   Everything else in the schema is unchanged.

2. **The OCR is markedly worse than AAS.** ASS volumes are older type, and the text layer
   contains many artefacts (`ä`, `á`, `ö` for ordinary vowels; `iprod` for `quod`;
   `subsequüta` for `subsecuta`; running heads garbled). Expect to repair more, and to set
   `confidence` lower more often. Keep the raw reading in `notes` whenever you repair one.

3. **Volume/year mapping is irregular.** Several ASS volumes span two years
   (e.g. ASS 1 = 1865–66, ASS 5 = 1869–70). The `year` given in each passage is the first
   year of the volume. If the act's own `Datum` line gives a different year, trust the act
   and say so in `notes`.

4. **What coronation material looks like in this period.** In the 19th century the crowning
   of an image was overwhelmingly the business of the **Chapter of St Peter's Basilica**
   (*Capitulum Vaticanum*), acting under a papal indult. So expect:
   - decrees or notices citing *ex decreto Capituli Vaticani* / *Capitulo Vaticano*;
   - papal **Briefs** (*Breve*) granting the faculty to crown;
   - reports of the coronation ceremony itself;
   - retrospective mentions inside other acts, exactly as in AAS.
   Classify with the same `evidence_type` values as SPEC.md. Where the crowning is by the
   Chapter under papal authority, use `retrospective_attestation` unless the document you
   are reading IS the granting act, in which case use `papal_coronation_act`.

5. **`sertum`** (garland/wreath) is used for a crown in this period as well as
   *corona* and *diadema*. Treat it as a coronation when applied to a sacred image.

6. Much of ASS is Roman-Curia business (dispensations, canon-law responses, seminary
   decrees) that merely uses the word *corona* in passing. Be as strict as in AAS.
