# Imagines Coronatae

A machine-readable catalogue of **sacred images crowned under papal authority**, compiled from a
complete sweep of the official gazettes of the Holy See — *Acta Sanctae Sedis* (ASS, 1865–1908) and
*Acta Apostolicae Sedis* (AAS, 1909– ) — and from the one digitized volume of the Vatican Chapter's
own coronation dossiers, *Madonne coronate*, tomo IV (1689–1714) — plus, kept visibly distinct, thirty
coronations reported by Vrabelová's 2013 study of the same archive.

| Where | What |
|---|---|
| [`registry/by-country.md`](registry/by-country.md) | Browsable registry, grouped by country |
| [`registry/chronological.md`](registry/chronological.md) | Browsable registry, ordered by date of crowning |
| [`data/imagines-coronatae.json`](data/imagines-coronatae.json) | **The catalogue** — one record per image, each carrying all its sources |
| [`data/imagines-coronatae.csv`](data/imagines-coronatae.csv) | One row per image, flat |
| [`data/attestations.json`](data/attestations.json) | The evidence layer — one record per *act* in ASS/AAS |
| [`data/attestations-acsp.json`](data/attestations-acsp.json) | The evidence layer for the Chapter archive — one record per *dossier* in Madonne coronate IV |
| [`data/attestations-lit.json`](data/attestations-lit.json) | Secondary literature — coronations *reported*, not read at first hand, each with the author's archival citation |
| [`data/sources.csv`](data/sources.csv) | One row per (image, source) pair |

## What is in it

**416 crowned images** in **42 countries**, documented by **495 source citations**:
400 from **147,576 pages** of the two gazettes (ASS 1–41, 1865–1908; AAS 1–118, 1909–2026);
34 from the **713 transcribed folios** of *Madonne coronate* IV — the Chapter's dossiers for
34 images crowned between 1689 and 1716, only three of which the gazettes ever mention; and
61 from **secondary literature** — Vrabelová 2013 on Central Europe 1717–1786 and Balzamo 2023 on Italy
and Rome 1631–1798 — reporting coronations from volumes of the same archive that are not online.

53 images are attested by more than one act — the most-cited is Our Lady of Guadalupe, with seven.
Crownings run from **1645 to 2001**, far earlier than the gazettes themselves,
because a later act often recites when an image was first crowned.

By strongest evidence available for each image:

| Type | Images |
|---|---|
| `retrospective_attestation` | 181 |
| `papal_coronation_act` | 101 |
| `chapter_decree` | 88 |
| `papal_personal_coronation` | 28 |
| `papal_legate_deputation` | 15 |
| `norms` | 2 |

Most-represented countries:

| Country | Images |
|---|---|
| Italy | 99 |
| Poland | 64 |
| Spain | 24 |
| Mexico | 23 |
| France | 21 |
| Colombia | 11 |
| Belgium | 9 |
| Argentina | 7 |
| Philippines | 7 |
| Brazil | 6 |
| Ecuador | 5 |
| Peru | 5 |

Confidence: 215 high, 119 medium, 5 low.
`medium` usually means the country was inferred from the Latin name of the diocese rather than
stated outright; every such case says so in the source's `notes`.

## One record per image, not per act

An image crowned once may be mentioned in a dozen later acts. **Nossa Senhora da Conceição
Aparecida** is recited in AAS 23 (1931), AAS 46 (1954) and AAS 59 (1967) — that is one image with
three sources, not three crowned images. So each record here is an **image**, and every act
attesting it is kept in that record's `sources` array. Nothing is discarded by consolidation:
400 source citations sit inside 339 image records, and `data/attestations.json` still holds
the flat act-level layer if you want it.

**Images crowned more than once.** `coronation_dates` is an array, and where it holds more than
one date the image really was crowned again — typically a Vatican Chapter crowning later renewed by
a Pope. 6 images in the catalogue were crowned more than once:

