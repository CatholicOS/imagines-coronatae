"""Cross-match the Basilici–Bigliazzi database against the catalogue, in both directions.

Input : data/basilici-bigliazzi-2025-db.json (their 1,737 schede), data/imagines-coronatae.json
Output: data/crossmatch-basilici.csv   — one row per scheda: matched image (if any) and how
        docs/CROSSMATCH-BASILICI.md    — the report

Matching uses the catalogue's own place and title normalisation (imported from build_images.py) so
that the two sides are compared on the same footing: a scheda and an image are the same crowning
when they share a place token (their `localita` or `luogo_di_culto` against the image's locality)
and either a title word or a coronation year; for Rome, as in the catalogue, a shared church word
is required as well. No fuzzier than that, on purpose — the point is to find the gaps, and a
false match hides one.
"""
import json,csv,collections,pathlib,datetime
REPO=pathlib.Path(__file__).resolve().parent.parent
# borrow the catalogue's normalisation (everything before the clustering starts)
_src=open(REPO/'scripts/build_images.py',encoding='utf-8').read()
_ns={'__file__':str(REPO/'scripts/build_images.py')}
exec(_src[:_src.index('tokloc=collections.defaultdict(set)')],_ns)
loc_toks,title_full,norm,toks,rome_sig,SYN,TITLE_STOP,CITY=(_ns[k] for k in ('loc_toks','title_full','norm','toks','rome_sig','SYN','TITLE_STOP','CITY'))

B=json.load(open(REPO/'data/basilici-bigliazzi-2025-db.json',encoding='utf-8'))
I=json.load(open(REPO/'data/imagines-coronatae.json',encoding='utf-8'))['images']

NATION={'Italia':'Italy','Francia':'France','Polonia':'Poland','Belgio':'Belgium','Ucraina':'Ukraine','Spagna':'Spain',
 'Città del Vaticano':'Italy','Lituania':'Lithuania','Austria':'Austria','Repubblica Ceca':'Czech Republic','Messico':'Mexico',
 'Olanda':'Netherlands','Argentina':'Argentina','Bielorussia':'Belarus','Svizzera':'Switzerland','Croazia':'Croatia',
 'Slovenia':'Slovenia','Germania':'Germany','Malta':'Malta','Portogallo':'Portugal','Brasile':'Brazil','Perù':'Peru',
 'Colombia':'Colombia','Venezuela':'Venezuela','Ecuador':'Ecuador','Cile':'Chile','Filippine':'Philippines','Canada':'Canada',
 'Stati Uniti':'United States','Turchia':'Turkey','Ungheria':'Hungary','Slovacchia':'Slovakia','Lettonia':'Latvia',
 'Regno Unito':'United Kingdom','Inghilterra':'United Kingdom','Irlanda':'Ireland','Algeria':'Algeria','Uruguay':'Uruguay',
 'Bolivia':'Bolivia','Paraguay':'Paraguay','Cuba':'Cuba','Guatemala':'Guatemala','Nicaragua':'Nicaragua','Costa Rica':'Costa Rica',
 'El Salvador':'El Salvador','Honduras':'Honduras','Panama':'Panama','Repubblica Dominicana':'Dominican Republic',
 'Porto Rico':'Puerto Rico','India':'India','Sri Lanka':'Sri Lanka','Libano':'Lebanon','Australia':'Australia','Romania':'Romania',
 'Bosnia ed Erzegovina':'Bosnia and Herzegovina','Serbia':'Serbia','Montenegro':'Montenegro','Albania':'Albania','Grecia':'Greece',
 'Lussemburgo':'Luxembourg','Egitto':'Egypt','Giappone':'Japan','Cina':'China','Vietnam':'Vietnam','Indonesia':'Indonesia',
 'Sud Africa':'South Africa','Marocco':'Morocco','Tunisia':'Tunisia','Siria':'Syria','Israele':'Israel','Palestina':'Palestine',
 'Russia':'Russia','Moldavia':'Moldova','Danimarca':'Denmark','Svezia':'Sweden','Norvegia':'Norway','Finlandia':'Finland'}

