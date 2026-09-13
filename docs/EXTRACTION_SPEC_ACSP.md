# Extraction spec — Madonne coronate, tomo IV (BAV, Arch. Cap. S. Pietro)

You are reading a machine transcription (TEI, via OCR) of **tomo IV** of the series *Madonne
coronate* in the archive of the Chapter of St Peter's Basilica, now at the Vatican Library. Its
title leaf: *"Madonne Coronate ossia Raccolta di documenti relativi alle corone di oro donate dal
R.mo Capitolo Vaticano secondo la pia intenzione del Conte Alessandro Sforza di Piacenza alle
Immagini o Statue di Maria S.ma e suo Divin Figlio più celebri per antichità culto e miracoli —
1689–1714"*.

## What the volume is

A **dossier book**. Under the Sforza Pallavicino legacy (will of 1636), a bishop or chapter
petitioned the Vatican Chapter to crown a miraculous image; the Chapter, assembled, **decreed the
concession** ("conceditur", "concessio", "concesso") and fixed a year; it deputed a canon or
prelate to perform the crowning; a Roman silversmith made the crown(s) — usually **two**, one for
the Virgin and one for the Child ("duarum coronarum aurearum"); a **notarial instrument of donation**
was drawn up ("Instrumentum donationis duarum coronarum aurearum factae simulacro miraculoso
B. M. V. … existenti in ecclesia …"); afterwards the deputy sent a **relazione** of the ceremony,
often with a printed commemorative sheet. The archivist filed all of this per image and wrote
**marginal notes** (`[note place=margin]`) summarising each document — those margin notes are your
best guide: they name the image, the church, the town, and give concession dates and register
cross-references (e.g. *"Lib. XXI f.º 318"*, *"Caps. 29 f. 379"*).

Languages: Italian (most), Latin (instruments, decrees), occasional Spanish/French. Spelling is
17th–18th c. with long-s rendered as **ſ**, and the OCR is imperfect: expect broken words,
`[...]`, and garbled Latin abbreviations. Read charitably but never invent.

## Your task

Identify every **distinct crowned image** documented in your page range and emit one record per
image. Give the **folio range** the dossier occupies. Dossiers may **start before** or **continue
past** your range — say so with the flags below rather than guessing what you cannot see.

## Page markers

Each page begins `=== pb N | f.FOLIO | FILENAME ===`. Cite folios by the `f.` label (e.g. `17r`,
`17r.02.mn.0000` for an inserted sheet at f. 17r). `pb` is the transcription's own page number.

## Record schema — ONE object per crowned image

```json
{
  "image_title_vernacular": "Madonna del Lago",
  "image_title_latin": "B. M. V. de Lacu — as given in a Latin instrument, or null",
  "image_subject": "Blessed Virgin Mary | Blessed Virgin Mary with Child | other (specify)",
  "church_or_sanctuary": "as named, or null",
  "locality": "Bertinoro",
  "diocese": "as named, or null",
  "country": "Italy — only if unambiguous from the place; else null",
  "concession_date": "YYYY-MM-DD if the decree/margin note gives it (e.g. '20. Junii 1689 conced.' -> 1689-06-20); YYYY if only a year; else null",
  "coronation_date": "date the crowning was performed, if any document states it; else null",
  "crowns": "e.g. 'two (Virgin and Child)' or 'one', or null",
  "deputy": "person deputed to crown (canon, abbot, bishop), or null",
  "petitioner": "who asked (bishop, chapter, community), or null",
  "register_refs": ["verbatim cross-references such as 'Lib. XXI f. 318', 'Caps. 29 f. 379'"],
  "documents": ["types present: supplica | decretum | instrumentum donationis | relazione | lettera | stampa | conto argentiere | other"],
  "folio_from": "3r",
  "folio_to": "16v",
  "pb_from": 5,
  "pb_to": 35,
  "starts_before_range": false,
  "continues_past_range": false,
  "key_quote": "one short verbatim phrase that identifies the image and place, ideally the margin note",
  "confidence": "high | medium | low",
  "notes": "OCR damage, ambiguity, alternative readings of the place-name; else null"
}
```

## Rules

1. **Never invent.** A field the pages do not support is `null`. Do NOT supply a modern diocese,
   country or saint's name from your own knowledge unless the text makes it unambiguous; if you
   infer, say so in `notes` and set `confidence` to `medium`.
2. **Place-name readings.** OCR mangles them ("Bisegliis", "Hydrunt.", "Tratian"). Give your best
   reading in `locality`, keep the raw form in `key_quote` or `notes`.
3. **Dates.** Latin/Italian month forms: *9bris* = November, *Xbris* = December, *7bris* =
   September, *8bris* = October. Convert carefully; if unsure give only the year.
4. **One record per image**, not per document. A dossier of twelve letters about one Madonna is
   one record listing the document types.
5. **Not coronations of images:** accounts of the silversmith alone (`conto`), general Chapter
   business, indices. Do not emit those as images — but if a silversmith's account names images
   that are otherwise absent from your range, you may emit them with `documents:["conto
   argentiere"]` and `confidence:"low"`.
6. Overlap: your range shares ~6 pages with the neighbouring batch; duplicates across batches are
   fine, they are merged later.

## Output

Write ONLY a JSON array to the output file. `[]` if nothing qualifies. Then reply with a two-line
summary.
