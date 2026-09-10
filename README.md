# Imagines Coronatae

A machine-readable catalogue of **sacred images crowned under papal authority**, compiled from a
complete sweep of the official gazettes of the Holy See published on vatican.va:
*Acta Sanctae Sedis* (ASS, 1865–1908) and *Acta Apostolicae Sedis* (AAS, 1909– ).

| Where | What |
|---|---|
| [`registry/by-country.md`](registry/by-country.md) | Browsable registry, grouped by country |
| [`registry/chronological.md`](registry/chronological.md) | Browsable registry, ordered by date of crowning |
| [`data/imagines-coronatae.json`](data/imagines-coronatae.json) | Full dataset (validated against `schema/`) |
| [`data/imagines-coronatae.csv`](data/imagines-coronatae.csv) | Same records, flat |

## What is in it

**400 records** covering **333 distinct localities** in **42 countries**,
drawn from **147,576 pages** across **440 volume PDFs**
(ASS 1–41, 1865–1908; AAS 1–118, 1909–2026).

Crownings recorded run from **1645 to 2001** — far earlier than the gazettes
themselves, because a later act often recites when an image was first crowned.

By evidence type:

| Type | Records |
|---|---|
| `retrospective_attestation` | 233 |
| `papal_coronation_act` | 102 |
| `papal_personal_coronation` | 47 |
| `papal_legate_deputation` | 16 |
| `norms` | 2 |

By series: ASS 14, AAS 386.

Most-represented countries:

| Country | Records |
|---|---|
| Italy | 120 |
| Poland | 67 |
| Mexico | 32 |
| Spain | 25 |
| France | 23 |
| Colombia | 12 |
| Belgium | 10 |
| Argentina | 10 |
| Venezuela | 8 |
| Brazil | 8 |
| Portugal | 8 |
| Philippines | 7 |

Confidence: 242 high, 152 medium, 6 low.
`medium` usually means the country was inferred from the Latin name of the diocese rather than
stated outright; every such case says so in `notes`.

## What "crowned under papal authority" means here

Coronation of an image is a papal act, but it reaches the gazettes in several shapes. Each record
carries an `evidence_type` so you can filter to exactly the sense you need:

| `evidence_type` | Meaning |
|---|---|
| `papal_coronation_act` | The act itself grants or permits the coronation — *"pretioso diademate redimiri sinitur"*. |
| `papal_legate_deputation` | The Pope deputes a Cardinal or Bishop to crown the image in his name. |
| `papal_personal_coronation` | The act records that the Pope crowned the image himself. |
| `retrospective_attestation` | A *different* act (typically a Basilica Minor elevation or a patron declaration) states in passing that the image was crowned, often *"ex decreto Capituli Vaticani"*. |
| `norms` | General legislation on crowning images. |

## Important limits — please read before citing

1. **This is not a global census.** For most of the period covered, the crowning of an image was
   decreed by the **Chapter of St Peter's Basilica** (*Capitulum Vaticanum*) and never published in
   either gazette. What this dataset documents is what ASS and AAS attest — a well-defined and
   citable subset.
2. **The Chapter's own archives were not consulted.** The Archivio del Capitolo di San Pietro is not
   published online; vatican.va's archive section carries only the Bible, Catechism, Codes of Canon
   Law, Councils and the official acts. Those archives remain the principal unexamined source, both
   for coronations before 1909 and for many after it.

   *A concrete case.* **Our Lady of Altagracia** (Higüey, Dominican Republic), patroness of the
   country, is generally said to have been crowned on 15 August 1922 under Pius XI. **AAS volumes
   14 (1922), 15 (1923) and 16 (1924) do not mention Altagracia, Higüey or the Dominican Republic
   at all** — nor does the 1959 Apostolic Constitution erecting the diocese of Higüey
   (AAS 51, 688) recite any crowning. That coronation is simply not in the gazette; its record lies
   in the Chapter's archives. What AAS *does* preserve is a later papal act: see below.
3. **1973 is a watershed.** The *Normae circa patronos constituendos et imagines B. M. Virginis
   coronandas* of 25 March 1973 (AAS 65, 276) reshaped the practice; from 1974 the acts appear as
   *Litterae Apostolicae* granting the faculty to crown, and they are numerous.
4. **A rule worth knowing.** ASS 41 (1908), 621 records Pius X's ruling that images of the **Sacred
   Heart** are not to be crowned — a crown may only be laid at the statue's feet. That explains the
   near-absence of Sacred Heart coronations in the record.
5. **The sources are OCR scans**, and ASS is markedly rougher than AAS. Place names are frequently
   mangled. Every record keeps the **verbatim Latin rubric and incipit** and carries a `confidence`
   value. Anything marked `low`, or carrying a `notes` field, should be checked against the printed
   page before being treated as authoritative.
6. Several ASS volumes span two calendar years; `year` is the first year of the volume.

## A note on borderline cases: San Giovanni Rotondo

The inclusion bar for this catalogue is that an image was crowned **under papal authority** — by a
papal act, by a Legate deputed for it, by the Pope in person, or by decree of the Vatican Chapter
acting on a papal indult. One case sits just outside that line and is worth recording explicitly,
because it shows both what the bar excludes and what the gazettes incidentally preserve.

