import json,glob,os,re,datetime,collections,sys
sys.path.insert(0,'.')
REPO='/home/johnrdorazio/development/CatholicOS_org/imagines-coronatae'
FIELDS=['aas_volume','aas_year','aas_page','act_number','act_type','pope','aas_citation',
 'source_pdf_url','evidence_type','rubric_latin','incipit_latin','image_title_latin',
 'image_title_vernacular','image_subject','church_or_sanctuary','locality','diocese_latin',
 'diocese_modern','country','act_date','coronation_date','legate','confidence','notes']

merged=json.load(open('merged.json'))
recs=[]
for r in merged:
    o={k:r.get(k) for k in FIELDS}
    for k,v in list(o.items()):
        if isinstance(v,str):
            v=re.sub(r'\s+',' ',v).strip()
            o[k]=v or None
    recs.append(o)
# consolidate `norms` records that are the same document printed across a page span
_n=[r for r in recs if r.get('evidence_type')=='norms']
_g={}
for r in _n: _g.setdefault((r['aas_volume'],r['aas_year']),[]).append(r)
for k,g in _g.items():
    if len(g)<2: continue
    g.sort(key=lambda r:r.get('aas_page') or 0)
    keep=g[0]; pages=[r.get('aas_page') for r in g if r.get('aas_page')]
    keep['notes']=((keep.get('notes') or '')+f" Document spans pp. {min(pages)}-{max(pages)}+; section II 'De Coronatione Imaginis B. M. V.' begins at p. {max(pages)}.").strip()
    for r in g[1:]: recs.remove(r)

recs.sort(key=lambda r:((r.get('aas_year') or 0),(r.get('aas_volume') or 0),(r.get('aas_page') or 0),
                        (r.get('image_title_vernacular') or r.get('image_title_latin') or '')))
npages=sum(1 for _ in open('logs/extract.log')) # placeholder
stats={
 'by_evidence_type':dict(collections.Counter(r['evidence_type'] for r in recs)),
 'by_confidence':dict(collections.Counter(r['confidence'] for r in recs)),
 'by_country':dict(collections.Counter(r['country'] for r in recs if r['country']).most_common()),
 'by_pope':dict(collections.Counter(r['pope'] for r in recs if r['pope']).most_common()),
 'by_decade':dict(sorted(collections.Counter(((r['aas_year']or 0)//10)*10 for r in recs).items())),
}
doc={
 'metadata':{
   'title':'Imagines Coronatae — crowned sacred images attested in Acta Apostolicae Sedis',
   'source':'Acta Apostolicae Sedis (AAS), Libreria Editrice Vaticana',
   'source_index_url':'https://www.vatican.va/archive/aas/index_sp.htm',
   'generated':datetime.date.today().isoformat(),
   'record_count':len(recs),
   'coverage':{
     'volumes':101,
     'pdf_files':399,
     'years':'1909-2026',
     'pages_searched':117555
   },
   'method':'Every AAS volume PDF on vatican.va was downloaded and its text layer extracted; '
            'the full corpus was swept for Latin and vernacular coronation vocabulary; '
            'candidate passages were read and structured by parallel extraction agents '
            'against a fixed schema, then merged and de-duplicated.',
   'evidence_types':{
     'papal_coronation_act':'The act itself grants or permits the coronation.',
     'papal_legate_deputation':'The Pope deputes a Legate to crown the image in his name.',
     'papal_personal_coronation':'The act records that the Pope crowned the image himself.',
     'retrospective_attestation':'Another act (e.g. a Basilica Minor elevation) states in passing that the image was crowned.',
     'norms':'General legislation on the crowning of images.'
   },
   'caveats':[
     'AAS begins in 1909. Coronations before that date appear here only as retrospective '
     'mentions; the primary record for them is Acta Sanctae Sedis (1865-1908) and the archives '
     'of the Chapter of St Peter’s Basilica.',
     'Historically most coronations were decreed by the Chapter of the Vatican Basilica and were '
     'NOT published in AAS. This dataset therefore documents what AAS attests, which is a subset '
     'of all crowned images worldwide.',
     'The 25 March 1973 Normae (AAS 65, 276) reserved coronation to the Pope but allowed local '
     'celebration; from 1974 onward the acts appear as Litterae Apostolicae granting the faculty.',
     'Source volumes are OCR scans. Place names are frequently mangled; every record carries a '
     'confidence level, and the verbatim Latin rubric and incipit are retained so any reading can '
     'be checked against the source.',
     'Records marked confidence "low" or carrying a note should be verified against the printed page '
     'before being treated as authoritative.'
   ],
   'statistics':stats,
   'license':'Underlying AAS texts are © Libreria Editrice Vaticana. This compilation is provided for research use.'
 },
 'records':recs
}
os.makedirs(os.path.join(REPO,'data'),exist_ok=True)
out=os.path.join(REPO,'data','imagines-coronatae.json')
json.dump(doc,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

import csv
csvp=os.path.join(REPO,'data','imagines-coronatae.csv')
with open(csvp,'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=FIELDS,extrasaction='ignore')
    w.writeheader()
    for r in recs: w.writerow(r)
print('wrote',out,len(recs),'records')
print('wrote',csvp)
for k,v in stats.items():
    if k!='by_country': print(k,':',v)
print('countries:',len(stats['by_country']))
