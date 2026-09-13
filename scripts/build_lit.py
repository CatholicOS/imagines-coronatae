"""Secondary-literature layer: coronations reported by a scholarly work that cites the Chapter archive.

Input : data/vrabelova-2013-table-xxi.json
Output: data/attestations-lit.json   (act-level records, series "LIT")

These records are NOT read at first hand. Each carries the work and section as its citation and the
author's own archival references (BAV, ACSP, Madonne coronate, sv. N, fol. X) in `register_refs`,
so that any row can be taken back to the primary dossier. Confidence is capped at "medium".
"""
import json,pathlib,datetime,re
REPO=pathlib.Path(__file__).resolve().parent.parent
V=json.load(open(REPO/'data/vrabelova-2013-table-xxi.json',encoding='utf-8'))
WORK='Vrabelová 2013'
recs=[]
for r in V['rows']:
    refs=[f"BAV, ACSP, Madonne coronate, {x}" for x in r['refs']]
    recs.append({
      'series':'LIT','volume':0,'year':int(r['date'][:4]),'page':r['no'],'folio':None,'folio_to':None,
      'citation':f"{WORK}, § XXI no. {r['no']} (§ {r['section']})",
      'source_pdf_url':None,'act_number':str(r['no']),
      'act_type':'Coronation reported by secondary literature, citing the Chapter dossier',
      'pope':None,'evidence_type':'chapter_decree',
      'act_date':None,'concession_date':None,'coronation_date':r['date'],
      'legate':None,'deputy':None,'register_refs':refs,'documents':['secondary literature'],
      'rubric_latin':r['title_as_given'],'incipit_latin':None,
      'image_title_vernacular':r['title_vernacular'],'image_title_latin':None,
      'image_subject':r['subject'],'church_or_sanctuary':None,
      'locality':r['locality'],'diocese_latin':None,'diocese_modern':None,'country':r['country'],
      'confidence':'medium' if refs else 'low',
      'notes':('Reported by '+WORK+', not read at first hand. '+(r['notes'] or '')).strip(),
    })
out={'metadata':{'layer':'attestations-lit — coronations reported by secondary literature, each with the author’s own citation of the Chapter archive',
  'source':V['source'],'generated':datetime.date.today().isoformat(),'record_count':len(recs),
  'caveats':['Secondary evidence: none of these records was read at first hand; confidence is capped at medium.',
             'Where the author cites no folio for an image, confidence is low and the record says so.']},
  'records':recs}
json.dump(out,open(REPO/'data/attestations-lit.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('wrote data/attestations-lit.json',len(recs),'records')
