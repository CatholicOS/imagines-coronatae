"""Secondary-literature layer: coronations reported by scholarly works that cite the Chapter archive.

Inputs : data/vrabelova-2013-table-xxi.json, data/balzamo-2023-crownings.json,
         data/zander-magister-2011-catalogue.json, data/briccolani-1800-serie.json,
         data/bombelli-1792-raccolta.json
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

# --- Zander / Magister 2011 (exhibition catalogue; one row per painted copy, with the dossier cited) ---
Z=json.load(open(REPO/'data/zander-magister-2011-catalogue.json',encoding='utf-8'))
for i,r in enumerate(Z['rows']):
    refs=[f"BAV, ACSP, Madonne coronate, {x}" for x in r['refs']]
    afsp=[f"AFSP, Arm. 12, F, 11, nr. 10, catalogo delle immagini, {x}" for x in r['afsp_refs']]
    notes='Reported by Zander/Magister 2011, not read at first hand. '+(r['notes'] or '')
    if len(r['coronation_dates'])>1:
        notes+=f" The catalogue gives more than one crowning: {', '.join(r['coronation_dates'])}."
    recs.append({'series':'LIT','volume':0,'year':year(r['coronation_dates'][0]),'page':200+i,'folio':None,'folio_to':None,
      'citation':f"Zander/Magister 2011, cat. {r['no']}, p. {r['page']}",'source_pdf_url':None,'act_number':f"Z{r['no']}",
      'act_type':'Coronation reported by secondary literature'+(', citing the Chapter dossier' if refs else ''),'pope':None,
      'evidence_type':'chapter_decree','act_date':None,'concession_date':None,'coronation_date':r['coronation_dates'][0],
      'legate':None,'deputy':None,'register_refs':refs+afsp,'documents':['secondary literature'],
      'rubric_latin':None,'incipit_latin':None,
      'image_title_vernacular':r['title'],'image_title_latin':None,'image_subject':r['subject'],
      'church_or_sanctuary':r['church_or_sanctuary'],'locality':r['locality'],'diocese_latin':None,'diocese_modern':None,
      'country':r['country'],'confidence':'medium' if refs else 'low','notes':notes.strip()})
    # a re-crowning the catalogue reports is a second act on the same image
    for d in r['coronation_dates'][1:]:
        recs.append({**recs[-1],'year':year(d),'coronation_date':d,'act_number':f"Z{r['no']}b",
          'notes':f"Re-crowning reported by Zander/Magister 2011 (cat. {r['no']}): crowned again {d}."})

# --- Briccolani 1800 (the earliest printed register: year by year, 1631-1793, no folio) ---
Bc=json.load(open(REPO/'data/briccolani-1800-serie.json',encoding='utf-8'))
for r in Bc['rows']:
    child=r['kind']=='child'
    guad=r['country']=='Mexico'
    notes='Reported by Briccolani 1800 (printed register, year only, no archival reference), not read at first hand. '
    if child: notes+='Crown for the Child (Bambino Gesù) of an image already crowned, listed as a separate concession. '
    notes+=(r['notes'] or '')
    recs.append({'series':'LIT','volume':0,'year':r['year'],'page':400+r['no'],'folio':None,'folio_to':None,
      'citation':f"Briccolani 1800, p. {r['page']}",'source_pdf_url':'https://archive.org/details/gri_33125011212400',
      'act_number':f"Br{r['no']}",'act_type':'Coronation listed in a printed register','pope':None,
      'evidence_type':'chapter_decree','act_date':None,
      'concession_date':str(r['year']) if guad else None,'coronation_date':None if guad else str(r['year']),
      'legate':None,'deputy':None,'register_refs':[],'documents':['printed register'],
      'rubric_latin':None,'incipit_latin':r['text_as_printed'],
      'image_title_vernacular':r['title'],'image_title_latin':None,
      'image_subject':'Blessed Virgin Mary with Child' if child else 'Blessed Virgin Mary',
      'church_or_sanctuary':r['church_or_place'],'locality':r['locality'],'diocese_latin':None,'diocese_modern':None,
      'country':r['country'],'confidence':'low','notes':notes.strip(),
      'parent_act':f"Br{r['parent_no']}" if r.get('parent_no') else None})

# --- Bombelli 1792 (the illustrated Raccolta: one notice per Roman image, with the day of the crowning, no folio) ---
Bo=json.load(open(REPO/'data/bombelli-1792-raccolta.json',encoding='utf-8'))
for r in Bo['rows']:
    notes=("Reported by Bombelli 1792 (notice with the day of the crowning, drawn from the Chapter's memorie and atti but "
           "citing no folio), not read at first hand. ")
    plate=[]
    if r['medium']: plate.append(f"in {r['medium']}")
    if r['size_palmi']: plate.append(f"pal. {r['size_palmi']}")
    if r['caption_year']: plate.append(f"crowned {r['caption_year']}")
    if plate: notes+=f"The plate's caption: {', '.join(plate)}. "
    if r['crown_cost_scudi']: notes+=f"Crown cost sc. {r['crown_cost_scudi']}. "
    if r['deputies']: notes+=f"Deputed: {r['deputies']}. "
    notes+=(r['notes'] or '')
    recs.append({'series':'LIT','volume':0,'year':r['year'],'page':500+r['no'],'folio':None,'folio_to':None,
      'citation':f"Bombelli 1792, tomo {r['tomo']}, p. {r['page']}",'source_pdf_url':Bo['scan'][r['tomo']],
      'act_number':f"Bo{r['no']}",'act_type':'Coronation reported in a printed collection of notices','pope':None,
      'evidence_type':'chapter_decree','act_date':None,'concession_date':r['concession_date'],'coronation_date':r['coronation_date'],
      'legate':None,'deputy':r['deputies'],'register_refs':[],'documents':['printed notice'],
      'rubric_latin':r['heading_as_printed'],'incipit_latin':r['text_as_printed'],
      'image_title_vernacular':r['title'],'image_title_latin':None,'image_subject':'Blessed Virgin Mary',
      'church_or_sanctuary':r['church_or_place'],'locality':r['locality'],'diocese_latin':None,'diocese_modern':None,
      'country':'Italy','confidence':'low','notes':notes.strip(),'parent_act':None})
    # a separate crown for the Child is a second act on the same image, linked by parent_act
    if r['child_date']:
        recs.append({**recs[-1],'year':year(r['child_date']),'coronation_date':r['child_date'],'concession_date':None,
          'act_number':f"Bo{r['no']}c",'image_subject':'Blessed Virgin Mary with Child','parent_act':f"Bo{r['no']}",
          'notes':f"Crown for the Child (Bambino Gesù) of the image crowned {r['coronation_date']}, reported by Bombelli 1792 (tomo {r['tomo']}, p. {r['page']})."})

out={'metadata':{'layer':'attestations-lit — coronations reported by secondary literature, each with the author’s own citation of the Chapter archive where given',
  'sources':[V['source'],B['source'],Z['source'],Bc['source'],Bo['source']],'generated':datetime.date.today().isoformat(),'record_count':len(recs),
  'caveats':['Secondary evidence: none of these records was read at first hand; confidence is capped at medium.',
             'Where the author cites no folio, confidence is low and the record says so.']},
  'records':recs}
json.dump(out,open(REPO/'data/attestations-lit.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('wrote data/attestations-lit.json',len(recs),'records')
