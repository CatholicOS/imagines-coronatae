# Cross-match: the Basilici–Bigliazzi database against this catalogue

Generated 2026-09-14 by `scripts/crossmatch_basilici.py`; the row-level result is
`data/crossmatch-basilici.csv`, the database itself `data/basilici-bigliazzi-2025-db.json`.

## What was compared

Massimo Basilici and Rita Bigliazzi, *Le Madonne Coronate* (four volumes, 2025), publish their
research as a database at <https://www.pereto.org/madonne_coronate/>: **1,737 schede**, one per crowning
they examined, 1631–1981, each with locality, church, title, date of crowning, date of the Chapter's
decree where known, the authorising body, and a verdict (`Data verificata: sì/no`) on whether they
found evidence that the crowning was really by Count Sforza, the Chapter, a papal brief or the Pope.
By their own account the list was built from Anselmo da Reno Centese's catalogue of 1933 (itself
drawn from the Chapter's registers only for 1905 onwards), the printed repertories, the internet and
correspondence, with the archive consulted for particular cases — so it is a *secondary* source, of
the same standing as the LIT layer here, and it has **not** been merged into the catalogue. It is the
most complete list in existence, which is exactly why it is worth measuring the catalogue against it.

A scheda and a catalogue image are counted as the same crowning when they share a place token and
either a title word or the year (±1); in Rome a shared church word is required, as in the catalogue's
own matching. The rule is deliberately no fuzzier than that.

## Result

| | schede |
|---|---|
| in the database | 1,737 |
| matched to a catalogue image | 467 (27%) |
| — on title and year | 301 |
| — on title only | 67 |
| — on year only | 99 |
| not in the catalogue | 1,270 (73%) |
| — of which they mark *verificata: sì* and a real crowning (1st/2nd) | 981 |

Of the 467 matches, the year agrees exactly in 379, is one off in 21,
differs in 49, and cannot be compared in 18.

### Gaps in the catalogue: crownings they record that this catalogue lacks

981 schede that they mark as verified crownings have no counterpart here. By period, authority and country:

| Century | Schede |
|---|---|
| 1600s | 6 |
| 1700s | 39 |
| 1800s | 227 |
| 1900s | 709 |

| Authority (their `Autorizza`) | Schede |
|---|---|
| Capitolo | 570 |
| B.P. | 371 |
| # | 9 |
| B.P | 9 |
| Papa Pio VII | 6 |
| Pio VII | 4 |
| Papa Pio IX | 3 |
|  | 3 |
| Capitolo assenso | 2 |
| Papa Pio VI | 1 |
| Papa Gregorio XVI | 1 |
| Papa Paolo VI | 1 |
| Papa Giovanni Paolo II | 1 |

| Country | Schede |
|---|---|
| Italia | 436 |
| Spagna | 178 |
| Francia | 108 |
| Messico | 51 |
| Polonia | 23 |
| Belgio | 23 |
| Argentina | 18 |
| Filippine | 18 |
| Perù | 12 |
| Malta | 10 |
| Ucraina | 9 |
| Colombia | 8 |
| Brasile | 7 |
| Austria | 6 |
| Svizzera | 6 |
| Germania | 6 |
| Venezuela | 6 |
| Cile | 5 |
| Ecuador | 5 |
| Paesi Bassi | 4 |

The shape is what the sources predict. The catalogue's primary layers are the two gazettes and one
dossier volume (1689–1714); its literature layer is Briccolani to 1791, Vrabelová for Central Europe
to 1786, Balzamo's lists to 1798 and the 89 painted copies of Zander/Magister. Before 1800 the two
lists nearly coincide: 45 of their verified crownings of the seventeenth and eighteenth
centuries are unmatched here, and on inspection about half of those are the same crowning under a
locality this matching could not align (Tolfa for Cibona, Nova Gorica for Monte Santo, Dobrzyń nad
Wisłą for Skępe, Leopoli for Lwów, Monte San Giuliano for Custonaci, or a year two or three off — see
below). The rest are genuine absences, mostly omissions of Briccolani's list: Reggio Calabria 1722,
Meta 1748, Piancastagnaio 1751, Pescasseroli 1752, Scurcola Marsicana 1757, Verona's Madonna del
Popolo 1770, Paternopoli 1774, Cesena 1782 (by Pius VI), Roccadaspide 1786, Sinalunga 1793,
Catanzaro 1797, and a few Roman and Neapolitan images (Costantinopoli 1651, Gioie 1679, Naples'
Grazie 1726 and Addolorata 1761). After 1800 the
catalogue has only what a gazette or Zander/Magister happened to record, and that is what the
other 936 rows are: the Chapter's Italian coronations of the nineteenth century and the
Chapter and papal-brief coronations of 1900–1981 in Italy, Spain, France and Latin America — the
volumes 12–36 of *Madonne coronate* and the *Madonne incoronate* of the Archivio Capitolare, seen
through Anselmo's 1933 list and its continuators.

### Gaps in the database: images here that they do not record

258 of the catalogue's 671 images found no scheda. By evidence and by the series that attest them:

