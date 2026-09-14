"""Report on the Basilici-Bigliazzi layer: what their schede add to the catalogue, and where they disagree.

Reads the built catalogue (data/imagines-coronatae.json) and the database (data/basilici-bigliazzi-2025-db.json)
and writes docs/BASILICI-BIGLIAZZI.md and the row-level data/basilici-in-catalogue.csv: for every scheda,
whether it was taken into the catalogue (and if not, why), the image it sits in, the other sources of that
image, and whether their date agrees with the others'. Successor of the cross-match that was run while the
database was still kept outside the catalogue.
"""
import json,csv,collections,datetime,pathlib,re
REPO=pathlib.Path(__file__).resolve().parent.parent
B=json.load(open(REPO/'data/basilici-bigliazzi-2025-db.json',encoding='utf-8'))
I=json.load(open(REPO/'data/imagines-coronatae.json',encoding='utf-8'))['images']
ROME=json.load(open(REPO/'data/basilici-rome-alignment.json',encoding='utf-8'))['rows']
def work(s):
    if s['series']!='LIT': return s['series']
    return (re.match(r'[A-Za-z]*',str(s.get('act_number') or '')) or re.match('','')).group(0)
WORK={'ASS':'ASS','AAS':'AAS','ACSP':'ACSP','Br':'Briccolani','Bo':'Bombelli','Z':'Zander/Magister','ZV':'Zander/Magister','B':'Balzamo','':'Vrabelová','BB':'Basilici–Bigliazzi'}
where={}
for im in I:
    for s in im['sources']:
        if str(s.get('act_number','')).startswith('BB'): where[int(s['act_number'][2:])]=im
rows=[]
for s in B['rows']:
    taken=s['row'] in where
    why='' if taken else ('petition refused or crowning uncertain (incoronazione #)' if s['incoronazione']=='#' else 'not verified by them (data verificata: no)' if s['data_verificata']=='no' else 'not verified')
    im=where.get(s['row'])
    others=[x for x in im['sources'] if not str(x.get('act_number','')).startswith('BB')] if im else []
    y=int(s['coronation_date'][:4]) if s['coronation_date'] else None
    oy={int(str(x.get('coronation_date') or x.get('concession_date') or '')[:4]) for x in others if str(x.get('coronation_date') or x.get('concession_date') or '')[:4].isdigit()}
    agrees='' if not (y and oy) else 'yes' if y in oy else '±1' if any(abs(y-z)<=1 for z in oy) else 'no'
    rows.append({'row':s['row'],'id':s['id'],'nation':s['nation'],'localita':s['localita'],'titolo':s['titolo'],
      'data_incoronazione':s['data_incoronazione'],'autorizza':s['autorizza'],'data_verificata':s['data_verificata'],
      'incoronazione':s['incoronazione'],'taken':'yes' if taken else 'no','why_not':why,
      'image_id':im['id'] if im else '','image_locality':im['locality'] if im else '',
      'image_title':(im['image_title_vernacular'] or im['image_title_latin'] or '') if im else '',
      'image_dates':'; '.join(im['coronation_dates']) if im else '',
      'other_sources':'; '.join(sorted({WORK.get(work(x),work(x)) for x in others})),'date_agrees':agrees,
      'rome_alignment':ROME.get(str(s['row']),{}).get('how',''),'annotazioni':s['annotazioni']})
