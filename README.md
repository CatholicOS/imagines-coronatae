# Imagines Coronatae

A machine-readable catalogue of **sacred images crowned under papal authority**, compiled from a
complete sweep of *Acta Apostolicae Sedis* (AAS) as published on vatican.va.

The dataset is `data/imagines-coronatae.json`, validated against `schema/imagines-coronatae.schema.json`.

## What this is

Every AAS volume from **1909 to 2026** was downloaded, its text layer extracted, and the whole
corpus searched for the Latin and vernacular vocabulary of image-coronation. Each candidate passage
was then read and turned into a structured record citing **volume, year, printed page, act number,
the act's Latin rubric and incipit**, and the image's title, place and country.

## What is in it

**379 records** covering **321 distinct localities** in **40 countries**,
drawn from **117,555 pages** across **399 AAS PDF files** (volumes 1–118, 1909–2026).

By evidence type:

| Type | Records |
|---|---|
| `retrospective_attestation` | 222 |
| `papal_coronation_act` | 99 |
| `papal_personal_coronation` | 41 |
| `papal_legate_deputation` | 16 |
| `norms` | 1 |

By pope: Ioannes Paulus PP. II (125), Pius PP. XII (91), Pius PP. XI (47), Paulus PP. VI (40), Ioannes PP. XXIII (32), Benedictus PP. XV (26), Pius PP. X (14), Franciscus PP. (2), Benedictus PP. XVI (1).

Most-represented countries:

| Country | Records |
|---|---|
| Italy | 113 |
| Poland | 67 |
| Mexico | 29 |
| Spain | 25 |
| France | 19 |
| Colombia | 12 |
| Argentina | 10 |
| Belgium | 9 |
| Venezuela | 8 |
| Brazil | 8 |
| Portugal | 8 |
| Philippines | 7 |

Confidence: 231 high, 142 medium, 6 low.
`medium` usually means the country was inferred from the Latin name of the diocese rather than
stated outright; every such case says so in `notes`.

### Recall check

An independent audit swept the corpus for the unambiguous act-granting formulas
(*redimiri sinitur*, *coronam apponendam*, *facultas conceditur … coronandi*, *coronasse imaginem*,
*redimiendi serto*, and others) and collected every page on which one occurs. Excluding
back-of-volume index pages, **47 of 48** such act pages are represented in the dataset; the one
exception is an index entry whose underlying act (Our Lady of Fátima, AAS 38, 376) *is* included.

## What "crowned under papal authority" means here

Coronation of an image is a papal act, but it reaches AAS in several different shapes. Each record
carries an `evidence_type` so you can filter to exactly the sense you need:

| `evidence_type` | Meaning |
|---|---|
| `papal_coronation_act` | The act itself grants or permits the coronation — *"pretioso diademate redimiri sinitur"*. |
| `papal_legate_deputation` | The Pope deputes a Cardinal or Bishop to crown the image in his name. |
| `papal_personal_coronation` | The act records that the Pope crowned the image himself. |
| `retrospective_attestation` | A *different* act (typically a Basilica Minor elevation or a patron declaration) states in passing that the image was crowned, often *"ex decreto Capituli Vaticani"*. |
| `norms` | General legislation on crowning images. |

## Important limits — please read before citing

1. **AAS is not the whole story.** For most of its history the crowning of an image was decreed by
   the **Chapter of St Peter's Basilica**, and those decrees were *not* published in AAS. What this
   dataset documents is what AAS attests — a well-defined and citable subset, not a global census
   of crowned images.
2. **AAS begins in 1909.** Earlier coronations (Leo XIII and before) appear here only where a later
   act mentions them. Their primary record is *Acta Sanctae Sedis* (1865–1908) and the Vatican
   Chapter's own archives.
3. **1973 is a watershed.** The *Normae circa patronos constituendos et imagines B. M. Virginis
   coronandas* of 25 March 1973 (AAS 65, 276) reshaped the practice; from 1974 the acts appear as
   *Litterae Apostolicae* granting the faculty to crown, and they are numerous.
4. **The sources are OCR scans.** Place names are frequently mangled. Every record therefore keeps
   the **verbatim Latin rubric and incipit** and carries a `confidence` value. Anything marked
   `low`, or carrying a `notes` field, should be checked against the printed page before being
   treated as authoritative.

## Record shape

```json
{
  "aas_volume": 91,
  "aas_year": 1999,
  "aas_page": 345,
  "act_number": "V",
  "act_type": "Litterae Apostolicae",
  "pope": "Ioannes Paulus PP. II",
  "aas_citation": "AAS 91 (1999), p. 345",
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

## Reproducing

Scripts are in `scripts/`, in pipeline order:

| Script | Does |
|---|---|
| `fetch_aas.sh` | Downloads all AAS PDFs from vatican.va and verifies each against its `Content-Length`. |
| `extract_text.py` | Extracts the text layer of every PDF, with page markers. |
| `find_passages.py` | Sweeps the corpus for coronation vocabulary and emits candidate passages. |
| `merge.py` | Merges and de-duplicates the per-batch extraction output. |
| `build_dataset.py` | Assembles the final dataset with metadata and statistics. |

The reading-and-structuring step between `find_passages.py` and `merge.py` was performed by
parallel LLM agents against the specification in `docs/EXTRACTION_SPEC.md`.

## Licence

The underlying AAS texts are © Libreria Editrice Vaticana. This compilation is offered for
research use.