| Strongest evidence | Images |
|---|---|
| `papal_coronation_act` | 92 |
| `retrospective_attestation` | 74 |
| `chapter_decree` | 59 |
| `papal_personal_coronation` | 24 |
| `papal_legate_deputation` | 7 |
| `norms` | 2 |

| Series | Images |
|---|---|
| AAS | 192 |
| LIT | 47 |
| AAS+LIT | 6 |
| ACSP | 5 |
| ASS | 3 |
| AAS+ASS | 2 |
| ACSP+LIT | 2 |
| ASS+LIT | 1 |

| Country | Images |
|---|---|
| Italy | 80 |
| Poland | 64 |
| Mexico | 17 |
| Spain | 16 |
| Colombia | 8 |
| Philippines | 7 |
| Ukraine | 6 |
| France | 5 |
| None | 5 |
| Belgium | 4 |
| Peru | 4 |
| Argentina | 3 |

Two kinds of image sit here. First, and most of them, the **papal crownings the gazettes record**
— 197 images attested only by ASS/AAS: a Legate's coronation in Colombia or the Philippines, the
*Litterae Apostolicae* of the 1980s and 1990s (they stop at 1981), and the 64 Polish images most of
which John Paul II crowned. Their database follows the Chapter and Anselmo, and the papal acts of
the gazettes are largely outside it — which is the catalogue's own contribution. Second, a few
dozen images from the literature layer — Briccolani's Roman entries that their Rome schede name by
a different church, Balzamo's town-and-year rows — where a good number will be the same images
under different names, and some genuine absences; they are the rows with an empty `match` in the
CSV.

### Where the two disagree on the date

49 matched crownings carry a year here that differs from theirs by more than one. A sample:

| Their scheda | Their date | Catalogue image | Catalogue dates |
|---|---|---|---|
| Madonna della Febbre — Città del Vaticano | 31-1-1643 | Madonna della Febbre — Rome, Vatican Basilica (sacristy) | 1631-08-27; 1697-08-15 |
| Madonna di Loreto — Roma | #-#-1646 | Santa Maria di Loreto in S. Salvator in Lauro — Rome, San Salvatore in Lauro | 1644 |
| Madonna del Soccorso — Città del Vaticano | #-#-1647 | Santa Maria del Soccorso nella Cappella Gregoriana della Basilica Vaticana — Rome, Vatican Basilica (Cappella Gregoriana) | 1643-11-17 |
| Madonna del Pianto — Roma | #-#-1651 | Santa Maria del Pianto — Rome, Santa Maria del Pianto | 1643 |
| Madonna della Purità — Roma | #-#-1651 | Santa Maria della Purità in Borgo — Rome, Santa Maria della Purità in Borgo | 1646 |
| Madonna del Rosario — Roma | 15-12-1654 | Santa Maria del Rosario nella Chiesa di Santa Maria — Rome, Santa Maria sopra Minerva | 1640 |
| Madonna della Misericordia — Roma | 6-11-1661 | Santa Maria della Misericordia in S. Giovanni de Fiorentini — Rome, San Giovanni dei Fiorentini | 1648 |
| Madonna del Popolo — Roma | 6-9-1667 | Santa Maria de' Miracoli sulla Piazza del Popolo — Rome, Santa Maria dei Miracoli | 1645 |
| Madonna dei Miracoli — Roma | #-#-1667 | Santa Maria de' Miracoli sulla Piazza del Popolo — Rome, Santa Maria dei Miracoli | 1645 |
| Madonna della Salute — Roma | 6-12-1696 | Santa Maria della Salute in S. Lorenzo in Lucina — Rome, San Lorenzo in Lucina | 1648 |
| Santa Maria del Rosario — Antegnate | 29-4-1753 | Santa Maria del Rosario nella Chiesa di S. Michel Arcangelo di Antegnate — Antegnate | 1751 |
| Nostra Signora di Chelm — Chelm | 17-9-1767 | Nostra Signora di Chelm — Chełm | 1765-09-15 |
| Santa Maria dell'Orto — Chiavari | 8-9-1769 | Santa Maria dell'Orto di Chiaveri — Chiavari (Clavarium), Liguria | 1767 |
| Santa Maria del Soccorso — Vezzano Ligure, frazione di Vezzano Superiore | #-9-1776 | Santa Maria del Soccorso di Vezzano — Vezzano Ligure | 1772 |
| Santa Maria dei Miracoli — Alcamo | 21-6-1784 | Santa Maria de' Miracoli nella Chiesa d'Alcami — Alcamo | 1782 |
| Santa Maria delle Grazie — Vallo della Lucania | 8-6-1788 | Santa Maria delle Grazie nella Chiesa de' Domenicani di Val di Novi — Vallo della Lucania (Novi Velia), diocese of Capaccio | 1786 |
| Santa Maria di Costantinopoli — Ischia | 25-8-1794 | Santa Maria di Costantinopoli d'Ischia — Ischia | 1791 |
| Madonna di Galloro — Ariccia, frazione di Galloro | 20-10-1818 | Santa Maria di Galloro — Galloro (Ariccia) | 1726 |
| Santa Maria della Rotonda — Albano Laziale | 22-8-1829 | Santa Maria della Rotonda d'Albano — Albano | 1729 |
| Santa Maria di Loreto — Roma | 9-12-1836 | Santa Maria di Loreto in S. Salvator in Lauro — Rome, San Salvatore in Lauro | 1644 |
| Santa Maria del Parto — Roma | 2-7-1851 | Santa Maria in S. Agostino — Rome, Sant'Agostino | 1641; 1643 |
| Santa Maria delle Grazie — Napoli, zona di Caponapoli | 21-11-1853 | Santa Maria delle Grazie alla Pietra del Pesce in Napoli — Napoli (Pietra del Pesce) | 1786 |
| Immacolata Concezione — Roma | 8-12-1854 | Santa Maria della Concezione in S. Lorenzo, e Damaso — Rome, San Lorenzo in Damaso | 1635 |
| Madonna della Salute — Roma | 30-8-1868 | Santa Maria della Salute nella Chiesa della Madalena — Rome, Santa Maria Maddalena | 1668 |
| Santa Maria in Sassia — Roma | 4-6-1872 | Santa Maria in S. Spirito in Sassia — Rome, Santo Spirito in Sassia | 1655 |
| Nostra Signora di Arcachon — Arcachon | 16-7-1873 | Notre-Dame d'Arcachon — Arcachon | 1870 |
| Santa Maria della Civita — Itri | 20-7-1877 | Santa Maria di Civita nella Chiesa d'Itri — Itri | 1777 |
| Nostra Signora de la Delivrande — Douvres-la-Délivrande | 22-8-1877 | Notre Dame De La Délivrande — Douvres-la-Délivrande | 1872-08-22 |
| Santa Maria della Rotonda — Albano Laziale | 3-8-1879 | Santa Maria della Rotonda d'Albano — Albano | 1729 |
| Santa Maria di Costantinopoli — Acquaviva delle Fonti | 4-9-1881 | Santa Maria di Costantinopoli nella Chiesa di S. Eustachio della Città d'Aquaviva — Acquaviva delle Fonti | 1780 |

