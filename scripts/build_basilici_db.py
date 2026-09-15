"""Basilici–Bigliazzi (2025), *Le Madonne Coronate* — the companion database, normalised.

Massimo Basilici and Rita Bigliazzi, *Le Madonne Coronate: anni 1631-1750; 1751-1900; 1901-1931;
1932-1981* (four volumes, 2025), publish their research as a searchable database at
https://www.pereto.org/madonne_coronate/ — one *scheda* per crowning, 1,737 in all, "per rendere
disponibili i dati della ricerca". This script turns the fetched schede into one JSON file.

Input : a directory of scheda HTML files as returned by the site's `api/get.php` (one per row; the
        row numbers and the date index come from the `const DATA` block of `by_date.php`), plus the
        `rows.json` index written by the fetch. The fetch itself (one request a second) is not part
        of the repository.
Output: data/basilici-bigliazzi-2025-db.json

Their fields, kept as they define them (see the site's "Informazioni scheda"): `data_incoronazione`
and `data_decreto` as printed (d-m-y, `#` = unknown); `autorizza` = Capitolo / Capitolo assenso /
Conte Sforza / B.P (papal brief) / the Pope's name; `data_verificata` = whether they found evidence
that the crowning was by Sforza, the Chapter, a brief or the Pope; `incoronazione` = 1 (first),
2 (second) or # (uncertain, or refused by the Chapter). NOT read at first hand and, by their own
account, compiled from Anselmo da Reno Centese's 1933 catalogue, the printed repertories and the
internet, with the archive consulted for particular cases; so this is a SECONDARY layer. The schede they
mark as verified crownings go into the catalogue through build_lit.py as series LIT, confidence low; the
report on what they add is docs/BASILICI-BIGLIAZZI.md.
"""
import json,re,sys,pathlib,html,datetime
REPO=pathlib.Path(__file__).resolve().parent.parent
SRC=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else None
if SRC is None or not (SRC/'rows.json').exists():
    sys.exit('usage: build_basilici_db.py <dir with rows.json and schede/*.html>')
rows=json.load(open(SRC/'rows.json',encoding='utf-8'))
def field(t,label):
    m=re.search(r'<u>'+re.escape(label)+r'</u>\s*<[^>]+>\s*(.*?)\s*</(?:b|i|span)>',t,re.S)
    return html.unescape(re.sub(r'\s+',' ',m.group(1))).strip() if m else None
def iso(d):
    """'28-10-1715' -> '1715-10-28'; '#-#-1740' -> '1740'; '#-#-#' -> None."""
    if not d: return None
    p=d.split('-')
    if len(p)!=3 or not p[2].isdigit(): return None
    y,mo,da=p[2],p[1],p[0]
    if mo.isdigit() and da.isdigit(): return f"{int(y):04d}-{int(mo):02d}-{int(da):02d}"
    if mo.isdigit(): return f"{int(y):04d}-{int(mo):02d}"
    return f"{int(y):04d}"
