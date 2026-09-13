# The Vatican Chapter archives and where coronation concessions are recorded

Research note. Everything below was verified against the live sources on 10–11 September 2026;
URLs and shelfmarks are given so each claim can be rechecked.

## Why this matters for this catalogue

Most crowned images never appear in *Acta Sanctae Sedis* or *Acta Apostolicae Sedis*. For three
centuries the crowning of an image was granted not by a papal act but by **decree of the Chapter of
St Peter's Basilica**, and those decrees were not gazetted. The AAS/ASS record is therefore a subset,
and the Chapter's own series is the primary source for everything outside it.

## Origin of the practice

The tradition rests on a private bequest, not on legislation. Count **Alessandro Sforza Pallavicino**
(d. 20 August 1638) had been crowning Roman Marian images from 1631, and by his will of **3 July
1636** left the Chapter of St Peter the income of 71 *luoghi di monte* so that golden crowns should
perpetually be made for the most ancient, most venerated and most miraculous images of the Virgin —
on condition *"che le stia su la testa, e che mai ne sia levata"*. The Chapter has administered the
legacy ever since, which is why the concession is a **Chapter** act.

## The procedure, and the paper trail it created

Set out in the Chapter's own norms and summarised in the study of the 1724 Bisognosi coronation
(see Sources):

1. The **bishop petitions the Chapter**, sending a *supplica* with authenticated letters proving the
   image's antiquity, the concourse of people, and its miracles.
2. The Chapter, **collegially assembled, decrees the coronation** and fixes the year.
3. Execution is delegated to a **canon of the Chapter** or another dignitary, who sets the day.
4. The petitioners send **the measurements of the image** to Rome so the crown fits; the crown is
   made by Roman goldsmiths at the Chapter's expense.
5. Afterwards a **public notarial act**, together with the history of the image and of its
   coronation, is transmitted to the **Secretary of the Chapter** to be preserved in the archive
   *"a perenne documentazione dell'avvenimento"* — plus printed commemorative sheets and a painted
   copy of the crowned image kept in the Basilica.

Step 5 is the reason a searchable series exists at all: every coronation was supposed to deposit a
dossier.

## Where the records sit

The archive was **divided in 1940**. Historical material went to the **Biblioteca Apostolica
Vaticana** (BAV), where it forms the fond *Archivio del Capitolo di San Pietro* (**ACSP**); legal and
administrative material stayed with the **Chapter** at the Palazzo della Canonica.

The relevant series is **`Madonne coronate`**, and it is on the BAV side. Scholars cite it as:

> **BAV, ACSP, Madonne coronate, tomo I, foglio XII fronte (mecc. 15)**

