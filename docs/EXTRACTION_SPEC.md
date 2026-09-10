# Extraction spec — crowned images (imagines coronatae) in Acta Apostolicae Sedis

You are given a JSON array of candidate passages extracted from OCR'd AAS volumes.
Each passage has: id, file, volume, year, pdf_page, printed_page, context (verbatim OCR text).

Your job: decide what each passage attests, and emit a JSON record for every DISTINCT
crowned image you can document. Passages that attest nothing relevant are simply omitted.

## What counts

Emit a record when the passage documents that a sacred IMAGE (statue, painting, icon)
is or was crowned under papal authority. Classify with `evidence_type`:

- `papal_coronation_act`   — the act itself grants/permits the coronation.
  Typical Latin: "pretioso diademate redimiri sinitur", "coronari sinitur",
  "facultas conceditur diademate cingendi", "conceditur ut possit imaginem ... coronare",
  "aurea corona redimiatur", "Sinitur Episcopus ... coronare".
- `papal_legate_deputation` — the Pope deputes a Cardinal/Bishop Legate to crown the image
  in his name. Typical: "quem Legatum mittit ad coronam apponendam simulacro ...",
  "deputatur ad aurea corona ornandum simulacrum".
- `papal_personal_coronation` — records the Pope himself crowned it.
  Typical: "Memoriae proditur Summum Pontificem ... coronasse imaginem ...",
  "quam Nos Ipsi ... coronavimus".
- `retrospective_attestation` — a DIFFERENT act (e.g. Basilica Minor elevation, patron
  declaration) states in passing that the image was crowned, often
  "ex decreto Capituli Vaticani" / "auctoritate Pii PP. X ... aureo diademate redimita".
  Record it, with the coronation year if stated.
- `norms` — general legislation about crowning images (no specific image). Emit with
  image fields null.

## What does NOT count (omit entirely)

Crown of martyrdom ("martyrii corona", "martyrio coronatur"); academic laurels
("laurea coronatus"); the rosary ("corona", "coronae precatoriae"); the papal coronation
("coronatio Summi Pontificis"); the titular church "Ss. Quattuor Coronatorum";
the Camaldolese "Montis Coronae"; crown of thorns; the crowning of a secular monarch;
purely metaphorical crowns. When "corona" is a person's surname, omit.

## Record schema — emit ONE JSON object per crowned image

```json
{
  "source_id": "<passage id, verbatim>",
  "aas_volume": 91,
  "aas_year": 1999,
  "aas_page": 345,
  "act_number": "V",
  "act_type": "Litterae Apostolicae",
  "pope": "Ioannes Paulus PP. II",
  "evidence_type": "papal_coronation_act",
  "rubric_latin": "verbatim rubric/heading, or null",
  "incipit_latin": "the first ~15 words of the act body AFTER 'Ad perpetuam rei memoriam. —' (or after the salutation), verbatim, or null",
  "image_title_latin": "title as given in Latin, or null",
  "image_title_vernacular": "e.g. Nuestra Señora de Canòlich, or null",
  "image_subject": "Blessed Virgin Mary | Sacred Heart of Jesus | Infant Jesus | St Joseph | Holy Family | other (specify)",
  "church_or_sanctuary": "or null",
  "locality": "town/place, or null",
  "diocese_latin": "e.g. Urgellensis, or null",
  "diocese_modern": "e.g. Urgell, or null",
  "country": "modern country name, or null",
  "act_date": "YYYY-MM-DD if the 'Datum' line gives it (Roman numerals -> digits), else null",
  "coronation_date": "YYYY-MM-DD or YYYY if the passage states when the crowning happened/will happen, else null",
  "legate": "name of the Legate deputed, or null",
  "confidence": "high | medium | low",
  "notes": "OCR damage, ambiguity, or anything a checker should verify; else null"
}
```

## Rules — accuracy over completeness

1. **Never invent.** If a field is not in the passage, use `null`. Do NOT infer a country
   from your own knowledge of a shrine unless the passage names the place clearly enough
   that the country is unambiguous — if you do infer, say so in `notes` and drop
   `confidence` to `medium`.
2. **Verbatim Latin.** `rubric_latin` and `incipit_latin` must be copied from the text.
   You may silently repair obvious OCR letter-splitting (e.g. "IMAGINEB. M. V." ->
   "IMAGINE B. M. V.", "REDIMIT UR" -> "REDIMITUR") but must not paraphrase.
3. **OCR damage.** These are OCR'd scans; place names are often mangled
   (e.g. "Seynora" for "Señora", "Bafios" for "Baños"). Give your best reading in the
   vernacular field, keep the raw form in `notes`, and set `confidence` accordingly.
4. **Roman numerals.** Dates appear as "die VII mensis Decembris, anno MCMXCVIII" ->
   `1998-12-07`. Convert carefully; if unsure, null + note.
5. **Page numbers.** Use `printed_page` from the passage as `aas_page` — that is the
   citable AAS page. If the act clearly begins on a different printed page visible in the
   context, prefer that and note it.
6. One passage may contain SEVERAL acts (they run together). Emit a record for each
   distinct image. Conversely a passage may duplicate one already covered — that's fine,
   dedup happens later.
7. `confidence`: `high` = act type, image and place all explicit; `medium` = some
   inference or OCR repair; `low` = fragmentary, needs human check.

## Output

Write ONLY a JSON array to the output file you are given. No prose, no markdown fence.
If nothing qualifies, write `[]`. Then reply with a two-line summary: count of records
and anything notable you want the coordinator to know.
