"""Align the Roman schede of Basilici-Bigliazzi with the catalogue's church strings.

Rome is matched by church, and Basilici-Bigliazzi describe a church at length ("Basilica di Santa
Maria in Trastevere nella Cappella Altemps", "Oratorio del Santissimo Sacramento in Laterano" for
the Scala Santa, "Tempio di Ercole Vincitore" for Santa Maria del Sole), so their Roman rows would
not reach the images Briccolani and Bombelli already put there. This script writes a frozen table,
data/basilici-rome-alignment.json, giving for each verified Roman scheda the catalogue's own
locality string, and — for the twelve schede that are in fact the separate crown for the Child of
an image crowned earlier (Briccolani's twelve Bambino Gesù concessions, which they file as first
crownings) — the row of the parent scheda.

The table was built on 14 September 2026 against the catalogue as it stood before the ingest
(commit d347b3a): for each Roman scheda the Roman images sharing a church word or a title word
within two years of its date were listed; where exactly one shared a church word it was taken
(AUTO), the rest were decided by eye (PICK, the dict below). Rows absent from the table keep
their own church string: images the catalogue did not yet have (the Divino Amore, the Madonna
dell'Archetto, the Perpetuo Soccorso ...). Re-run only to regenerate after checking the PICKs.
"""
import json,pathlib,sys
REPO=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(REPO/'scripts'))
BASE=sys.argv[1] if len(sys.argv)>1 else str(REPO/'data/imagines-coronatae.json')   # a catalogue WITHOUT the BB layer
src=open(REPO/'scripts/build_images.py',encoding='utf-8').read()
head=src.split('for c,rs in bycountry.items():')[0].replace('pathlib.Path(__file__).resolve().parent.parent','pathlib.Path(%r).parent.parent'%str(REPO/'scripts/x'))
_ns={}; exec(head,_ns)
toks,loc_toks,title_full,ROME_NOISE,ECCL_STOP=(_ns[k] for k in ('toks','loc_toks','title_full','ROME_NOISE','ECCL_STOP'))

