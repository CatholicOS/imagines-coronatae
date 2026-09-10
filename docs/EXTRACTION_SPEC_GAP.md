# Gap-triage addendum to SPEC.md

Read `SPEC.md` first (and `SPEC_ASS.md` if your batch is ASS). This states only what differs.

## Why this batch exists

The first sweep required a coronation word to sit near an *image* word (`imago`, `simulacrum`,
`statua`, `effigies`…). That filter silently dropped a real record:

> **AAS 71 (1979), 158.** John Paul II, homily at Santo Domingo, 25 January 1979:
> *"vivid la devoción a nuestra querida Madre del cielo, a quien invocáis con el hermoso nombre de
> **Nuestra Señora de la Altagracia, a la que el Papa quiere dejar como homenaje de devoción una
> diadema**."*

No word for "image" appears anywhere near it — the devotion is named by its **title** instead.
That is the pattern you are hunting: a crown or diadem given to, placed on, or offered to a named
devotional title (*Nuestra Señora de…*, *Notre-Dame de…*, *Madonna di…*, *Matka Boża…*,
*Our Lady of…*, *B. M. V. de…*, *Santo Niño…*), where the source never says "image".

## What to do

Every passage here was **rejected** by the first pass and carries a devotional title near a
coronation word. **Most are still noise** — expect a low yield. Reject, as always: crowns of
martyrdom, academic laurels, the rosary (*corona*, *coronae precatoriae*), the crown of thorns,
the papal tiara or a papal/royal coronation, metaphor, and surnames.

Emit a record only where a sacred image or named devotion is actually crowned, or is said to have
been crowned, or receives a crown/diadem from the Pope, under papal authority.

## Fields

Use the series-aware field names: **`series`** (`"AAS"` or `"ASS"`), **`volume`**, **`year`**,
**`page`** — not `aas_*`. Each passage tells you its series, volume, year and `printed_page`.
Everything else follows SPEC.md.

Where the source names only a devotional title and no physical image, still fill
`image_title_vernacular`, and say in `notes` that the source speaks of the devotion/title rather
than describing an image.

A gift of a crown or diadem by the Pope to a named devotion counts as
`papal_personal_coronation` when the Pope himself gives or imposes it; note in `notes` exactly what
the source says, since "leaving a diadem as homage" is not identical to a formal liturgical
coronation.

Your batch's passages each span about three printed pages, so the act's opening may be visible;
as always set `page` to the page the act begins on and note it if it differs from `printed_page`.