def srec(s):
    """A scheda as a pseudo-record for the catalogue's token functions."""
    loc=s['localita'] or ''
    church=s['luogo_di_culto']
    if s['nation']=='Città del Vaticano': loc,church='Rome, Vatican',None     # the Basilica itself: the title carries it
    elif s['nation']=='Italia' and s['region']=='Lazio' and norm(loc).startswith('roma'):
        loc='Rome, '+(s['luogo_di_culto'] or '')
    return {'locality':loc,'image_title_vernacular':' / '.join(x for x in (s['titolo'],s['altro_titolo']) if x),
            'church_or_sanctuary':church,'coronation_date':s['coronation_date']}
def irec(im):
    return {'locality':im['locality'],'image_title_vernacular':' / '.join(x for x in (im.get('image_title_vernacular'),im.get('image_title_latin')) if x),
            'church_or_sanctuary':im.get('church_or_sanctuary'),'coronation_date':None}
def years(im): return {int(d[:4]) for d in im['coronation_dates'] if d[:4].isdigit()}
def church_toks(r): return {t for t in toks(r.get('church_or_sanctuary')) if t not in TITLE_STOP}

# index images by country and by place token
by_tok=collections.defaultdict(set)
IR=[irec(im) for im in I]
for k,r in enumerate(IR):
    for t in loc_toks(r): by_tok[t].add(k)

rows=[];matched_images=collections.defaultdict(list)
for s in B['rows']:
    r=srec(s); lt=loc_toks(r); ct=church_toks(r); tt=title_full(r)
    y=int(s['coronation_date'][:4]) if s['coronation_date'] else None
    country=NATION.get(s['nation'])
    cands=set()
    for t in lt|ct: cands|=by_tok.get(t,set())
    best=None;how=None
    for k in sorted(cands):
        im=I[k]; ir=IR[k]
        if country and im.get('country') and im['country']!=country: continue
        il=loc_toks(ir)
        if 'rome' in lt or 'rome' in il:
            if not ('rome' in lt and 'rome' in il): continue
            sa,sb=rome_sig(lt|ct),rome_sig(il|church_toks(ir))
            if sa and sb:
                if not (sa&sb): continue
                place='church'
            else:
                place='rome-title'     # no church on one side (e.g. 'Città del Vaticano'): the title must carry it
        else:
            if not (lt&il): continue          # the locality itself, never a church word (a 'San Giorgio' is not Venice)
            place='place'
        it=title_full(ir)
        tmatch=bool(tt&it) or bool({t[:7] for t in tt if len(t)>=7}&{t[:7] for t in it if len(t)>=7})
        ymatch=y is not None and any(abs(y-iy)<=1 for iy in years(im))
        exact=y is not None and y in years(im)
        if tmatch and ymatch: score=3
        elif tmatch: score=2
        elif exact and place!='rome-title': score=1     # a year alone must be the same year, not one off
        else: continue
        # a title-only or year-only match between records that name DIFFERENT churches is no match
        # (Naples' Madonna delle Grazie of 1726 is not the one at Pietra del Pesce of 1786)
        if score==2:
            ci=church_toks(ir)|{t for t in il if t not in lt}
            if ct and ci and not (ct&ci) and not ({t[:7] for t in ct if len(t)>=7}&{t[:7] for t in ci if len(t)>=7}): continue
        if best is None or score>best[0]: best=(score,k,place,('title+year' if score==3 else 'title' if score==2 else 'year'))
    if best:
        _,k,place,h=best; how=f"{place}+{h}"; matched_images[k].append(s['row'])
        im=I[k]
        rows.append({'row':s['row'],'id':s['id'],'nation':s['nation'],'localita':s['localita'],'titolo':s['titolo'],
          'data_incoronazione':s['data_incoronazione'],'autorizza':s['autorizza'],'data_verificata':s['data_verificata'],
          'incoronazione':s['incoronazione'],'match':how,'image_id':im['id'],'image_locality':im['locality'],
          'image_title':im.get('image_title_vernacular') or im.get('image_title_latin'),'image_dates':'; '.join(im['coronation_dates']),
          'image_series':'+'.join(sorted({x['series'] for x in im['sources']})),
          'date_agrees':'yes' if (y and y in years(im)) else ('±1' if (y and any(abs(y-iy)==1 for iy in years(im))) else ('no' if y and years(im) else '')),
          'annotazioni':s['annotazioni']})
    else:
        rows.append({'row':s['row'],'id':s['id'],'nation':s['nation'],'localita':s['localita'],'titolo':s['titolo'],
          'data_incoronazione':s['data_incoronazione'],'autorizza':s['autorizza'],'data_verificata':s['data_verificata'],
          'incoronazione':s['incoronazione'],'match':'','image_id':'','image_locality':'','image_title':'','image_dates':'',
          'image_series':'','date_agrees':'','annotazioni':s['annotazioni']})

