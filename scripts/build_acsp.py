"""Turn the per-image extraction from Madonne coronate tomo IV into attestation records.

Input : data/acsp-tomo4-extraction.json  (one object per crowned image, produced by reading the
        TEI transcription against docs/EXTRACTION_SPEC_ACSP.md and merging overlapping chunks)
Output: data/attestations-acsp.json        (act-level records in the same shape as attestations.json)

The image-level catalogue is then rebuilt by scripts/build_images.py, which reads both files.
"""
import json,re,pathlib,datetime
REPO=pathlib.Path(__file__).resolve().parent.parent
A=json.load(open(REPO/'data/acsp-tomo4-extraction.json',encoding='utf-8'))
VIEW='https://digi.vatlib.it/view/ARC_Arch.Cap.S.Pietro.Madonne.coron.4/{:04d}'
def yr(*ds):
    for d in ds:
        m=re.match(r'(\d{4})',str(d or ''))
        if m: return int(m.group(1))
    return None
recs=[]
for a in A:
    pb=a['pb_from']; fa,fz=a.get('folio_from'),a.get('folio_to')
    ff=f"f. {fa}" if (fa and (fa==fz or not fz)) else f"ff. {fa}–{fz}"
    recs.append({
      'series':'ACSP','volume':4,'year':yr(a.get('concession_date'),a.get('coronation_date')),
      'page':pb,'folio':fa,'folio_to':fz,
      'citation':f"BAV, ACSP, Madonne coronate, tomo IV, {ff}",
      'source_pdf_url':VIEW.format(pb+2),          # pb n = image index - 2
      'act_number':None,
      'act_type':'Chapter dossier: '+', '.join(a.get('documents') or []) if a.get('documents') else 'Chapter dossier',
      'pope':None,'evidence_type':('petition_not_conceded' if a.get('outcome')=='not conceded' else 'chapter_decree'),
      'act_date':a.get('concession_date'),'concession_date':a.get('concession_date'),
      'coronation_date':a.get('coronation_date'),'legate':a.get('deputy'),'deputy':a.get('deputy'),
      'register_refs':a.get('register_refs') or [],'documents':a.get('documents') or [],
      'rubric_latin':a.get('key_quote'),'incipit_latin':None,
      'image_title_vernacular':a.get('image_title_vernacular'),'image_title_latin':a.get('image_title_latin'),
      'image_subject':a.get('image_subject'),'church_or_sanctuary':a.get('church_or_sanctuary'),
      'locality':a.get('locality'),'diocese_latin':None,'diocese_modern':a.get('diocese'),
      'country':a.get('country'),'confidence':a.get('confidence'),
      'notes':(('Crowns: '+a['crowns']+'. ') if a.get('crowns') else '')+(('Petitioner: '+a['petitioner']+'. ') if a.get('petitioner') else '')+(a.get('notes') or '') or None,
    })
out={'metadata':{'layer':'attestations-acsp — one record per crowned image documented in BAV, Arch. Cap. S. Pietro, Madonne coronate, tomo IV (1689-1714)',
  'source':'BAV, Archivio del Capitolo di San Pietro, Madonne coronate, tomo IV; digitized at https://digi.vatlib.it/view/ARC_Arch.Cap.S.Pietro.Madonne.coron.4; transcribed (OCR) with Vulgate.ai, 13 September 2026; ff. 1r-302v',
  'generated':datetime.date.today().isoformat(),'record_count':len(recs),
  'caveats':['Machine transcription of 17th-18th c. Italian and Latin; place-names and dates carry OCR risk and each record has a confidence value.',
             'Folios 303r-v were not transcribed.','pb n (page) maps to the BAV image index as n + 2.']},
  'records':recs}
json.dump(out,open(REPO/'data/attestations-acsp.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('wrote data/attestations-acsp.json',len(recs),'records')