| Image | Crowned |
|---|---|
| Madonna del Rosario di Fontanellato — Fontanellato, Italy | 1660, 1925 |
| Nostra Signora di Bonaria — Cagliari (Calaris), Italy | 1870-04-24, 1926 |
| Onze-Lieve-Vrouw van Scherpenheuvel (Notre-Dame de Montaigu) — Scherpenheuvel (Aspricollis), near Leuven, Belgium | 1872, 1927 |
| Nuestra Señora de Guadalupe — Mexicopolis (Mexico City), Mexico | 1895-10-12, 1945-10-12, 1979-01-27 |
| Notre-Dame du Cap — Cap-de-la-Madeleine, Canada | 1904, 1954 |
| Nuestra Señora de Coromoto — Guanare, Venezuela | 1952-09-12, 1985-01-27 |

Dates are collapsed by precision first: one source giving `1954` and another `1954-08-29` is a
single crowning recorded at two levels of detail, not two, so only the fuller form is kept. Distinct
years stay distinct — which is what makes a multi-entry list mean something.

**How images are identified.** By **place first**, then title. Marian titles repeat all over the
world — there are seven distinct *Nuestra Señora de Guadalupe* here, in Mexico, Spain, Venezuela and
El Salvador — so a shared title is never on its own evidence of a shared image. Two records are the
same image when they name the same locality *and* carry compatible titles. An earlier build also
merged on a "distinctive" shared title across different localities; it was removed after it fused
Notre-Dame des Miracles at Rennes with Mauriac, the Carmine *la Bruna* at Naples with Matera, and
the four separate images John Paul II crowned together at Jasna Góra. **A false merge destroys a
distinct image; a false split merely leaves a duplicate — so the matching errs toward splitting.**
Titles are also stripped of *descriptive* words before comparison. Latin acts praise an image as
much as they name it, and adjectives like *perinsigne*, *thaumaturga* or *veneranda* are not
identity. Leaving them in kept Notre-Dame du Cap as two records — one act called it
*Simulacrum B. M. V. a Rosario*, another *perinsigne Virginis simulacrum* — for a single shrine
crowned in 1904 and again in 1954. Where an act's title reduces to nothing but praise, the shared
locality and subject carry the identification, and a record is merged only if exactly one cluster at
that place fits. Subjects never cross: a St Joseph is never merged into a Marian image.

