# Imagines Coronatae

A machine-readable catalogue of **sacred images crowned under papal authority**, compiled from a
complete sweep of the official gazettes of the Holy See — *Acta Sanctae Sedis* (ASS, 1865–1908) and
*Acta Apostolicae Sedis* (AAS, 1909– ) — and from the one digitized volume of the Vatican Chapter's
own coronation dossiers, *Madonne coronate*, tomo IV (1689–1714) — plus, kept visibly distinct, the
coronations reported by five secondary works on the same archive: Bombelli's illustrated *Raccolta*
of the crowned images of Rome (1792), Briccolani's printed register of 1800, the Zander/Magister
catalogue of the Fabbrica's painted copies (2011), Vrabelová's study of Central Europe (2013) and
Balzamo's of Italy (2023).

| Where | What |
|---|---|
| [`registry/by-country.md`](registry/by-country.md) | Browsable registry, grouped by country |
| [`registry/chronological.md`](registry/chronological.md) | Browsable registry, ordered by date of crowning |
| [`data/imagines-coronatae.json`](data/imagines-coronatae.json) | **The catalogue** — one record per image, each carrying all its sources |
| [`data/imagines-coronatae.csv`](data/imagines-coronatae.csv) | One row per image, flat |
| [`data/attestations.json`](data/attestations.json) | The evidence layer — one record per *act* in ASS/AAS |
| [`data/attestations-acsp.json`](data/attestations-acsp.json) | The evidence layer for the Chapter archive — one record per *dossier* in Madonne coronate IV |
| [`data/attestations-lit.json`](data/attestations-lit.json) | Secondary literature — coronations *reported*, not read at first hand, each with the author's archival citation |
| [`data/bombelli-1792-raccolta.json`](data/bombelli-1792-raccolta.json) | Transcription of Bombelli's 1792 *Raccolta*, tomi II–IV — 74 Roman images with the day of crowning, the crown's cost and the plate's caption |
| [`data/briccolani-1800-serie.json`](data/briccolani-1800-serie.json) | Transcription of Briccolani's 1800 *Serie* — the earliest printed register, 256 entries 1631–1793 |
| [`data/zander-magister-2011-catalogue.json`](data/zander-magister-2011-catalogue.json) | The 96 entries of the Zander/Magister 2011 catalogue, each with its dossier citation |
| [`data/basilici-bigliazzi-2025-db.json`](data/basilici-bigliazzi-2025-db.json) | The Basilici–Bigliazzi database of 1,737 crownings, 1631–1981 — **not merged**, used for the cross-match |
| [`docs/CROSSMATCH-BASILICI.md`](docs/CROSSMATCH-BASILICI.md) | The cross-match: what they record that this catalogue lacks, and the reverse (`data/crossmatch-basilici.csv` row by row) |
| [`data/sources.csv`](data/sources.csv) | One row per (image, source) pair |

## What is in it

**670 crowned images** in **43 countries**, documented by **939 source citations**:
400 from **147,576 pages** of the two gazettes (ASS 1–41, 1865–1908; AAS 1–118, 1909–2026);
34 from the **713 transcribed folios** of *Madonne coronate* IV — the Chapter's dossiers for
34 images crowned between 1689 and 1716, only three of which the gazettes ever mention; and
505 from **secondary literature** reporting coronations from volumes of the same archive that are
not online — 256 from Briccolani's register of 1800 (every Chapter coronation to 1791, by year),
81 from Bombelli's *Raccolta* of 1792 (74 Roman images with the day of the crowning, and seven
separate crowns for the Child), 107 from the Zander/Magister catalogue of 2011 (89 images with the day of crowning and the volume
and folios of the dossier), 30 from Vrabelová 2013 on Central Europe 1717–1786 and 31 from Balzamo
2023 on Italy and Rome 1631–1798.

195 images are attested by more than one source — the most-cited is Our Lady of Guadalupe, with
eight. Crownings run from **1500 to 2005**, far earlier than the gazettes themselves, because a
later act often recites when an image was first crowned. 304 images rest on secondary literature
alone; 115 of them on Briccolani's bare year and nothing else, and 63 more on Briccolani's year and
Bombelli's notice — nearly all of Rome.

By strongest evidence available for each image:

| Type | Images |
|---|---|
| `chapter_decree` | 363 |
| `retrospective_attestation` | 162 |
| `papal_coronation_act` | 100 |
| `papal_personal_coronation` | 27 |
| `papal_legate_deputation` | 15 |
| `norms` | 2 |
| `petition_not_conceded` | 1 |