— that is: *tomo* (volume, Roman numeral), *foglio* (folio, Roman numeral, *fronte*/*retro* for
recto/verso), with a parallel modern stamped foliation given as *mecc.*

## What is digitized, and what is not

DigiVatLib splits the fond across **two different sections**, which is easy to miss:

| Section | URL | Content |
|---|---|---|
| Manuscripts | `digi.vatlib.it/mss/Arch.Cap.S.Pietro` | **471** codices in letter series **A–K** — Bibles, passionaries, lectionaries, the Orsini bequest, Grimaldi's descriptions of the Basilica. Medieval and early-modern **books**. |
| Archives | `digi.vatlib.it/arc/Arch.Cap.S.Pietro` | **254 archival series** — the administrative fond: *Decreti*, *Capsulae*, *Privilegi e atti notarili*, *Lettere del Capitolo*, the Campomorto and Boccea estate accounts, the Sagrestia series, and **`Madonne.coron`**. |

Coronation concessions are in the **archives** section, not the manuscripts section. Searching
`/mss/` for them — the obvious first move — finds nothing.

**Of the `Madonne coronate` volumes, exactly one is digitized:**

> **`Arch.Cap.S.Pietro.Madonne.coron.4`** — 726 images
> Viewer: <https://digi.vatlib.it/view/ARC_Arch.Cap.S.Pietro.Madonne.coron.4>
> IIIF manifest: `https://digi.vatlib.it/iiif/ARC_Arch.Cap.S.Pietro.Madonne.coron.4/manifest.json`

Tomes 1, 2, 3, 5 and 6 return 404 — they are **not** online. Note the IIIF prefix for this section is
**`ARC_`**, not the `MSS_` used for the codices.

### What tomo 4 actually contains

Its own title leaf (f. 1r) reads:

> *Madonne Coronate ossia Raccolta di documenti relativi alle corone di oro donate dal R.mo Capitolo
> Vaticano secondo la pia intenzione del Conte Alessandro Sforza di Piacenza alle Immagini o Statue di
> Maria S.ma e suo Divin Figlio più celebri per antichità culto e miracoli — **1689 – 1714** — Tomo IV.*

So the volume covers coronations of **1689–1714** — not, as an earlier version of this note said,
the early nineteenth century. That misreading came from f. 17v, a printed broadside for the 1805
centenary of the coronation of the B.ma Vergine del Lago di Bertinoro, annotated **`= Bertinoro =`**
in the upper margin: a **later insert** filed with the dossier of an image crowned in 1705, not
evidence of the volume's date. The volume is a **dossier book** — the petitions, printed
commemorations, silversmiths' accounts and records deposited under step 5 above — and the marginal
place-name annotation is what makes it navigable. It closes (f. 302v) with the account of the
silversmith Giacomo Antonio Giardini *"in conto delle Corone d'Oro"*.

A full **TEI transcription** of ff. 1r–302v (713 pages) was produced with Vulgate.ai on 13 September
2026; the alignment of its `<pb>` elements to the BAV folio labels is pb *n* = image index − 2, and a
`pb-to-folio.csv` sidecar records it. Folios 303r–v were not transcribed.

### Limits

- **Not OCR'd.** These are page images only; there is no text layer, so the volume cannot be swept
  the way ASS and AAS were. Identification means reading the marginal place-names page by page, or
  working from a IIIF viewer.
- **Only one volume of the series is online.** The Sforza legacy runs from 1636 to the present, so
  the great majority of concessions are in tomes that are not digitized.
- `robots.txt` on digi.vatlib.it disallows `/search`, `/*/search`, `/*/index-search` and `/*/detail/*`,
  and sets `Crawl-delay: 10`. The listing pages and IIIF endpoints used here are permitted; any
  future harvesting should stay within those limits.

## Other series worth checking

Within the ACSP archives section, these may carry coronation material even though `Madonne.coron`
is the dedicated series:

`Decreti` (chapter decrees — the act of concession itself) · `caps` (*Capsulae*: 300+ containers of
private documents and papal bulls, 10th–19th c.) · `Privilegi.e.atti.not` · `Lettere.del.Cap` ·
`Inform` · `Misc.I`, `Misc.II` · `Varia`, `Varie`

None of these had a digitized item under the shelfmarks probed.

## Practical conclusion

To confirm a coronation not recorded in ASS/AAS, the route is:

1. Check whether the image's dossier falls in **tomo 4** (online, browsable by marginal place-name).
2. Otherwise apply to the **BAV** for the relevant `Madonne coronate` volume, or to the **Archivio
   Capitolare** at the Palazzo della Canonica for administrative records
   (`amministrazione@capitolosp.va`).

This is what [issue #1](https://github.com/CatholicOS/imagines-coronatae/issues/1) (Piekary Śląskie)
is waiting on. Tomo 4 covers 1689–1714, so a crowning of the 1920s will not be in the digitized
volume.

## Sources

- DigiVatLib, archives section: <https://digi.vatlib.it/arc/Arch.Cap.S.Pietro>
- DigiVatLib, manuscripts section: <https://digi.vatlib.it/mss/Arch.Cap.S.Pietro>
- Basilica di San Pietro, *Gli Archivi della Basilica*:
  <https://www.basilicasanpietro.va/it/san-pietro/gli-archivi-della-basilica>
- Edizioni Capitolo Vaticano, *L'Archivio Capitolare*:
  <https://www.edizionicapitolovaticano.it/archivio-2/>
- *Santa Maria dei Bisognosi: anno 1724, L'incoronazione* — the study whose citations established the
  form `BAV, ACSP, Madonne coronate, tomo I, foglio N (mecc. N)` and the procedure:
  <https://pereto.org/documenti/bisognosi/>
- ACI Stampa, *Nel Museo del Tesoro di San Pietro le "Madonne Coronate" dal Capitolo della basilica*:
  <https://www.acistampa.com/story/nel-museo-del-tesoro-di-san-pietro-le-madonne-coronate-dal-capitolo-della-basilica>