Read down the list and three things separate out.

- **Second crownings the catalogue does not have.** Their database records the *re-crowning* of
  many Roman images in the nineteenth and twentieth centuries — the Madonna di Loreto of San
  Salvatore in Lauro in 1836, the Salute of the Maddalena in 1868, Santa Maria in Sassia in 1872,
  the Madonna della Strada in 1885, the Nome di Maria in 1903, Santa Maria in Cosmedin in 1920 —
  and of others (Galloro 1818, Albano's Rotonda 1829, 1879 and 1905, Viterbo's Liberatrice 1901).
  Briccolani's list stops in 1791, so the catalogue has only the first crown; these are real
  additions, and the `incoronazione = 2` flag in their schede is how to find them.
- **A dating question about Briccolani.** For a run of coronations of the 1750s–1790s their date
  is two or three years later than Briccolani's year — Antegnate 1751/1753, Chiavari 1767/1769,
  Vezzano 1772/1776, Acquapendente 1778/1780, Alcamo 1782/1784, Vittoria 1785/1787, Pagani
  1785/1787, Vallo 1786/1788, Ischia 1791/1794. Where a dossier-based date exists the picture is
  mixed: Cava de' Tirreni (Briccolani 1764, Zander/Magister 15 June 1766) supports them, but
  Piano di Sorrento, Palermo, Casalpusterlengo and Valperga agree with Briccolani to the year, and
  their Alcamo (1784) sits between Briccolani's 1782 and Balzamo's 1786. Their dates for this
  period come from Anselmo, whose pre-1905 dates were not taken from the registers; which of the
  two lists gives the ceremony and which the decree is a question for vols 9–12 of the fond.
- **Genuine disagreements.** Chełm: their 17 September 1767 against Vrabelová's 15 September 1765
  (Zander/Magister give both). Trsat: their scheda gives 28 October 1715 (with the Chapter's decree of
  3 August 1713 and the officiant, Giovanni Francesco Barbarigo, bishop of Verona) and marks
  Anselmo's 21 March 1715 as an error; the dossier read here gives 8 September 1715, notarised on
  the 14th — three secondary dates for one primary one. Podkamień: their 15 August 1727 against
  Vrabelová's 15 August 1723.

## How to use this

- To **extend the catalogue**, the 981 unmatched verified schede are the work-list: each names
  a locality, a church and a year, which is enough to find the dossier in the right volume of
  *Madonne coronate* (Zander/Magister's citations give the volume for each decade) and, for 1865
  onwards, to search the gazettes for a retrospective mention.
- To **check the catalogue**, the 49 date disagreements and the 21 one-year offsets are
  the places to look first.
- Their `Autorizza = B.P.` rows (442) are crownings by papal brief; from 1865 these ought to
  be in ASS/AAS, and any that are unmatched here are candidates for a missed act.
