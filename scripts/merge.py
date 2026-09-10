import json,glob,os,re,sys,unicodedata,collections

FIELDS=['source_id','aas_volume','aas_year','aas_page','act_number','act_type','pope',
 'evidence_type','rubric_latin','incipit_latin','image_title_latin','image_title_vernacular',
 'image_subject','church_or_sanctuary','locality','diocese_latin','diocese_modern','country',
 'act_date','coronation_date','legate','confidence','notes']
EVID={'papal_coronation_act','papal_legate_deputation','papal_personal_coronation',
      'retrospective_attestation','norms'}

# map source file -> AAS pdf url
url={}
for line in open('urls.tsv'):
    u,n=line.rstrip('\n').split('\t'); url[n[:-4]]=u

def key(r):
    def n(s):
        if not s: return ''
        s=unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower()
        return re.sub(r'[^a-z0-9]+','',s)
    t=n(r.get('image_title_vernacular')) or n(r.get('image_title_latin'))
    return (r.get('aas_volume'),r.get('aas_page'),t[:28],n(r.get('locality'))[:18])

recs=[];prob=[]
for f in sorted(glob.glob('out/*.json')):
    b=os.path.basename(f)[:-5]
    try: data=json.load(open(f,encoding='utf-8'))
    except Exception as e: prob.append((b,'unparseable: %s'%e)); continue
    if not isinstance(data,list): prob.append((b,'not a list')); continue
    for r in data:
        if not isinstance(r,dict): prob.append((b,'non-dict record')); continue
        r['_batch']=b
        for k in FIELDS: r.setdefault(k,None)
        if r.get('evidence_type') not in EVID: prob.append((b,'bad evidence_type %r'%r.get('evidence_type')))
        recs.append(r)

# dedupe: cluster by (volume,page), then merge compatible records within a page
import unicodedata as _u
def _n(s):
    if not s: return ''
    s=_u.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','',s)
_SPECIAL=str.maketrans({'\u0142':'l','\u0141':'l','\u00f8':'o','\u00d8':'o','\u0111':'d','\u0110':'d',
                       '\u00e6':'ae','\u00c6':'ae','\u0153':'oe','\u0152':'oe','\u00df':'ss','\u00fe':'th'})
def _toks(s):
    if not s: return set()
    s=str(s).translate(_SPECIAL)
    s=_u.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return {t for t in re.split(r'[^a-z0-9]+',s) if len(t)>2}
def _near(A,B,n=5):
    """token sets match if they intersect or any pair shares an n-char prefix
    (absorbs OCR and Latin/vernacular spelling drift: Sevilla/Seville)"""
    if A & B: return True
    pa={t[:n] for t in A if len(t)>=n}; pb={t[:n] for t in B if len(t)>=n}
    return bool(pa & pb)
def compatible(a,b):
    """Same (volume,page) already guaranteed. Two records describe the SAME image when
    their localities overlap; titles are unreliable because one agent may give the Latin
    of the rubric and another the vernacular."""
    aa,ab=a.get('act_number'),b.get('act_number')
    if aa and ab and aa!=ab: return False
    la,lb=_toks(a.get('locality')),_toks(b.get('locality'))
    if la and lb: return _near(la,lb)
    # no locality on one side: fall back to title / sanctuary overlap
    ta=_toks(a.get('image_title_vernacular'))|_toks(a.get('image_title_latin'))|_toks(a.get('church_or_sanctuary'))
    tb=_toks(b.get('image_title_vernacular'))|_toks(b.get('image_title_latin'))|_toks(b.get('church_or_sanctuary'))
    if not ta or not tb: return True
    generic={'imago','beatae','mariae','virginis','sanctae','simulacrum','matka','boza','nuestra','senora','madonna','domina','nostra','dominae','sacra','beata','virgo','maria'}
    return _near(ta-generic,tb-generic)

bypage=collections.OrderedDict()
for r in recs: bypage.setdefault((r.get('aas_volume'),r.get('aas_page')),[]).append(r)
groups=collections.OrderedDict()
gi=0
for pk,rs in bypage.items():
    clusters=[]
    for r in rs:
        for c in clusters:
            if compatible(c[0],r): c.append(r); break
        else: clusters.append([r])
    for c in clusters:
        groups[(pk,gi)]=c; gi+=1
def richness(r): return sum(1 for k in FIELDS if r.get(k) not in (None,'',[]))
final=[]
for k,g in groups.items():
    g=sorted(g,key=richness,reverse=True)
    best=dict(g[0])
    for other in g[1:]:
        for fld in FIELDS:
            if best.get(fld) in (None,'') and other.get(fld) not in (None,''):
                best[fld]=other[fld]
    best['_duplicates']=len(g)
    best['_batches']=sorted({x['_batch'] for x in g})
    final.append(best)

for r in final:
    v,y,p=r.get('aas_volume'),r.get('aas_year'),r.get('aas_page')
    r['aas_citation']=f"AAS {v} ({y}), p. {p}" if v and y and p else None
    sid=(r.get('source_id') or '')
    fkey=sid.split('#')[0]
    r['source_pdf_url']=url.get(fkey)
    r.pop('_batch',None)

final.sort(key=lambda r:((r.get('aas_year') or 0),(r.get('aas_volume') or 0),(r.get('aas_page') or 0)))
json.dump(final,open('merged.json','w'),ensure_ascii=False,indent=1)
print('batch files:',len(glob.glob('out/*.json')),'| raw records:',len(recs),'| after dedupe:',len(final))
print('evidence_type:',collections.Counter(r.get('evidence_type') for r in final).most_common())
print('confidence  :',collections.Counter(r.get('confidence') for r in final).most_common())
print('countries   :',len({r.get('country') for r in final if r.get('country')}))
print('year range  :',min((r.get('aas_year') or 9999) for r in final),'-',max((r.get('aas_year') or 0) for r in final))
if prob:
    print('\nPROBLEMS:')
    for b,m in prob[:20]: print('  ',b,m)
