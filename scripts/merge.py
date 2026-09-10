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

# dedupe: keep the richest record per key
groups=collections.OrderedDict()
for r in recs: groups.setdefault(key(r),[]).append(r)
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