with open(REPO/'data/basilici-in-catalogue.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# ---- figures ----
n=len(rows); T=[r for r in rows if r['taken']=='yes']; NT=[r for r in rows if r['taken']=='no']
corr=[r for r in T if r['other_sources']]; alone=[r for r in T if not r['other_sources']]
bb_only=[im for im in I if all(str(s.get('act_number','')).startswith('BB') for s in im['sources'])]
def cent(d): return int(d.split('-')[-1])//100*100 if d and d.split('-')[-1].isdigit() else None
by_cent=collections.Counter(cent(r['data_incoronazione']) for r in alone)
by_auth=collections.Counter((r['autorizza'] or '#').rstrip('.') for r in alone)
by_nation=collections.Counter(r['nation'] for r in alone)
agree=collections.Counter(r['date_agrees'] for r in corr)
disagree=[r for r in corr if r['date_agrees']=='no']
no_scheda=[im for im in I if not any(str(s.get('act_number','')).startswith('BB') for s in im['sources'])]
ns_series=collections.Counter('+'.join(sorted({x['series'] for x in im['sources']})) for im in no_scheda)
ns_ev=collections.Counter(im['strongest_evidence'] for im in no_scheda)
ns_country=collections.Counter(im['country'] for im in no_scheda)
children=sum(1 for v in ROME.values() if v['child_of'] is not None)
def pct(a,b): return f"{100*a/b:.0f}%"

L=[]
L.append(f"""# The Basilici–Bigliazzi database in the catalogue

Generated {datetime.date.today().isoformat()} by `scripts/report_basilici.py`; the row-level result is
`data/basilici-in-catalogue.csv`, the database itself `data/basilici-bigliazzi-2025-db.json`.

## What it is

Massimo Basilici and Rita Bigliazzi, *Le Madonne Coronate* (four volumes, 2025), publish their
research as a database at <https://www.pereto.org/madonne_coronate/>: **{n:,} schede**, one per crowning
they examined, 1631–1981, each with locality, church, title, date of crowning, date of the decree
where known, the authorising body (`Autorizza`: the Chapter, a papal brief, Count Sforza, a Pope) and
a verdict (`Data verificata: sì/no`) on whether they found evidence that the crowning really took
place under that authority. By their own account the list was built from Anselmo da Reno Centese's
catalogue of 1933, the printed repertories (Briccolani, Bonci) and the internet, with the archive
consulted for particular cases; so it is a **secondary compilation citing no folio**, and every row
of it enters the catalogue as series `LIT`, confidence `low`, with their authority, officiant,
decree date and notes carried in the source's `notes`.

## What was taken

| | schede |
|---|---|
| in the database | {n:,} |
| taken into the catalogue — *verificata: sì* and a real crowning (1st, 2nd or 3rd) | {len(T):,} |
| — corroborating an image another source already attests | {len(corr):,} |
| — the only source of an image | {len(alone):,} ({len(bb_only):,} images) |
| left out — *incoronazione #* (uncertain, or a petition the Chapter refused) or *verificata: no* | {len(NT):,} |

Their `Autorizza` becomes the record's `evidence_type`: *Capitolo* and *Conte Sforza* →
`chapter_decree`; *B.P.* (a papal brief) → `papal_coronation_act`; a Pope who also officiated →
`papal_personal_coronation`; `#` (authority they could not establish) → `retrospective_attestation`.

**Rome.** They describe a Roman church at length ("Basilica di Santa Maria in Trastevere nella
Cappella Altemps"), which the catalogue's church-signature rule cannot see, so their {len(ROME)} Roman
schede are aligned by hand to the catalogue's own church strings in `data/basilici-rome-alignment.json`
(`scripts/align_basilici_rome.py`); {children} of them are the separate crown for the Child of an image
crowned earlier — Briccolani's twelve *Bambino Gesù* concessions — which they file as first crownings,
and which are linked to their image by `parent_act` and not counted as re-crownings.

## What they add

{len(bb_only):,} images rest on their database alone. By century, authority and country:

| Century | Images |
|---|---|""")
for c,v in sorted((k,v) for k,v in by_cent.items() if k): L.append(f"| {c}s | {v} |")
L.append("\n| Authority (their `Autorizza`) | Schede |\n|---|---|")
for a,v in by_auth.most_common(): L.append(f"| {a} | {v} |")
L.append("\n| Country | Schede |\n|---|---|")
for a,v in by_nation.most_common(20): L.append(f"| {a} | {v} |")
L.append(f"""
The shape is what the sources predict: the catalogue's primary layers are the two gazettes and one
dossier volume, its registers stop at 1800 (Briccolani) and Rome (Bombelli); what Basilici–Bigliazzi
supply is the Chapter's and the briefs' coronations of the nineteenth and twentieth centuries — the
volumes of *Madonne coronate* that are not online, seen through Anselmo's 1933 list and its
continuators. Every such image is `low`, and says in its notes what it rests on.

## Where the two disagree on the date

Of the {len(corr):,} schede that corroborate an image known from another source, the year agrees exactly
in {agree['yes']}, is one off in {agree['±1']}, differs in {agree['no']}, and cannot be compared in {agree['']}
(the other source gives no date). The {len(disagree)} disagreements — a year or more apart — are kept
as the sources give them, so such an image shows two dates; the first thirty:

| Their scheda | Their date | The other source's date |
|---|---|---|""")
for r in disagree[:30]:
    L.append(f"| {r['titolo']} — {r['localita']} | {r['data_incoronazione']} | {r['image_dates']} ({r['other_sources']}) |")
L.append(f"""
For the 1750s–1790s their dates run two or three years later than Briccolani's — Antegnate
1751/1753, Chiavari 1767/1769 — which is the difference between the year of the decree and the year
of the ceremony; the `notes` of many rows say so ("scambia la data del decreto con la data
dell'incoronazione").

## Images they do not record

{len(no_scheda):,} of the catalogue's {len(I):,} images have no scheda. By evidence and by the series that attest them:

| Strongest evidence | Images |
|---|---|""")
for a,v in ns_ev.most_common(): L.append(f"| `{a}` | {v} |")
L.append("\n| Series | Images |\n|---|---|")
for a,v in ns_series.most_common(): L.append(f"| {a} | {v} |")
L.append("\n| Country | Images |\n|---|---|")
for a,v in ns_country.most_common(12): L.append(f"| {a} | {v} |")
L.append("""
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
""")
open(REPO/'docs/BASILICI-BIGLIAZZI.md','w',encoding='utf-8').write('\n'.join(L))
print(f"schede {n} taken {len(T)} corroborating {len(corr)} alone {len(alone)} | BB-only images {len(bb_only)} | images without scheda {len(no_scheda)} | date disagreements {len(disagree)}")
print('agree',agree)