Most-represented countries:

| Country | Images |
|---|---|
| Italy | 387 |
| Poland | 73 |
| Spain | 31 |
| France | 24 |
| Mexico | 23 |
| Belgium | 12 |
| Colombia | 11 |
| Ukraine | 11 |
| Argentina | 7 |
| Philippines | 7 |
| Brazil | 6 |
| Malta | 6 |

Confidence: 235 high, 216 medium, 219 low.
`medium` usually means either that the country was inferred from the Latin name of the diocese
rather than stated outright (every such case says so in the source's `notes`), or that the only
source is a secondary work citing the dossier by folio; `low` is almost always a register that
gives a year and nothing else.

## One record per image, not per act

An image crowned once may be mentioned in a dozen later acts. **Nossa Senhora da Conceição
Aparecida** is recited in AAS 23 (1931), AAS 46 (1954) and AAS 59 (1967) — that is one image with
three sources, not three crowned images. So each record here is an **image**, and every act
attesting it is kept in that record's `sources` array. Nothing is discarded by consolidation:
939 source citations sit inside 670 image records, and `data/attestations.json`,
`data/attestations-acsp.json` and `data/attestations-lit.json` still hold the flat record-level
layers if you want them.

**Images crowned more than once.** `coronation_dates` is an array, and where it holds more than
one date the image really was crowned again — typically a Vatican Chapter crowning later renewed by
a Pope. 26 images in the catalogue were crowned more than once, among them:

| Image | Crowned |
|---|---|
| Madonna della Febbre — Rome, Vatican sacristy | 1631-08-27, 1697-08-15 |
| Salus Populi Romani — Rome, Santa Maria Maggiore | 1597, 1954-11-01 |
| Madonna del Rosario di Fontanellato — Fontanellato, Italy | 1660, 1925 |
| Nostra Signora della Misericordia — Savona, Italy | 1770, 1815-05-10 |
| Nostra Signora dei Miracoli — Cicagna, Italy | 1790-09-14, 1814-09-14 |
| Vergine del Sacro Monte — Varallo, Italy | 1857-08-20, 1862-08-17 |
| Nostra Signora di Bonaria — Cagliari (Calaris), Italy | 1870-04-24, 1926-04-24 |
| Onze-Lieve-Vrouw van Scherpenheuvel (Notre-Dame de Montaigu) — Scherpenheuvel (Aspricollis), near Leuven, Belgium | 1872, 1927 |
| Nuestra Señora de Guadalupe — Mexicopolis (Mexico City), Mexico | 1895-10-12, 1945-10-12, 1979-01-27 |
| Notre-Dame du Cap — Cap-de-la-Madeleine, Canada | 1904, 1954 |
| Nuestra Señora de Coromoto — Guanare, Venezuela | 1952-09-12, 1985-01-27 |

Dates are collapsed by precision first: one source giving `1954` and another `1954-08-29` is a
single crowning recorded at two levels of detail, not two, so only the fuller form is kept. A bare
year from a register that is one year off a full date from a dossier is treated the same way —
a register often gives the year of the decree, the dossier the day of the ceremony (Lucca: decree
1689, crowned 30 April 1690). Distinct years otherwise stay distinct — which is what makes a
multi-entry list mean something. A crown for the **Child** of an image already crowned (Briccolani
lists twelve such *Bambino Gesù* concessions) is kept as a source on the image, linked to it by
`parent_act`, but is not counted as a re-crowning. Five of the 26 are source
disagreements rather than two ceremonies: Sant'Agostino in Rome (Briccolani 1641, Balzamo 1643),
Jarosław (Briccolani 1732, Vrabelová 1755-09-08), two Roman images where Bombelli's notice contradicts
his own plate — Santa Maria del Sole (notice 18 May 1669, plate and Briccolani 1665) and the Rosario
of the Minerva (notice 28 August 1644, plate and Briccolani 1640) — and Lima, where the act of 1925 prints *die XXIV
mensis septembris anno MDCCXXI* and Zander/Magister, citing the dossier in vol. 25, give 24 September
1921 — the same day a century apart, and the dossier's century is the likelier. They are left as
the sources give them.

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

Three further rules came in with the registers, which name a hundred and more images in one city:

- **A place-word inside a title is not identity.** *Santa Maria della Neve di Frosinone* is
  identified by *Neve*; the locality already carries *Frosinone*, and matching on it fused
  Acquapendente's Madonna delle Grazie (1742) with its cathedral's Concezione (1778). Words for
  kinds of building (*cattedrale*, *chiesa*, *monastero*) are dropped too, so *Santa Maria nella
  Cattedrale di Verona* has no title at all and the place and the year must carry it — and then a
  year-only register never merges with another register's entry at the same place on the year
  alone (Benevento 1723 is two images: Balzamo's Incoronata of the Camaldolese and Briccolani's
  Madonna delle Grazie), unless one of them gives the day.
- **Rome is not a place.** Over a hundred distinct images were crowned there, so two Roman records
  match only when their **church** signatures agree — *Rome, Sant'Agostino* with *Rome, S.
  Agostino*, never *San Giovanni in Fonte* with *San Giovanni dei Fiorentini* — and a Roman record
  never matches one from anywhere else, however many saints' names the two churches share (San
  Giovanni in Fonte is not San Giovanni Valdarno). A record that says only *Rome* reaches a church
  through its title (*Madonna del Nome di Maria* → *Rome, Santissimo Nome di Maria*); a record
  that names no place at all never reaches a Roman church on a title word alone (the *Madonna del
  Rimedio* of Arborea, in Sardinia, is not the one in San Dionigi alle Quattro Fontane) — a Roman
  act says *Romae*.
