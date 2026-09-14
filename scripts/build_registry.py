import json,collections,datetime,os,re,pathlib,unicodedata as U
REPO=str(pathlib.Path(__file__).resolve().parent.parent)
I=json.load(open(os.path.join(REPO,'data','imagines-coronatae.json'),encoding='utf-8'))['images']
EV={'papal_coronation_act':'act','papal_legate_deputation':'legate','papal_personal_coronation':'by pope',
    'retrospective_attestation':'retro','norms':'norms','petition_not_conceded':'NOT conceded'}
CONF={'high':'●●●','medium':'●●○','low':'●○○'}
def esc(s): return re.sub(r'\s+',' ',str(s or '')).replace('|','\\|').strip()
def title(im): return esc(im.get('image_title_vernacular') or im.get('image_title_latin') or '—')
def _t(s):
    if not s: return set()
    s=U.normalize('NFKD',str(s).translate(str.maketrans({'ł':'l','Ł':'l'}))).encode('ascii','ignore').decode().lower()
    return {x for x in re.split(r'[^a-z0-9]+',s) if len(x)>2}
def place(im):
    loc=im.get('locality'); dio=im.get('diocese_modern') or im.get('diocese_latin')
    bits=[b for b in (loc,dio) if b]
    if loc and dio and (_t(dio)&_t(loc)): bits=[loc]
    return esc(', '.join(dict.fromkeys(bits)))
def when(im):
    d=im.get('coronation_dates') or []
    return esc('; '.join(d)) if d else ''
def srcs(im):
    out=[]
    for s in im['sources']:
        c=esc(s.get('citation')); u=s.get('source_pdf_url')
        tag=EV.get(s.get('evidence_type'),'')
        out.append(f"[{c}]({u}) *{tag}*" if (c and u) else f"{c} *{tag}*")
    return '<br>'.join(out)

HEAD="""<!-- GENERATED FILE — do not edit by hand.
     Regenerate with: python3 scripts/build_registry.py -->

"""
LEGEND="""Each row is **one crowned image**. The *Sources* column lists every act in
*Acta Sanctae Sedis* (ASS, 1865–1908) or *Acta Apostolicae Sedis* (AAS, 1909– ) that attests it,
linked to the source PDF on vatican.va — an image cited in several volumes is one row with several
sources, not several rows.

**Evidence tags** — `act` the granting act itself · `legate` a Cardinal Legate deputed to crown ·
`by pope` the Pope crowned it in person · `retro` a later act mentions an earlier crowning ·
`norms` general legislation · `NOT conceded` a petition the Chapter never granted — the image was not crowned by it.
**Conf.** — ●●● explicit · ●●○ some inference (usually country from the Latin diocese) ·
●○○ fragmentary, verify against the printed page.

Where *Crowned* shows more than one date, the image was crowned more than once — typically a
Vatican Chapter crowning later renewed by a Pope.

"""
n_src=sum(i['source_count'] for i in I)

# ---- by country ----
byc=collections.defaultdict(list)
for im in I: byc[im.get('country') or '— unstated —'].append(im)
ck=lambda k:(k.startswith('—'),k)
L=[HEAD,"# Registry of crowned images — by country\n\n",
   f"**{len(I)} images** · {len([k for k in byc if not k.startswith('—')])} countries · "
   f"{n_src} source citations · generated {datetime.date.today().isoformat()}\n\n",LEGEND,
   "**Contents:** "+" · ".join(f"[{esc(k)}](#{re.sub(r'[^a-z0-9]+','-',k.lower()).strip('-')})" for k in sorted(byc,key=ck))+"\n\n---\n\n"]
for c in sorted(byc,key=ck):
    rs=sorted(byc[c],key=lambda im:(place(im).lower(),title(im).lower()))
    L.append(f"## {esc(c)}\n\n*{len(rs)} image{'s' if len(rs)!=1 else ''}*\n\n")
    L.append("| Image | Place | Crowned | Evidence | Sources | Conf. |\n|---|---|---|---|---|---|\n")
    for im in rs:
        L.append(f"| {title(im)} | {place(im)} | {when(im)} | {EV.get(im.get('strongest_evidence'),'')} | {srcs(im)} | {CONF.get(im.get('confidence'),'')} |\n")
    L.append("\n")
open(os.path.join(REPO,'registry','by-country.md'),'w',encoding='utf-8').write(''.join(L))

# ---- chronological ----
def yr(im):
    d=im.get('first_coronation') or ''
    m=re.match(r'(\d{4})',str(d))
    if m: return int(m.group(1))
    ys=[s.get('year') for s in im['sources'] if s.get('year')]
    return min(ys) if ys else 9999
rs=sorted(I,key=lambda im:(yr(im),str(im.get('first_coronation') or ''),title(im).lower()))
L=[HEAD,"# Registry of crowned images — chronological\n\n",
   f"**{len(I)} images** · {n_src} source citations · generated {datetime.date.today().isoformat()}\n\n",
   "Ordered by the date the image was crowned where a source gives it, otherwise by the earliest act attesting it.\n\n",LEGEND]
cur=None
for im in rs:
    y=yr(im); lab=f"{(y//10)*10}s" if y!=9999 else "Undated"
    if lab!=cur:
        cur=lab
        L.append(f"\n## {lab}\n\n| Crowned | Image | Place | Country | Evidence | Sources | Conf. |\n|---|---|---|---|---|---|---|\n")
    L.append(f"| {when(im)} | {title(im)} | {place(im)} | {esc(im.get('country'))} | {EV.get(im.get('strongest_evidence'),'')} | {srcs(im)} | {CONF.get(im.get('confidence'),'')} |\n")
open(os.path.join(REPO,'registry','chronological.md'),'w',encoding='utf-8').write(''.join(L))
print('wrote registry/by-country.md and registry/chronological.md')
print('images:',len(I),'| source citations:',n_src,'| countries:',len([k for k in byc if not k.startswith('—')]))