PICK={ # row: (catalogue locality, parent row for a Child's crown)
 10:("Rome, Vatican Basilica (Pietà)",None), 18:("Rome, Vatican Basilica (sacristy)",0),
 24:("Rome, San Cosimato in Trastevere",17), 25:("Rome, Vatican Basilica (Madonna della Colonna)",None),
 26:("Rome, Sant'Alessio",None), 27:("Rome, Vatican Basilica (Madonna della Colonna)",25),
 28:("Rome, Santa Marta al Collegio Romano",None), 32:("Rome, Santa Marta al Collegio Romano",28),
 34:("Rome, San Salvatore in Lauro",23), 35:("Rome, San Giovanni in Fonte (Lateran baptistery)",None),
 36:("Rome, Santa Maria delle Grazie al Foro Romano",None), 38:("Rome, Vatican Basilica (Cappella Gregoriana)",21),
 40:("Rome, San Giovanni dei Fiorentini",None), 44:("Rome, San Giovannino in Campo Marzio (Mercedarians)",None),
 45:("Rome, Santa Maria in Portico in Campitelli",None), 48:("Rome, Oratorio di Campitelli",None), 46:("Rome, Santa Maria di Costantinopoli a Capo le Case",None),
 50:("Rome, Santa Maria del Pianto",20), 51:("Rome, Santa Maria della Purità in Borgo",31),
 52:("Rome, Santa Maria in Traspontina",16), 53:("Rome, Sant'Anna dei Falegnami",None),
 56:("Rome, Santa Maria in Posterula",None), 57:("Rome, Santa Maria Liberatrice",None),
 61:("Rome, Santa Maria sopra Minerva",13), 64:("Rome, Santa Maria in Campo Marzio (nuns)",None),
 65:("Rome, Santa Prassede",None), 67:("Rome, Santa Maria dell'Orto",None),
 72:("Rome, Santa Maria in Trastevere (Madonna della Clemenza)",None), 73:("Rome, Santa Maria di Montesanto",None),
 87:("Rome, Santa Lucia del Gonfalone",None), 88:("Rome, Santa Maria del Popolo",4),
 90:("Rome, Santa Lucia della Tinta",None), 91:("Rome, Santa Maria dei Miracoli",29),
 106:("Rome, Oratorio del Caravita",None), 108:("Rome, Sant'Adriano al Foro",None),
 111:("Rome, Santi Vincenzo e Anastasio a Trevi",None), 112:("Rome, Scala Santa",None),
 124:("Rome, Santo Spirito (nuns)",None), 126:("Rome, Tor de' Specchi (monastery)",None),
 # the nineteenth- and twentieth-century re-crownings of images already in the catalogue
 385:("Rome, San Salvatore in Lauro",None), 387:("Rome (ceremony in the Vatican Basilica)",None),
 407:("Rome, Sant'Agostino (Madonna del Parto)",None), 416:("Rome, San Lorenzo in Damaso",None),
 477:("Rome, Santa Maria Maddalena",None), 588:("Rome, Chiesa del Gesù",None),
 715:("Rome, Santa Maria in Portico in Campitelli",None), 767:("Rome, Santissimo Nome di Maria",None),
 807:("Rome, Vatican Basilica (Cappella del Coro)",None), 992:("Rome, Santa Maria in Cosmedin",None),
 1085:("Rome, Santa Maria delle Grazie a Porta Angelica",None), 1086:("Rome, Santa Maria delle Grazie a Porta Angelica",None),
 1175:("Rome, Santa Maria in Traspontina",None),
}
ims=[im for im in json.load(open(BASE,encoding='utf-8'))['images'] if (im['locality'] or '').startswith('Rome')]
assert not any(str(s.get('act_number','')).startswith('BB') for im in ims for s in im['sources']), 'base catalogue must not contain the BB layer'
rows=json.load(open(REPO/'data/basilici-bigliazzi-2025-db.json',encoding='utf-8'))['rows']
def rec(im): return {'locality':im['locality'],'image_title_vernacular':im['image_title_vernacular'],'image_title_latin':im['image_title_latin'],'church_or_sanctuary':im['church_or_sanctuary']}
def ctoks(r): return {t for t in toks(r.get('church_or_sanctuary'))|loc_toks(r) if t not in ROME_NOISE and t not in ECCL_STOP and t!='rome'}
def is_rome(s):
    return s['nation']=='Città del Vaticano' or (s['nation']=='Italia' and s['region']=='Lazio' and (s['localita'] or '').lower().startswith('roma'))
out={}
for s in rows:
    if s['row']==0: out[0]={'locality':'Rome, Vatican Basilica (sacristy)','child_of':None,'how':'PICK'}; continue
    if not (s['data_verificata']=='sì' and s['incoronazione'] in ('1','2','3') and is_rome(s)): continue
    if s['row'] in PICK:
        loc,par=PICK[s['row']]; out[s['row']]={'locality':loc,'child_of':par,'how':'PICK'}; continue
    r={'locality':'Rome, '+(s['luogo_di_culto'] or ''),'image_title_vernacular':s['titolo']+' '+(s['altro_titolo'] or ''),'church_or_sanctuary':s['luogo_di_culto']}
    y=int(s['coronation_date'][:4]); ct=ctoks(r); tt=title_full(r)
    top=[]
    for im in ims:
        ir=rec(im); ci=ctoks(ir); ti=title_full(ir)
        yrs=[int(d[:4]) for d in im['coronation_dates'] if d[:4].isdigit()]
        dy=min([abs(y-z) for z in yrs],default=99)
        if (ct&ci or tt&ti) and dy<=2: top.append((len(ct&ci),len(tt&ti),dy,im['locality']))
    top.sort(key=lambda c:(-c[0]-c[1],c[2]))
    if len(top)==1 and top[0][0]>=1: out[s['row']]={'locality':top[0][3],'child_of':None,'how':'AUTO'}
res={"note":(__doc__ or "").strip(),'rows':{str(k):v for k,v in sorted(out.items())}}
json.dump(res,open(REPO/'data/basilici-rome-alignment.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
import collections
print('aligned',len(out),collections.Counter(v['how'] for v in out.values()),'children',sum(1 for v in out.values() if v['child_of'] is not None))