**ASS 36 (1903–04), 226–231** — *Sypontina, Iurium*, a case decided by the Sacred Congregation of
the Council on 18 July 1903. It is a property dispute at **San Giovanni Rotondo**, in the
archdiocese of Siponto (Manfredonia), between Canon Michele Limongelli and the Confraternity of
the Blessed Sacrament at the church of St Catherine, over who owned certain sacred furnishings —
a silver monstrance, a **silver crown**, a chalice veil, a manuscript ledger, and a statue of
St Agnes.

The crowning surfaces only as evidence about the crown's ownership. At p. 230 the confraternity
argues that the canon had himself acknowledged the crown was bought with the faithful's offerings,
saying so *"dum functionem peragebat solemnem apponendi coronam fronti sacrae imagini"* — while he
was performing the solemn function of placing the crown on the forehead of the sacred image — and
that he had called himself the faithful's mandatary *"in apponenda hac corona in fronte B. M.
Virginis"*.

So a solemn crowning of a Marian image at San Giovanni Rotondo is genuinely attested. But the
record names **no papal authority and no Chapter decree**, gives **no date** for the crowning, and
does **not name or title the image**; the coronation is incidental to a lawsuit about a piece of
silver. It is therefore **not** in the dataset. It is noted here so that the omission is a recorded
judgement rather than a silent gap — and because it is a reminder that the Congregational
jurisprudence in ASS and AAS carries evidence of local crownings that a search for coronation
decrees will never surface.

## Record shape

```json
{
  "series": "AAS",
  "volume": 91,
  "year": 1999,
  "page": 345,
  "act_number": "V",
  "act_type": "Litterae Apostolicae",
  "pope": "Ioannes Paulus PP. II",
  "citation": "AAS 91 (1999), p. 345",
  "evidence_type": "papal_coronation_act",
  "rubric_latin": "Imago beatae Mariae Virginis titulo «Nostra Seynora de Canòlich» invocatae ... pretioso diademate redimiri sinitur «nomine et auctoritate Summi Pontificis».",
  "incipit_latin": "In antiquo oppido Andorrae Principatus «Sant Julia de Loria» ...",
  "image_title_vernacular": "Nostra Senyora de Canòlich",
  "locality": "Sant Julià de Lòria",
  "diocese_latin": "Urgellensis",
  "country": "Andorra",
  "act_date": "1998-12-07",
  "confidence": "high"
}
```

## Recall check

An independent audit swept the corpus for the unambiguous act-granting formulas
(*redimiri sinitur*, *coronam apponendam*, *facultas conceditur … coronandi*, *coronasse imaginem*,
*redimiendi serto*, and others) and collected every page on which one occurs. Excluding
back-of-volume index pages, **47 of 48** such act pages are represented; the one exception is an
index entry whose underlying act (Our Lady of Fátima, AAS 38, 376) *is* included.

Three systematic traps were found and fixed during the build, and are worth knowing if you extend
this work.

1. The act rubric switches from ALL-CAPS to lowercase italic around 1970, so a caps-based parser
   goes blind on everything after it.
2. The OCR hyphenates words across line breaks (`pretioso dia-\ndemate redimiat`), hiding the key
   terms from a naive search. De-hyphenating the corpus recovered 96 passages.
3. **Requiring a word for "image" near the coronation word.** This looks like a safe precision
   filter and is not: a papal act often names the devotion by its **title** alone. It dropped
   **AAS 71 (1979), 158**, where John Paul II, preaching at Santo Domingo on 25 January 1979, says
   of *Nuestra Señora de la Altagracia* that *"el Papa quiere dejar como homenaje de devoción una
   diadema"* — no word for image anywhere near it. Re-triaging the 348 passages that filter had
   rejected recovered that record and several more, among them the diadem presented at Guadalupe
   two days later (AAS 71, 177), the Virgen del Carmen de Maipú (AAS 66, 727), and the Virgen de la
   Caridad del Cobre, of which the Pope later recalled *"el momento en que le ceñí la corona que sus
   hijos le ofrecieron"* (AAS 91, 105).

## Reproducing

| Script | Does |
|---|---|
| `scripts/fetch_aas.sh` | Downloads all AAS PDFs and verifies each against its `Content-Length`. |
| `scripts/fetch_ass.sh` | The same for the 41 ASS volumes. |
| `scripts/extract_text.py` | Extracts the text layer of every PDF, with page markers. |
| `scripts/find_passages.py` | De-hyphenates and sweeps for coronation vocabulary; emits candidate passages. |
| `scripts/find_passages_vernacular.py` | Second sweep for Italian, Spanish, French, Polish and German coronation terms. |
| `scripts/merge.py` | Merges and de-duplicates the per-batch extraction output by locality. |
| `scripts/build_dataset.py` | Assembles the dataset with metadata and statistics. |
| `scripts/build_registry.py` | Renders the two registry tables from the dataset. |

The reading-and-structuring step between the sweep and the merge was performed by parallel LLM
agents against the specifications in `docs/EXTRACTION_SPEC.md` and `docs/EXTRACTION_SPEC_ASS.md`.

## Licence

The underlying ASS and AAS texts are © Libreria Editrice Vaticana. This compilation is offered for
research use.