with open(REPO/'data/crossmatch-basilici.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

# ---- report ----
n=len(rows); m=[r for r in rows if r['match']]; um=[r for r in rows if not r['match']]
def pct(a,b): return f"{100*a/b:.0f}%"
verified=[r for r in rows if r['data_verificata']=='sì']
um_ver=[r for r in um if r['data_verificata']=='sì' and r['incoronazione'] in ('1','2','3')]
by_nation=collections.Counter(r['nation'] for r in um_ver)
by_auth=collections.Counter(r['autorizza'] for r in um_ver)
by_cent=collections.Counter((int(r['data_incoronazione'].split('-')[-1])//100*100 if r['data_incoronazione'] and r['data_incoronazione'].split('-')[-1].isdigit() else None) for r in um_ver)
agree=collections.Counter(r['date_agrees'] for r in m)
# images not in the database
unmatched_images=[im for k,im in enumerate(I) if k not in matched_images]
ui_series=collections.Counter('+'.join(sorted({x['series'] for x in im['sources']})) for im in unmatched_images)
ui_country=collections.Counter(im['country'] for im in unmatched_images)
ui_ev=collections.Counter(im['strongest_evidence'] for im in unmatched_images)
# images the database dates differently
disagree=[r for r in m if r['date_agrees']=='no']

L=[]
L.append(f"""# Cross-match: the Basilici–Bigliazzi database against this catalogue

Generated {datetime.date.today().isoformat()} by `scripts/crossmatch_basilici.py`; the row-level result is
`data/crossmatch-basilici.csv`, the database itself `data/basilici-bigliazzi-2025-db.json`.

## What was compared

Massimo Basilici and Rita Bigliazzi, *Le Madonne Coronate* (four volumes, 2025), publish their
research as a database at <https://www.pereto.org/madonne_coronate/>: **{n:,} schede**, one per crowning
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
| in the database | {n:,} |
| matched to a catalogue image | {len(m):,} ({pct(len(m),n)}) |
| — on title and year | {sum(1 for r in m if r['match'].endswith('title+year')):,} |
| — on title only | {sum(1 for r in m if r['match'].endswith('+title')):,} |
| — on year only | {sum(1 for r in m if r['match'].endswith('+year') and not r['match'].endswith('title+year')):,} |
| not in the catalogue | {len(um):,} ({pct(len(um),n)}) |
| — of which they mark *verificata: sì* and a real crowning (1st/2nd) | {len(um_ver):,} |

Of the {len(m):,} matches, the year agrees exactly in {agree.get('yes',0):,}, is one off in {agree.get('±1',0):,},
differs in {agree.get('no',0):,}, and cannot be compared in {agree.get('',0):,}.

### Gaps in the catalogue: crownings they record that this catalogue lacks

{len(um_ver):,} schede that they mark as verified crownings have no counterpart here. By period, authority and country:

| Century | Schede |
|---|---|""")
for c,v in sorted((k,v) for k,v in by_cent.items() if k): L.append(f"| {c}s | {v} |")
L.append("\n| Authority (their `Autorizza`) | Schede |\n|---|---|")
for a,v in by_auth.most_common(): L.append(f"| {a} | {v} |")
L.append("\n| Country | Schede |\n|---|---|")
for a,v in by_nation.most_common(20): L.append(f"| {a} | {v} |")
L.append(f"""
The shape is what the sources predict. The catalogue's primary layers are the two gazettes and one
dossier volume (1689–1714); its literature layer is Briccolani to 1791 and Bombelli for Rome, Vrabelová for Central Europe
to 1786, Balzamo's lists to 1798 and the 89 painted copies of Zander/Magister. Before 1800 the two
lists nearly coincide: {by_cent.get(1600,0)+by_cent.get(1700,0)} of their verified crownings of the seventeenth and eighteenth
centuries are unmatched here, and on inspection about half of those are the same crowning under a
locality this matching could not align (Tolfa for Cibona, Nova Gorica for Monte Santo, Dobrzyń nad
Wisłą for Skępe, Leopoli for Lwów, Monte San Giuliano for Custonaci, or a year two or three off — see
below). The rest are genuine absences, mostly omissions of Briccolani's list: Reggio Calabria 1722,
Meta 1748, Piancastagnaio 1751, Pescasseroli 1752, Scurcola Marsicana 1757, Verona's Madonna del
Popolo 1770, Paternopoli 1774, Cesena 1782 (by Pius VI), Roccadaspide 1786, Sinalunga 1793,
Catanzaro 1797, and a few Roman and Neapolitan images (Costantinopoli 1651, Gioie 1679, Naples'
Grazie 1726 and Addolorata 1761). After 1800 the
catalogue has only what a gazette or Zander/Magister happened to record, and that is what the
other {by_cent.get(1800,0)+by_cent.get(1900,0):,} rows are: the Chapter's Italian coronations of the nineteenth century and the
Chapter and papal-brief coronations of 1900–1981 in Italy, Spain, France and Latin America — the
volumes 12–36 of *Madonne coronate* and the *Madonne incoronate* of the Archivio Capitolare, seen
through Anselmo's 1933 list and its continuators.

### Gaps in the database: images here that they do not record

{len(unmatched_images):,} of the catalogue's {len(I):,} images found no scheda. By evidence and by the series that attest them:

| Strongest evidence | Images |
|---|---|""")
for a,v in ui_ev.most_common(): L.append(f"| `{a}` | {v} |")
L.append("\n| Series | Images |\n|---|---|")
for a,v in ui_series.most_common(): L.append(f"| {a} | {v} |")
L.append("\n| Country | Images |\n|---|---|")
for a,v in ui_country.most_common(12): L.append(f"| {a} | {v} |")
L.append(f"""
Two kinds of image sit here. First, and most of them, the **papal crownings the gazettes record**
— {ui_series.get('AAS',0)+ui_series.get('ASS',0)+ui_series.get('AAS+ASS',0)} images attested only by ASS/AAS: a Legate's coronation in Colombia or the Philippines, the
*Litterae Apostolicae* of the 1980s and 1990s (they stop at 1981), and the {ui_country.get('Poland',0)} Polish images most of
which John Paul II crowned. Their database follows the Chapter and Anselmo, and the papal acts of
the gazettes are largely outside it — which is the catalogue's own contribution. Second, a few
dozen images from the literature layer — Briccolani's Roman entries that their Rome schede name by
a different church, Balzamo's town-and-year rows — where a good number will be the same images
under different names, and some genuine absences; they are the rows with an empty `match` in the
CSV.

### Where the two disagree on the date

{len(disagree):,} matched crownings carry a year here that differs from theirs by more than one. A sample:

| Their scheda | Their date | Catalogue image | Catalogue dates |
|---|---|---|---|""")
for r in disagree[:30]:
    L.append(f"| {r['titolo']} — {r['localita']} | {r['data_incoronazione']} | {r['image_title']} — {r['image_locality']} | {r['image_dates']} |")
L.append(f"""
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

- To **extend the catalogue**, the {len(um_ver):,} unmatched verified schede are the work-list: each names
  a locality, a church and a year, which is enough to find the dossier in the right volume of
  *Madonne coronate* (Zander/Magister's citations give the volume for each decade) and, for 1865
  onwards, to search the gazettes for a retrospective mention.
- To **check the catalogue**, the {len(disagree):,} date disagreements and the {agree.get('±1',0):,} one-year offsets are
  the places to look first.
- Their `Autorizza = B.P.` rows ({sum(1 for r in rows if r['autorizza']=='B.P.'):,}) are crownings by papal brief; from 1865 these ought to
  be in ASS/AAS, and any that are unmatched here are candidates for a missed act.
""")
open(REPO/'docs/CROSSMATCH-BASILICI.md','w',encoding='utf-8').write('\n'.join(L))
print('schede',n,'matched',len(m),'unmatched',len(um),'unmatched verified crownings',len(um_ver))
print('images without a scheda',len(unmatched_images),'| date disagreements',len(disagree))
print('agree',agree)
