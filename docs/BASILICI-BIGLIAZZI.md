# The Basilici–Bigliazzi database in the catalogue

Generated 2026-09-15 by `scripts/report_basilici.py`; the row-level result is
`data/basilici-in-catalogue.csv`, the database itself `data/basilici-bigliazzi-2025-db.json`.

## What it is

Massimo Basilici and Rita Bigliazzi, *Le Madonne Coronate* (four volumes, 2025), publish their
research as a database at <https://www.pereto.org/madonne_coronate/>: **1,737 schede**, one per crowning
they examined, 1631–1981, each with locality, church, title, date of crowning, date of the decree
where known, the authorising body (`Autorizza`: the Chapter, a papal brief, Count Sforza, a Pope) and
a verdict (`Data verificata: sì/no`) on whether they found evidence that the crowning really took
place under that authority. By their own account the list was built from Anselmo da Reno Centese's
catalogue of 1933, the printed repertories (Briccolani, Bonci) and the internet, with the archive
consulted for particular cases; so it is a **secondary compilation citing no folio**, and the rows
taken from it enter the catalogue as series `LIT`, confidence `low`, with their authority, officiant,
decree date and notes carried in the source's `notes`.

## What was taken

| | schede |
|---|---|
| in the database | 1,737 |
| taken into the catalogue — *verificata: sì* and a real crowning (1st, 2nd or 3rd) | 1,420 |
| — corroborating an image another source already attests | 472 |
| — the only source of an image | 948 (934 images) |
| left out — *incoronazione #* (uncertain, or a petition the Chapter refused) or *verificata: no* | 317 |

Their `Autorizza` becomes the record's `evidence_type`: *Capitolo* and *Conte Sforza* →
`chapter_decree`; *B.P.* (a papal brief) → `papal_coronation_act`; a Pope who also officiated →
`papal_personal_coronation`; `#` (authority they could not establish) → `retrospective_attestation`.