- **Two full dates that differ are two crownings.** Genoa's Madonnetta (27 June 1920) and Nostra
  Signora delle Vigne (21 November 1920) are not one image because both were crowned in 1920.

One earlier merge was undone by these rules and is left undone on purpose: Julius II's crowning of
the Loreto statue in 1500 (Balzamo) and the 1922 crowning at Loreto are now two records — the acts
of 1922 crown a *nova Virginis effigies*, the statue that replaced the one burned in 1921.

Residual duplicates are possible where a source names no locality at all, or where two acts
describe one image in words too different to match. One such pair was left open for a while:
**Piekary Śląskie** ([issue #1](https://github.com/CatholicOS/imagines-coronatae/issues/1)), where
AAS 55 (1963), 225 records a crowning *Pii Pp. XI permissu* and AAS 111 (2019), 1343 records August
Hlond crowning the Piekary image as Apostolic Administrator, neither act giving a date or naming
the other. Basilici–Bigliazzi (after Anselmo 1933) record exactly one crowning at Piekary, on 15
August 1925 by papal brief, with Pius XI's crowns and the Nuncio Lorenzo Lauri officiating — inside
both acts' windows — so the two are now held to be one image, with that date in the acts' `notes`
rather than in `coronation_dates`, since neither act states it. The word that had kept them apart,
*mirifica*, was praise leaking into a title, and is now on the descriptive stop-list.

## Primary and secondary sources are kept apart

Every source carries a `series`: **ASS** and **AAS** (the gazettes) and **ACSP** (the Chapter's
dossiers) were **read at first hand** for this catalogue. **LIT** is different: it marks a coronation
**reported by a scholarly work or a printed register** and not read here. Five works so far:

| Work | LIT records | What it is | Citation it carries |
|---|---|---|---|
| [Pietro **Bombelli**], *Raccolta delle immagini della Beatissima Vergine ornate della corona d'oro dal R.mo Capitolo di S. Pietro*, Rome 1792, tomi II–IV | 81 (74 images and 7 crowns for the Child) | One notice per crowned Roman image, facing an engraving: the day of the crowning, often the decree, the canons deputed, the cost of the crowns; the plate gives the support, the size and the year | none — 'le memorie dell'archivio', the *memoriali* and *atti capitolari*, no folio; confidence `low` |
| Vincenzo **Briccolani**, *Descrizione della sacrosanta Basilica Vaticana*, Rome 1800, pp. 144–161 | 256 | The earliest printed register: every Chapter coronation 1631–1791, year by year, Rome first and then all Italy and abroad | none — a year only; confidence `low` |
| Pietro **Zander** and Sara **Magister**, *Full of Grace: Crowned Madonnas from the Vatican Basilica*, New Haven 2011 | 107 (96 entries; a reported re-crowning is a second record) | Catalogue of the Fabbrica's painted copies of 89 crowned images, with the day of crowning | *BAV, ACSP, Madonne Coronate, vol., cc.* for 83 of them, and the Fabbrica's *catalogo delle immagini* (AFSP, Arm. 12, F, 11, nr. 10) |
| Dana **Vrabelová**, *Imago gratiosa*, Prague 2013, § XXI | 30 | Thirty Chapter coronations in Central Europe, 1717–1786 | *sv., fol.* for most |
| Nicolas **Balzamo**, « Uniformisation ou distinction ? », *RHR* 97 (2023) | 31 | Roman and Italian coronations 1631–1798 named in the text | *volume, folio* where given; town-and-year lists without |

A fifth work is kept outside the catalogue altogether. Massimo Basilici and Rita Bigliazzi's
*Le Madonne Coronate* (2025) and its database of **1,737 crownings 1631–1981** is the fullest list
there is, but it is compiled from Anselmo da Reno Centese's 1933 catalogue and the internet rather
than from the archive, so it is used as a yardstick: [`docs/CROSSMATCH-BASILICI.md`](docs/CROSSMATCH-BASILICI.md)
matches it against the catalogue in both directions — 474 of their schede correspond to an image
here, 974 verified crownings (almost all after 1800) do not, and 250 images here (the gazettes'
papal acts, above all) are not in their list.

Each row is cited to *BAV, ACSP, Madonne coronate, volume, folio* where the author gives one, and
those citations are carried in `register_refs`, so a LIT row can be taken back to the primary
dossier; until it is, its confidence is capped at `medium` (`low` where no folio is cited). The
rows are in `data/vrabelova-2013-table-xxi.json`, `data/balzamo-2023-crownings.json`,
`data/zander-magister-2011-catalogue.json`, `data/briccolani-1800-serie.json` and
`data/bombelli-1792-raccolta.json`. Rows that name
only a town and a year are kept **standalone** — they are not merged into any named image on place
and year, only on a shared title word, because a town and a year do not identify one.

Why keep the distinction visible: where the literature can be checked against the dossiers read
here, it is mostly right and sometimes not. Vrabelová dates Trsat to 21 March 1715; the instrument
says 14 September, the letters say 8 September. Where Briccolani and a tomo IV dossier meet (twenty-seven
images), his year is the dossier's in all but three, and those are one year off (Bertinoro and
Otranto a year early, Frascati a year late); where Zander/Magister meet
a dossier or a gazette act (Otranto, Cuglieri, Narni, Bonaria) the day agrees exactly. Bombelli
gives the day for fifty of his seventy-four Roman images, and where a tomo IV dossier covers the
same image the two fit: San Pantaleo's receipt is dated 25 March 1694 and so is his crowning; for
San Marcello the dossier's decree is of 16 August 1694 and his ceremony of 17 April 1695, for San
Lorenzo in Borgo decree 3 November and ceremony 6 December 1696. Against Briccolani his year agrees
in 71 of 74; in the three that differ (the Vittoria, the Madonna del Sole, the Rosario of the
Minerva) the caption engraved under his own plate sides with Briccolani against his notice. He and
Zander/Magister differ on the Madonna della Colonna (7 February against 1 January 1645), he and
Balzamo on the Altemps chapel (15 against 12 April 1673). Secondary
reports are valuable, but they are not the same kind of evidence.

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
   N (mecc. N)*. Exactly **one volume of it is digitized in full** —
   [`Arch.Cap.S.Pietro.Madonne.coron.4`](https://digi.vatlib.it/view/ARC_Arch.Cap.S.Pietro.Madonne.coron.4),
   726 images, not OCR'd — and ten folios of
   [vol. 19](https://digi.vatlib.it/view/ARC_Arch.Cap.S.Pietro.Madonne.coron.19) (the Capocolonna
   dossier of 1892). Everything else must be consulted at the Vatican Library or at the
   Archivio Capitolare. **That one volume has now been transcribed and swept** (`chapter_decree`
   records, cited by folio); the other tomes remain the largest unexamined source, reached here
   only through the registers and catalogues that cite them. See
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
| `scripts/transcribe_briccolani.py`, `scripts/transcribe_bombelli.py` | The transcriptions of the two printed registers, as Python rows, written out to `data/`. |
| `scripts/build_lit.py` | Turns the secondary-literature table into `data/attestations-lit.json`. |
| `scripts/build_images.py` | Consolidates acts into one record per image, with `sources`. |
| `scripts/build_registry.py` | Renders the two registry tables from the catalogue. |

The reading-and-structuring step between the sweep and the merge was performed by parallel LLM
agents against the specifications in `docs/EXTRACTION_SPEC.md`, `docs/EXTRACTION_SPEC_ASS.md` and,
for the Chapter dossiers, `docs/EXTRACTION_SPEC_ACSP.md`.

## Licence

The underlying ASS and AAS texts are © Libreria Editrice Vaticana. This compilation is offered for
research use.