out=[];missing=[]
for r in sorted(rows,key=lambda x:x['row']):
    f=SRC/'schede'/f"{r['row']}.html"
    if not f.exists(): missing.append(r['row']); continue
    t=f.read_text(encoding='utf-8')
    if not t.strip():
        # the API returns nothing for row 0 (the Madonna della Febbre, 1631): fall back to the date index
        out.append({'row':r['row'],'id':r['id'],'continent':'Europa' if r['loc'] else None,'nation':'Città del Vaticano' if r['loc']=='Città del Vaticano' else None,'region':None,'province':None,
          'localita':r['loc'],'luogo_di_culto':None,'titolo':r['nome'],'altro_titolo':None,'diocesi':None,
          'esiste_chiesa':None,'esiste_madonna':None,'posto_originale':None,'incoronazione':None,'tipo_manufatto':None,
          'data_incoronazione':f"{r['d']}-{r['m']}-{r['y']}",'data_verificata':None,'incoronata':None,'data_decreto':None,
          'autorizza':None,'officia':None,'annotazioni':'scheda not returned by the site API; fields from the date index only',
          'note':None,'coronation_date':iso(f"{r['d']}-{r['m']}-{r['y']}"),'decree_date':None})
        continue
    hdr=re.search(r'<span>\s*\((\d+)\)\s*-\s*(.*?)\s*</span>',t,re.S)
    geo=[html.unescape(x.strip()) for x in re.sub(r'\s+',' ',hdr.group(2)).split(' - ')] if hdr else []
    geo=[g for g in geo if g]
    rec={'row':r['row'],'id':int(hdr.group(1)) if hdr else r['id'],
         'continent':geo[0] if geo else None,'nation':geo[1] if len(geo)>1 else None,
         'region':geo[2] if len(geo)>2 else None,'province':geo[3] if len(geo)>3 else None,
         'localita':field(t,'Località:'),'luogo_di_culto':field(t,'Luogo di culto:'),
         'titolo':field(t,'Titolo:'),'altro_titolo':field(t,'Altro titolo:'),'diocesi':field(t,'Diocesi:'),
         'esiste_chiesa':field(t,'Esiste la chiesa?'),'esiste_madonna':field(t,'Esiste la Madonna?'),
         'posto_originale':field(t,'Nel posto originale?'),'incoronazione':field(t,'Incoronazione:'),
         'tipo_manufatto':field(t,'Tipo manufatto:'),
         'data_incoronazione':field(t,'Data incoronazione:'),'data_verificata':field(t,'Data verifica:'),
         'incoronata':field(t,"Incoronata/o:"),'data_decreto':field(t,'Data del decreto:'),
         'autorizza':field(t,'Autorizza:'),'officia':field(t,"Officia l'incoronazione:"),
         'annotazioni':field(t,'Annotazioni:'),'note':field(t,'Note:')}
    for k in ('altro_titolo','annotazioni','note','officia','diocesi','luogo_di_culto'):
        if rec[k] in ('#','=='): rec[k]=None
    rec['coronation_date']=iso(rec['data_incoronazione']); rec['decree_date']=iso(rec['data_decreto'])
    out.append(rec)
doc={'source':("Massimo Basilici and Rita Bigliazzi, Le Madonne Coronate (anni 1631-1750; 1751-1900; 1901-1931; "
  "1932-1981), 2025 — companion database 'Le Madonne Coronate, a cura di Massimo Basilici e Rita Bigliazzi, anni "
  "1631-1981', https://www.pereto.org/madonne_coronate/ , one scheda per crowning."),
 'fetched':datetime.date.today().isoformat(),
 'note':("SECONDARY and not read at first hand: the authors' own conclusions, compiled (their introduction, 'La ricerca') "
  "from Anselmo da Reno Centese 1933, the printed repertories (Bombelli, Mazzolari, Briccolani, Mansi, Bonci), the "
  "internet and correspondence, with the archive consulted for particular cases; the `autorizza` field is taken "
  "'principalmente dalla pubblicazione di frate Anselmo'. Fields are theirs; `coronation_date` and `decree_date` are "
  "ISO renderings of `data_incoronazione` and `data_decreto`. The schede marked 'data_verificata: sì' with "
  "'incoronazione' 1, 2 or 3 enter the catalogue as LIT records (scripts/build_lit.py); see docs/BASILICI-BIGLIAZZI.md."),
 'row_count':len(out),'missing_rows':missing,'rows':out}
json.dump(doc,open(REPO/'data/basilici-bigliazzi-2025-db.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
import collections
print('rows',len(out),'missing',len(missing))
print('autorizza',collections.Counter(r['autorizza'] for r in out).most_common(12))
print('verificata',collections.Counter(r['data_verificata'] for r in out))
print('incoronazione',collections.Counter(r['incoronazione'] for r in out))
print('nations',collections.Counter(r['nation'] for r in out).most_common(15))
