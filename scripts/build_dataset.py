import json,os,re,datetime,collections
import pathlib
REPO=str(pathlib.Path(__file__).resolve().parent.parent)
FIELDS=['series','volume','year','page','act_number','act_type','pope','citation','source_pdf_url',
 'evidence_type','rubric_latin','incipit_latin','image_title_latin','image_title_vernacular',
 'image_subject','church_or_sanctuary','locality','diocese_latin','diocese_modern','country',
 'act_date','coronation_date','legate','confidence','notes']
recs=[]
for r in json.load(open('merged_all.json')):
    o={k:r.get(k) for k in FIELDS}
    for k,v in list(o.items()):
        if isinstance(v,str):
            v=re.sub(r'\s+',' ',v).strip(); o[k]=v or None
    recs.append(o)
# consolidate multi-page `norms` documents
g={}
for r in [y for y in recs if y['evidence_type']=='norms']: g.setdefault((r['series'],r['volume'],r['year']),[]).append(r)
for k,grp in g.items():
    if len(grp)<2: continue
    grp.sort(key=lambda r:r.get('page') or 0)
    pg=[r['page'] for r in grp if r.get('page')]
    grp[0]['notes']=((grp[0].get('notes') or '')+f" Document spans pp. {min(pg)}-{max(pg)}+.").strip()
    for r in grp[1:]: recs.remove(r)
order={'ASS':0,'AAS':1}
recs.sort(key=lambda r:(order.get(r['series'],9),r.get('year') or 0,r.get('volume') or 0,r.get('page') or 0,
                        (r.get('image_title_vernacular') or r.get('image_title_latin') or '')))
st={
 'by_series':dict(collections.Counter(r['series'] for r in recs)),
 'by_evidence_type':dict(collections.Counter(r['evidence_type'] for r in recs)),
 'by_confidence':dict(collections.Counter(r['confidence'] for r in recs)),
 'by_country':dict(collections.Counter(r['country'] for r in recs if r['country']).most_common()),
 'by_pope':dict(collections.Counter(r['pope'] for r in recs if r['pope']).most_common()),
 'by_decade':dict(sorted(collections.Counter(((r['year'] or 0)//10)*10 for r in recs).items())),
}
doc={'metadata':{
 'title':'Imagines Coronatae — crowned sacred images attested in the official acts of the Holy See',
 'source':'Acta Sanctae Sedis (1865-1908) and Acta Apostolicae Sedis (1909- ), Libreria Editrice Vaticana',
 'source_index_urls':{'ASS':'https://www.vatican.va/archive/ass/index_it.htm',
                      'AAS':'https://www.vatican.va/archive/aas/index_sp.htm'},
 'generated':datetime.date.today().isoformat(),
 'record_count':len(recs),
 'layer':'attestations — one record per ACT that attests a crowning; see imagines-coronatae.json for one record per IMAGE',
 'coverage':{'series':[
    {'series':'ASS','volumes':41,'files':41,'years':'1865-1908','pages_searched':30021},
    {'series':'AAS','volumes':101,'files':399,'years':'1909-2026','pages_searched':117555}],
   'pages_searched':147576},
 'method':('Every ASS and AAS volume PDF published on vatican.va was downloaded and verified against its '
   'Content-Length, its text layer extracted, de-hyphenated across line breaks, and swept for the Latin and '
   'vernacular vocabulary of image-coronation. Candidate passages were read and structured by parallel '
   'extraction agents against a fixed specification, then merged and de-duplicated by locality.'),
 'evidence_types':{
   'papal_coronation_act':'The act itself grants or permits the coronation.',
   'papal_legate_deputation':'The Pope deputes a Legate to crown the image in his name.',
   'papal_personal_coronation':'The act records that the Pope crowned the image himself.',
   'retrospective_attestation':'Another act (e.g. a Basilica Minor elevation) states in passing that the image was crowned.',
   'norms':'General legislation on the crowning of images.'},
 'caveats':[
   'NOT A GLOBAL CENSUS. For most of the period covered, the crowning of an image was decreed by the Chapter '
   'of St Peter’s Basilica (Capitulum Vaticanum) and was never published in either gazette. This dataset '
   'documents what ASS and AAS attest — a well-defined and citable subset.',
   'The archives of the Chapter of St Peter’s Basilica are a separate source and only fractionally '
   'online. The dedicated series is “Madonne coronate” (cited BAV, ACSP, Madonne coronate, tomo I, '
   'foglio N (mecc. N)); one volume is digitized in full, Arch.Cap.S.Pietro.Madonne.coron.4 (726 images, '
   'not OCR’d), and ten folios of vol. 19. Everything else must be consulted at the Vatican Library or '
   'the Archivio Capitolare, or reached through the registers and catalogues that cite it. '
   'See docs/CHAPTER-ARCHIVES.md.',
   'The 25 March 1973 Normae (AAS 65, 276) reshaped the practice; from 1974 the acts appear as Litterae '
   'Apostolicae granting the faculty to crown, and they are numerous.',
   'Sources are OCR scans and ASS is markedly rougher than AAS. Place names are frequently mangled. Every '
   'record keeps the verbatim Latin rubric and incipit and carries a confidence value; records marked "low", '
   'or carrying a note, should be checked against the printed page before being treated as authoritative.',
   'Several ASS volumes span two calendar years; `year` is the first year of the volume.'],
 'statistics':st,
 'license':'Underlying ASS and AAS texts are © Libreria Editrice Vaticana. This compilation is provided for research use.'},
 'records':recs}
os.makedirs(os.path.join(REPO,'data'),exist_ok=True)
out=os.path.join(REPO,'data','attestations.json')
json.dump(doc,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
import csv
with open(os.path.join(REPO,'data','attestations.csv'),'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=FIELDS,extrasaction='ignore'); w.writeheader()
    for r in recs: w.writerow(r)
print('wrote',out,len(recs),'records')
for k,v in st.items():
    if k!='by_country': print(' ',k,':',v)
print('  countries:',len(st['by_country']))
