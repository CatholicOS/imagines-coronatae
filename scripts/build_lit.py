"""Secondary-literature layer: coronations reported by scholarly works that cite the Chapter archive.

Inputs : data/vrabelova-2013-table-xxi.json, data/balzamo-2023-crownings.json
Output : data/attestations-lit.json   (act-level records, series "LIT")

These records are NOT read at first hand. Each carries the work and locus as its citation and the
author's own archival references (BAV, ACSP, Madonne coronate, volume, folio) in `register_refs`,
so that any row can be taken back to the primary dossier. Confidence is capped at "medium", and is
"low" where the author gives no folio.
"""
import json,pathlib,datetime,re
REPO=pathlib.Path(__file__).resolve().parent.parent
recs=[]
def year(d):
    m=re.match(r'(\d{4})',str(d or '')); return int(m.group(1)) if m else None

# --- Vrabelová 2013, § XXI ---
V=json.load(open(REPO/'data/vrabelova-2013-table-xxi.json',encoding='utf-8'))
for r in V['rows']:
    refs=[f"BAV, ACSP, Madonne coronate, {x}" for x in r['refs']]
    recs.append({'series':'LIT','volume':0,'year':year(r['date']),'page':r['no'],'folio':None,'folio_to':None,
      'citation':f"Vrabelová 2013, § XXI no. {r['no']} (§ {r['section']})",'source_pdf_url':None,'act_number':str(r['no']),
      'act_type':'Coronation reported by secondary literature, citing the Chapter dossier','pope':None,
      'evidence_type':'chapter_decree','act_date':None,'concession_date':None,'coronation_date':r['date'],
      'legate':None,'deputy':None,'register_refs':refs,'documents':['secondary literature'],
      'rubric_latin':r['title_as_given'],'incipit_latin':None,
      'image_title_vernacular':r['title_vernacular'],'image_title_latin':None,'image_subject':r['subject'],
      'church_or_sanctuary':None,'locality':r['locality'],'diocese_latin':None,'diocese_modern':None,'country':r['country'],
      'confidence':'medium' if refs else 'low',
      'notes':('Reported by Vrabelová 2013, not read at first hand. '+(r['notes'] or '')).strip()})

# --- Balzamo 2023 ---
B=json.load(open(REPO/'data/balzamo-2023-crownings.json',encoding='utf-8'))
for r in B['rows']:
    refs=[f"BAV, ACSP, Madonne coronate, {x}" for x in r['refs']]
    recs.append({'series':'LIT','volume':0,'year':year(r.get('date')) or year(r.get('concession_date')),'page':100+r['no'],
      'folio':None,'folio_to':None,
      'citation':f"Balzamo 2023, p. {r['page']}",'source_pdf_url':None,'act_number':f"B{r['no']}",
      'act_type':'Coronation reported by secondary literature'+(', citing the Chapter dossier' if refs else ''),'pope':None,
      'evidence_type':r['evidence'],'act_date':None,'concession_date':r.get('concession_date'),'coronation_date':r.get('date'),
      'legate':r.get('deputy'),'deputy':r.get('deputy'),'register_refs':refs,'documents':['secondary literature'],
      'rubric_latin':None,'incipit_latin':None,
      'image_title_vernacular':r['title_vernacular'],'image_title_latin':None,'image_subject':r['subject'],
      'church_or_sanctuary':None,'locality':r['locality'],'diocese_latin':None,'diocese_modern':None,'country':r['country'],
      'confidence':'medium' if refs else 'low','standalone':bool(r.get('standalone')),
      'notes':('Reported by Balzamo 2023, not read at first hand. '+(r['notes'] or '')).strip()})

out={'metadata':{'layer':'attestations-lit — coronations reported by secondary literature, each with the author’s own citation of the Chapter archive where given',
  'sources':[V['source'],B['source']],'generated':datetime.date.today().isoformat(),'record_count':len(recs),
  'caveats':['Secondary evidence: none of these records was read at first hand; confidence is capped at medium.',
             'Where the author cites no folio, confidence is low and the record says so.']},
  'records':recs}
json.dump(out,open(REPO/'data/attestations-lit.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('wrote data/attestations-lit.json',len(recs),'records')