Residual duplicates are possible where a source names no locality at all, or where two acts
describe one image in words too different to match. One such pair is left open deliberately:
**Piekary Śląskie** ([issue #1](https://github.com/CatholicOS/imagines-coronatae/issues/1)), where
AAS 55 (1963), 225 records a crowning *Pii Pp. XI permissu* and AAS 111 (2019), 1343 records August
Hlond crowning the Piekary image as Apostolic Administrator — almost certainly the same event, but
neither act gives a date or names the other, so the merge would be inference rather than evidence.
It waits on the Chapter archives.

## Primary and secondary sources are kept apart

Every source carries a `series`: **ASS** and **AAS** (the gazettes) and **ACSP** (the Chapter's
dossiers) were **read at first hand** for this catalogue. **LIT** is different: it marks a coronation
**reported by a scholarly work** and not read here — at present Dana Vrabelová's 2013 dissertation
(thirty Chapter coronations in Central Europe, 1717–1786, § XXI) and Nicolas Balzamo's 2023 article
(Roman and Italian coronations 1631–1798), each row cited to *BAV, ACSP, Madonne coronate, volume,
folio* where the author gives one. Those citations are carried in `register_refs`, so
every LIT row can be taken back to the primary dossier; until it is, its confidence is capped at
`medium` (`low` where she cites no folio). The rows are in `data/vrabelova-2013-table-xxi.json` and
`data/balzamo-2023-crownings.json`. Rows that name only a town and a year are kept **standalone** —
they are not merged into any named image, because a town and a year do not identify one.

Why keep the distinction visible: in the one place her account could be checked against a dossier
read here, it was wrong — she dates Trsat to 21 March 1715; the instrument says 14 September, the
letters say 8 September. Secondary reports are valuable and mostly right, but they are not the
same kind of evidence.

## What "crowned under papal authority" means here

Coronation of an image is a papal act, but it reaches the gazettes in several shapes. Each record
carries an `evidence_type` so you can filter to exactly the sense you need:

| `evidence_type` | Meaning |
|---|---|
| `papal_coronation_act` | The act itself grants or permits the coronation — *"pretioso diademate redimiri sinitur"*. |
| `papal_legate_deputation` | The Pope deputes a Cardinal or Bishop to crown the image in his name. |
| `papal_personal_coronation` | The act records that the Pope crowned the image himself. |
| `retrospective_attestation` | A *different* act (typically a Basilica Minor elevation or a patron declaration) states in passing that the image was crowned, often *"ex decreto Capituli Vaticani"*. |
| `chapter_decree` | The Chapter of St Peter's own dossier under the Sforza Pallavicino legacy: petition, decree of concession, instrument of donation of the crowns, and the *relazione* of the ceremony. From *Madonne coronate* IV. |
| `norms` | General legislation on crowning images. |
| `petition_not_conceded` | A petition to the Chapter that was refused or never granted — the image was **not** crowned by it. One case so far: Żabbar, Malta, c. 1700. |

## Important limits — please read before citing

1. **This is not a global census.** For most of the period covered, the crowning of an image was
   decreed by the **Chapter of St Peter's Basilica** (*Capitulum Vaticanum*) and never published in
   either gazette. What this dataset documents is what ASS and AAS attest — a well-defined and
   citable subset.
2. **The Chapter's own archives are a separate source, only fractionally online.** For three
   centuries the crowning of an image was granted by decree of the **Chapter of St Peter's
   Basilica**, under the 1636 Sforza Pallavicino legacy, and those decrees were never gazetted. The
   dedicated series is **`Madonne coronate`**, cited as *BAV, ACSP, Madonne coronate, tomo I, foglio
   N (mecc. N)*. Exactly **one volume of it is digitized** —
   [`Arch.Cap.S.Pietro.Madonne.coron.4`](https://digi.vatlib.it/view/ARC_Arch.Cap.S.Pietro.Madonne.coron.4),
   726 images, not OCR'd. Everything else must be consulted at the Vatican Library or at the
   Archivio Capitolare. **That one volume has now been transcribed and swept** (`chapter_decree`
   records, cited by folio); the other tomes remain the largest unexamined source. See
   [`docs/CHAPTER-ARCHIVES.md`](docs/CHAPTER-ARCHIVES.md) for the series layout, the citation form,
   the petition procedure and what each coronation deposited.

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
  "id": "nossa-senhora-da-conceicao-aparecida-aparecida",
  "image_title_vernacular": "Nossa Senhora da Conceição Aparecida",
  "image_subject": "Blessed Virgin Mary",
  "locality": "Aparecida",
  "country": "Brazil",
  "coronation_dates": ["1904"],
  "first_coronation": "1904",
  "strongest_evidence": "retrospective_attestation",
  "confidence": "high",
  "source_count": 3,
  "sources": [
    {
      "series": "AAS", "volume": 23, "year": 1931, "page": 7,
      "citation": "AAS 23 (1931), p. 7",
      "evidence_type": "retrospective_attestation",
      "pope": "Pius PP. XI",
      "act_date": "1930-07-16",
      "coronation_date": "1904",
      "rubric_latin": "...", "incipit_latin": "...",
      "confidence": "medium",
      "notes": "Patron-declaration act; states the simulacrum was crowned 'decreto Capituli sacrosanctae Patriarchalis Vaticanae Basilicae'..."
    }
  ]
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
| `scripts/build_dataset.py` | Assembles the act-level evidence layer, `data/attestations.json`. |
| `scripts/build_acsp.py` | Turns the *Madonne coronate* IV extraction into `data/attestations-acsp.json`. |
| `scripts/build_lit.py` | Turns the secondary-literature table into `data/attestations-lit.json`. |
| `scripts/build_images.py` | Consolidates acts into one record per image, with `sources`. |
| `scripts/build_registry.py` | Renders the two registry tables from the catalogue. |

The reading-and-structuring step between the sweep and the merge was performed by parallel LLM
agents against the specifications in `docs/EXTRACTION_SPEC.md`, `docs/EXTRACTION_SPEC_ASS.md` and,
for the Chapter dossiers, `docs/EXTRACTION_SPEC_ACSP.md`.

## Licence

The underlying ASS and AAS texts are © Libreria Editrice Vaticana. This compilation is offered for
research use.
