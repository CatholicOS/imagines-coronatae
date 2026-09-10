import json,collections,datetime,os,re
REPO='/home/johnrdorazio/development/CatholicOS_org/imagines-coronatae'
R=json.load(open(os.path.join(REPO,'data','imagines-coronatae.json')))['records']

EV={'papal_coronation_act':'act','papal_legate_deputation':'legate',
    'papal_personal_coronation':'by pope','retrospective_attestation':'retro','norms':'norms'}
def esc(s):
    if s is None: return ''
    return re.sub(r'\s+',' ',str(s)).replace('|','\\|').strip()
def title(r):
    t=r.get('image_title_vernacular') or r.get('image_title_latin') or ''
    return esc(t)
import unicodedata as _u
def _tok(s):
    if not s: return set()
    s=str(s).translate(str.maketrans({'\u0142':'l','\u0141':'l'}))
    s=_u.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return {t for t in re.split(r'[^a-z0-9]+',s) if len(t)>2}
def place(r):
    loc=r.get('locality'); dio=r.get('diocese_modern') or r.get('diocese_latin')
    bits=[b for b in (loc,dio) if b]
    # drop the diocese when it merely repeats the locality
    if loc and dio and (_tok(dio) & _tok(loc)): bits=[loc]
    return esc(', '.join(dict.fromkeys(bits)))
def when(r):
    return esc(r.get('coronation_date') or r.get('act_date') or '')
def cite(r):
    c=esc(r.get('citation')); u=r.get('source_pdf_url')
    return f"[{c}]({u})" if (c and u) else c
def conf(r):
    return {'high':'●●●','medium':'●●○','low':'●○○'}.get(r.get('confidence'),'')

HEADER="""<!-- GENERATED FILE — do not edit by hand.
     Regenerate with: python3 scripts/build_registry.py -->

"""
INTRO_COMMON = """Each row cites the act in *Acta Sanctae Sedis* (ASS, 1865–1908) or
*Acta Apostolicae Sedis* (AAS, 1909– ), linked to the source PDF on vatican.va.

**Evidence** — how the act attests the crowning:
`act` the granting act itself · `legate` a Cardinal Legate deputed to crown ·
`by pope` the Pope crowned it in person · `retro` a later act mentions an earlier crowning ·
`norms` general legislation.
**Conf.** — ●●● explicit · ●●○ some inference (usually country from the Latin diocese) ·
●○○ fragmentary, verify against the printed page.

"""

# ---------- 1. by country ----------
byc=collections.defaultdict(list)
for r in R: byc[r.get('country') or '— unstated —'].append(r)
def ckey(k): return (k.startswith('—'),k)
lines=[HEADER,"# Registry of crowned images — by country\n\n",
 f"{len(R)} records · {len([k for k in byc if not k.startswith('—')])} countries · "
 f"generated {datetime.date.today().isoformat()}\n\n",INTRO_COMMON,
 "**Contents:** "+" · ".join(f"[{esc(k)}](#{re.sub(r'[^a-z0-9]+','-',k.lower()).strip('-')})" for k in sorted(byc,key=ckey))+"\n\n---\n\n"]
for c in sorted(byc,key=ckey):
    rs=sorted(byc[c],key=lambda r:(place(r).lower(),r.get('year') or 0))
    lines.append(f"## {esc(c)}\n\n*{len(rs)} record{'s' if len(rs)!=1 else ''}*\n\n")
    lines.append("| Image | Place | Crowned / act date | Evidence | Source | Conf. |\n|---|---|---|---|---|---|\n")
    for r in rs:
        lines.append(f"| {title(r)} | {place(r)} | {when(r)} | {EV.get(r['evidence_type'],'')} | {cite(r)} | {conf(r)} |\n")
    lines.append("\n")
open(os.path.join(REPO,'registry','by-country.md'),'w',encoding='utf-8').write(''.join(lines))

# ---------- 2. chronological ----------
def sortkey(r):
    d=r.get('coronation_date') or r.get('act_date') or ''
    m=re.match(r'(\d{4})',str(d))
    return (int(m.group(1)) if m else (r.get('year') or 9999), str(d))
rs=sorted(R,key=sortkey)
lines=[HEADER,"# Registry of crowned images — chronological\n\n",
 f"{len(R)} records · generated {datetime.date.today().isoformat()}\n\n",
 "Ordered by the date the image was crowned where the source gives it, otherwise by the date of the act.\n\n",
 INTRO_COMMON]
cur=None
for r in rs:
    y=sortkey(r)[0]
    dec=(y//10)*10 if y!=9999 else None
    lab=f"{dec}s" if dec else "Undated"
    if lab!=cur:
        cur=lab
        lines.append(f"\n## {lab}\n\n| Date | Image | Place | Country | Evidence | Source | Conf. |\n|---|---|---|---|---|---|---|\n")
    lines.append(f"| {when(r)} | {title(r)} | {place(r)} | {esc(r.get('country'))} | {EV.get(r['evidence_type'],'')} | {cite(r)} | {conf(r)} |\n")
open(os.path.join(REPO,'registry','chronological.md'),'w',encoding='utf-8').write(''.join(lines))
print('wrote registry/by-country.md and registry/chronological.md')
print('records:',len(R),'countries:',len([k for k in byc if not k.startswith('—')]))