**Rome.** They describe a Roman church at length ("Basilica di Santa Maria in Trastevere nella
Cappella Altemps"), which the catalogue's church-signature rule cannot see, so their 133 Roman
schede are aligned by hand to the catalogue's own church strings in `data/basilici-rome-alignment.json`
(`scripts/align_basilici_rome.py`); 12 of them are the separate crown for the Child of an image
crowned earlier — Briccolani's twelve *Bambino Gesù* concessions — which they file as first crownings,
and which are linked to their image by `parent_act` and not counted as re-crownings.

## What they add

934 images rest on their database alone (948 schede, an image crowned more than
once having a scheda per crowning). Those schede by century, authority and country:

| Century | Schede |
|---|---|
| 1600s | 2 |
| 1700s | 33 |
| 1800s | 217 |
| 1900s | 696 |

| Authority (their `Autorizza`) | Schede |
|---|---|
| Capitolo | 548 |
| B.P | 372 |
| # | 11 |
| Papa Pio VII | 4 |
| Pio VII | 4 |
| Papa Pio IX | 3 |
| Capitolo assenso | 2 |
| Papa Pio VI | 1 |
| Papa Benedetto XV | 1 |
| Papa Paolo VI | 1 |
| Papa Giovanni Paolo II | 1 |

| Country (the twenty most frequent) | Schede |
|---|---|
| Italia | 416 |
| Spagna | 175 |
| Francia | 108 |
| Messico | 49 |
| Polonia | 24 |
| Belgio | 23 |
| Filippine | 18 |
| Argentina | 17 |
| Perù | 12 |
| Malta | 9 |
| Colombia | 8 |
| Ucraina | 7 |
| Austria | 6 |
| Svizzera | 6 |
| Germania | 6 |
| Ecuador | 6 |
| Brasile | 6 |
| Venezuela | 5 |
| Cile | 4 |
| Paesi Bassi | 4 |

The shape is what the sources predict: the catalogue's primary layers are the two gazettes and one
dossier volume, its registers stop at 1800 (Briccolani) and Rome (Bombelli); what Basilici–Bigliazzi
supply is the Chapter's and the briefs' coronations of the nineteenth and twentieth centuries — the
volumes of *Madonne coronate* that are not online, seen through Anselmo's 1933 list and its
continuators. Every such image is `low`, and says in its notes what it rests on.

## Where the two disagree on the date

Of the 472 schede that corroborate an image known from another source, the year agrees exactly
in 379, is one off in 19, differs in 43, and cannot be compared in 31
(the other source gives no date). The 43 disagreements — a year or more apart — are kept
as the sources give them, so such an image shows two dates; the first thirty:

| Their scheda | Their date | The other source's date |
|---|---|---|
| Santa Maria delle Grazie — Napoli | 12-5-1726 | 1726-05-12; 1786-07-02; 1802-09-26; 1853-11-21 (Balzamo; Briccolani) |
| Santa Maria del Rosario — Antegnate | 29-4-1753 | 1753-04-29 (Briccolani) |
| Santa Maria Addolorata del Buoncammino — Napoli | 15-8-1761 | 1761-08-15; 1881-06-01; 1910-09-04 (AAS) |
| Santa Maria dell'Orto — Chiavari | 8-9-1769 | 1769-09-08 (Briccolani) |
| Santa Maria del Soccorso — Vezzano Ligure, frazione di Vezzano Superiore | #-9-1776 | 1772; 1776-09 (Briccolani) |
| Maria Santissima Immacolata Concezione — Acquapendente | 28-5-1780 | 1780-05-28 (Briccolani) |
| Santa Maria dei Miracoli — Alcamo | 21-6-1784 | 1784-06-21 (Briccolani) |
| Santa Maria Lauretana — Vittoria | 29-6-1787 | 1787-06-29 (Briccolani) |
| Santa Maria del Carmine — Pagani | 22-9-1787 | 1787-09-22 (Briccolani) |
| Santa Maria delle Grazie — Vallo della Lucania | 8-6-1788 | 1788-06-08 (Briccolani) |
| Santa Maria di Costantinopoli — Ischia | 25-8-1794 | 1791; 1794-08-25 (Briccolani) |
| Madonna di Loreto — Loreto | 23-2-1801 | 1801-02-23; 1922-09-05; 1962-10-04 (AAS) |
| Santa Maria delle Grazie — Napoli | 26-9-1802 | 1726-05-12; 1786-07-02; 1802-09-26; 1853-11-21 (Balzamo; Briccolani) |
| Madonna di Galloro — Ariccia, frazione di Galloro | 20-10-1818 | 1726-06-10; 1818-10-20 (Briccolani) |
| Santa Maria della Rotonda — Albano Laziale | 22-8-1829 | 1729-08-22; 1829-08-22; 1905-05-14 (Briccolani) |
| Santa Maria di Loreto — Roma | 9-12-1836 | 1644-12-12; 1836-12-09 (Bombelli; Briccolani) |
| Santa Maria "Salus Populi Romani" — Roma | 15-8-1838 | 1597; 1838-08-15; 1954-11-01 (AAS; Balzamo) |
| Santa Maria delle Grazie — Napoli, zona di Caponapoli | 21-11-1853 | 1726-05-12; 1786-07-02; 1802-09-26; 1853-11-21 (Balzamo; Briccolani) |
| Immacolata Concezione — Roma | 8-12-1854 | 1635-08-22; 1854-12-08 (Bombelli; Briccolani) |
| Madonna del Buon Consiglio — Genazzano | 30-4-1867 | 1682-11-17; 1867-04-30 (Briccolani) |
| Madonna della Salute — Roma | 30-8-1868 | 1668-11-05; 1868-08-30 (Bombelli; Briccolani) |
| Santa Maria della Civita — Itri | 20-7-1877 | 1777-07-20; 1877-07-20 (Briccolani) |
| Santa Maria Addolorata — Napoli | 1-6-1881 | 1761-08-15; 1881-06-01; 1910-09-04 (AAS) |
| Santa Maria di Costantinopoli — Acquaviva delle Fonti | 4-9-1881 | 1781-09-04; 1881-09-04 (Briccolani) |
| Madonna della Strada — Roma | 14-6-1885 | 1638-08-14; 1885-06-14 (Briccolani) |
| Santa Maria della Provvidenza, Aiuto dei Cristiani — Napoli | 13-11-1887 | 1775-11-25; 1887-11-13; 1889-05-24 (Balzamo; Briccolani) |
| Santa Maria Delle Grazie — Piano di Sorrento | 10-6-1888 | 1771-09-07; 1888-06-10 (Briccolani) |
| Santa Maria della Natività o di Belmonte — Valperga | 17-8-1888 | 1788-08-17; 1888-08-17 (Balzamo; Briccolani; Zander/Magister) |
| Santa Maria dell'Aiuto — Napoli | 24-5-1889 | 1775-11-25; 1887-11-13; 1889-05-24 (Balzamo; Briccolani) |
| Nostra Signora Consolatrix Afflictorum — Kevelaer | 1-6-1892 | 1892-06-01 (AAS) |

For the 1750s–1790s their dates run two or three years later than Briccolani's — Antegnate
1751/1753, Chiavari 1767/1769 — which is the difference between the year of the decree and the year
of the ceremony; the `notes` of many rows say so ("scambia la data del decreto con la data
dell'incoronazione").

## Images they do not record

245 of the catalogue's 1,605 images have no scheda. By evidence and by the series that attest them:

| Strongest evidence | Images |
|---|---|
| `papal_coronation_act` | 87 |
| `retrospective_attestation` | 73 |
| `chapter_decree` | 54 |
| `papal_personal_coronation` | 22 |
| `papal_legate_deputation` | 7 |
| `norms` | 2 |

| Series | Images |
|---|---|
| AAS | 185 |
| LIT | 46 |
| ACSP | 5 |
| ASS | 4 |
| AAS+LIT | 3 |
| AAS+ASS | 1 |
| ASS+LIT | 1 |

| Country (the twelve most frequent) | Images |
|---|---|
| Italy | 80 |
| Poland | 64 |
| Mexico | 15 |
| Spain | 13 |
| Colombia | 8 |
| Philippines | 7 |
| France | 6 |
| None | 5 |
| Belgium | 4 |
| Peru | 4 |
| Ukraine | 4 |
| Belarus | 3 |

These are, above all, the gazettes' papal acts — coronations by Legate or by the Pope in person,
and the retrospective mentions in later acts — which their list, built from the Chapter's side,
does not cover; and the images the catalogue holds twice where two acts describe one image in words
too different to match.

## Residue

A few schede that the earlier cross-match had paired with an image stay separate under the
catalogue's stricter rules, and are left so on purpose: where their date and the other source's are
more than a year apart with no shared title word (El Quinche 1943/1933, Arcachon 1873/1870, Chełm
1767/1765), where two clusters already hold the same image (Foggia's Iconavetere, the Grazie al Foro
Romano), or where the other side is a standalone town-and-year row (Monchiero). One known
over-merge is left visible: their Caponapoli crowning of 1853 sits on the Pietra del Pesce image at
Naples, both being a *Madonna delle Grazie* in a city with several.

## How to use this

`data/basilici-in-catalogue.csv` has one row per scheda: `taken` and `why_not`, the `image_id` it
sits in, `other_sources` on that image, `date_agrees` against them, and `rome_alignment` (AUTO/PICK)
where the Roman church was aligned by hand. An image whose only source is `Basilici–Bigliazzi 2025`
is a lead to be checked against the Chapter's registers or a local monograph, not a documented
crowning.
