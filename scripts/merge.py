import json,glob,os,re,collections,unicodedata as _u

FIELDS=['series','volume','year','page','act_number','act_type','pope','citation','source_pdf_url',
 'evidence_type','rubric_latin','incipit_latin','image_title_latin','image_title_vernacular',
 'image_subject','church_or_sanctuary','locality','diocese_latin','diocese_modern','country',
 'act_date','coronation_date','legate','confidence','notes']
EVID={'papal_coronation_act','papal_legate_deputation','papal_personal_coronation',
      'retrospective_attestation','norms'}

url={}
for tsv,ser in (('urls.tsv','AAS'),('ass_urls.tsv','ASS')):
    if os.path.exists(tsv):
        for line in open(tsv):
            u,n=line.rstrip('\n').split('\t'); url[(ser,n[:-4])]=u

def norm(r,series):
    o={}
    o['series']=r.get('series') or series
    o['volume']=r.get('volume',r.get('aas_volume'))
    o['year']  =r.get('year',  r.get('aas_year'))
    o['page']  =r.get('page',  r.get('aas_page'))
    for k in FIELDS:
        if k in ('series','volume','year','page','citation','source_pdf_url'): continue
        o[k]=r.get(k)
    o['_sid']=r.get('source_id') or ''
    return o

recs=[];prob=[]
for d,ser in (('out','AAS'),('out_ass','ASS'),('out_gap',None)):
    for f in sorted(glob.glob(f'{d}/*.json')):
        b=os.path.basename(f)[:-5]
        try: data=json.load(open(f,encoding='utf-8'))
        except Exception as e: prob.append((b,f'unparseable: {e}')); continue
        if not isinstance(data,list): prob.append((b,'not a list')); continue
        for r in data:
            if not isinstance(r,dict): continue
            o=norm(r,ser or ('ASS' if str(r.get('series','')).upper()=='ASS' else 'AAS')); o['_batch']=b
            if o['evidence_type'] not in EVID: prob.append((b,f"bad evidence_type {o.get('evidence_type')!r}"))
            recs.append(o)

_SPECIAL=str.maketrans({'ł':'l','Ł':'l','ø':'o','Ø':'o','đ':'d','Đ':'d','æ':'ae','Æ':'ae','œ':'oe','Œ':'oe','ß':'ss','þ':'th'})
def _toks(s):
    if not s: return set()
    s=str(s).translate(_SPECIAL)
    s=_u.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return {t for t in re.split(r'[^a-z0-9]+',s) if len(t)>2}
def _near(A,B,n=5):
    if A & B: return True
    return bool({t[:n] for t in A if len(t)>=n} & {t[:n] for t in B if len(t)>=n})
GENERIC={'imago','beatae','mariae','virginis','sanctae','simulacrum','matka','boza','nuestra',
 'senora','madonna','domina','nostra','dominae','sacra','beata','virgo','maria','notre','dame','della','delle'}
def compatible(a,b):
    aa,ab=a.get('act_number'),b.get('act_number')
    if aa and ab and aa!=ab: return False
    la,lb=_toks(a.get('locality')),_toks(b.get('locality'))
    if la and lb: return _near(la,lb)
    ta=(_toks(a.get('image_title_vernacular'))|_toks(a.get('image_title_latin'))|_toks(a.get('church_or_sanctuary')))-GENERIC
    tb=(_toks(b.get('image_title_vernacular'))|_toks(b.get('image_title_latin'))|_toks(b.get('church_or_sanctuary')))-GENERIC
    if not ta or not tb: return True
    return _near(ta,tb)

def richness(r): return sum(1 for k in FIELDS if r.get(k) not in (None,'',[]))
bypage=collections.OrderedDict()
for r in recs: bypage.setdefault((r['series'],r.get('volume'),r.get('page')),[]).append(r)
final=[]
for pk,rs in bypage.items():
    clusters=[]
    for r in rs:
        for c in clusters:
            if compatible(c[0],r): c.append(r); break
        else: clusters.append([r])
    for g in clusters:
        g=sorted(g,key=richness,reverse=True)
        best=dict(g[0])
        for o in g[1:]:
            for f in FIELDS:
                if best.get(f) in (None,'') and o.get(f) not in (None,''): best[f]=o[f]
        best['_dupes']=len(g)
        final.append(best)

for r in final:
    s,v,y,p=r['series'],r.get('volume'),r.get('year'),r.get('page')
    r['citation']=f"{s} {v} ({y}), p. {p}" if v and y and p else None
    r['source_pdf_url']=url.get((s,r.pop('_sid','').split('#')[0]))
    r.pop('_batch',None)
order={'ASS':0,'AAS':1}
final.sort(key=lambda r:(order.get(r['series'],9),r.get('year') or 0,r.get('volume') or 0,r.get('page') or 0))
json.dump(final,open('merged_all.json','w'),ensure_ascii=False,indent=1)
print('raw:',len(recs),'| final:',len(final))
print('by series:',collections.Counter(r['series'] for r in final))
print('evidence :',collections.Counter(r['evidence_type'] for r in final).most_common())
print('countries:',len({r['country'] for r in final if r.get('country')}))
if prob:
    print('PROBLEMS:'); [print('  ',*p) for p in prob[:10]]
