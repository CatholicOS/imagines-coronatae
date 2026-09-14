import json,re,collections,unicodedata as U,datetime,os,csv,pathlib
import pathlib
REPO=str(pathlib.Path(__file__).resolve().parent.parent)
src=json.load(open(REPO+'/data/attestations.json',encoding='utf-8'))
R=src['records'] if isinstance(src,dict) else src
for _extra in ('attestations-acsp.json','attestations-lit.json'):   # Chapter-archive and literature layers
    _p=pathlib.Path(REPO)/'data'/_extra
    if _p.exists(): R=R+json.load(open(_p,encoding='utf-8'))['records']
META=src.get('metadata',{}) if isinstance(src,dict) else {}
SPECIAL=str.maketrans({'ł':'l','Ł':'l','ø':'o','đ':'d','æ':'ae','œ':'oe','ß':'ss','þ':'th'})
STOP=set('''nuestra senora nossa senhora notre dame madonna matka boza bozej panna beata beatae maria mariae
mariam marii virgo virgen vergine virginis virgin imago imaginem imagen simulacrum simulacro effigies effigie
statua statue icon iconem sacra sacrae sacro sacrum santa sancta sanctae santo san sao our lady domina dominae
nostra nostrae della delle del dei los las sub titulo vulgo appellata appellatae invocatae dicta dictae
deipara deiparae genetricis the and que pie colitur servatur templo ecclesia templi loco urbe oppido dioecesis
archidioecesis fines intra quae cum divino puero iesu christi mater matris madre nuncupata nuncupatae
antiqua antiquum vetus vetusta miraculis clara insignis titulus
bambino gesu puero pueri iesu child figlio divin vergine santissima ssma sma miracolosa effigie vera suo sua detta
scuole schole pie padri frati monaci teatini cappuccini agostiniani domenicani francescani gesuiti serviti
sant sanct saint sankt sainte santi sancti chapel cappella capilla chapelle palazzo palace
chiesa nella nelle receipt imagines jesu roma rome esistente chiesa ordine congregazione convento
# Latin/vernacular DESCRIPTIVE adjectives. These praise an image, they do not identify it, and if
# left in they block real merges: Notre-Dame du Cap reduced to {rosario} in one act and
# {perinsigne} in another, so two records for one shrine survived side by side.
perinsigne perinsignis insigne insignem praeclara praeclarum praeclarus veneranda venerandum
venerabilis veneratio venerata miraculosa miraculoso thaumaturga thaumaturgum prodigiosa prodigioso
antiquissima antiquissimum celeberrima celeberrimum celebris augustum augusta augustae pretiosa
pretiosum sacratissima sacratissimum sanctissima sanctissimum mirabilis admirabilis egregia egregium
nobilis nobilisque pulcherrima devotissima piissima beatissima beatissimae grande grandis magna
magnum maior maxima antica antico bella bello santissima santissimo'''.split())
def norm(s): return U.normalize('NFKD',str(s or '').translate(SPECIAL)).encode('ascii','ignore').decode().lower()
def toks(*ss):
    out=set()
    for s in ss:
        for t in re.split(r'[^a-z0-9]+',norm(s)):
            if len(t)>3 and t not in STOP: out.add(t)
    return out
GEO_STOP={'near','prope','the','del','de','di','da','of','city','urbe','urbs','urbem','oppidum','oppido',
 'villa','villae','dioecesi','dioecesis','archidioecesi','san','santa','sant','sao','saint','sankt','nueva',
 'nuevo','alta','baja','los','las','and','sur','norte','provincia','region','regione','isola','island',
 # REGIONS and qualifiers: shared by unrelated shrines, so they must never establish identity.
 # ('Brittany' alone once fused Sainte-Anne d'Auray with Saint-Brieuc.)
 'brittany','bretagne','normandy','normandie','provence','sardinia','sardegna','sicily','sicilia','calabria',
 'campania','tuscany','toscana','lombardy','lombardia','piedmont','piemonte','veneto','liguria','puglia',
 'apulia','umbria','marche','lazio','abruzzo','basilicata','molise','silesia','slask','mazovia','malopolska',
 'wielkopolska','pomerania','galicia','catalonia','cataluna','andalusia','andalucia','castile','castilla',
 'extremadura','aragon','navarra','bavaria','bayern','tyrol','flanders','wallonia','brabant','parish','near',
 'monte','mons','montis','eremo','territory','territorio','loci','tolfa','avellino','dalmatia','valtellina','salento','japigia',
 # 'holy' in Slavic languages — the Czech/Polish san/santa: Svatá Hora and Svatý Kopeček are different places
 'svata','svaty','svate','sveta','sveti','svete','swieta','swiety','swiete','sw','sv','sventa','sventas','sviata','sviatyi',
 # institutions and orders are not places either: 'Łuck, Dominicans' and 'Lwów, Dominicans' share nothing
 'dominican','dominicans','dominikani','dominikanow','franciscan','franciscans','bernardine','bernardines','bernardynow',
 'augustinian','augustinians','jesuit','jesuits','carmelite','carmelites','theatine','theatines','piarist','piarists',
 'capuchin','capuchins','benedictine','benedictines','servite','servites','convent','monastery','klasztor','cathedral',
 'church','kosciol','kostel','chiesa','iglesia','basilica','sanctuary','shrine','sanktuarium','collegiate','abbey','oratory',
 'diocese','archdiocese','province','state','departamento','department','county','district','shrine','sanctuary'}
ECCL_STOP={'ecclesia','ecclesiae','paroecialis','paroeciali','templum','templo','templi','basilica',
 'basilicae','minoris','sanctuario','santuario','sanctuary','shrine','aedes','aede','cathedral','cathedralis',
 'cathedrali','collegiata','conventus','monasterii','monastery','church','parish','chiesa','iglesia','igreja',
 'kosciol','sacra','sacro','sacrum','dedicata','dicata','dicatum','honorem','beatae','mariae','virginis',
 'sanctae','sancti','sanctus','santa','santo','maria','virgin','nostra','domina','dominae','deiparae'}
def loc_toks(r):
    """Place signature: the LOCALITY only, keeping any parenthetical gloss (usually the Latin or
    modern equivalent of the same place, e.g. 'Mexicopolis (Mexico City)'). Sanctuary names were
    tried here too and had to be removed: they dragged unrelated shrines together."""
    raw=norm(r.get('locality')).replace('romae','rome').replace('roma','rome')   # one token for the city
    raw=raw.replace('(',' ').replace(')',' ').replace(';',' ').replace('/',' ')
    return {p for p in re.sub(r'[^a-z0-9 ]',' ',raw).split()
            if len(p)>2 and p not in GEO_STOP and p not in ECCL_STOP}
def _ed1(a,b):
    if a==b: return True
    if abs(len(a)-len(b))>1 or min(len(a),len(b))<6: return False   # 'Enna'/'Penna' are different places
    if len(a)>len(b): a,b=b,a
    i=j=d=0
    while i<len(a) and j<len(b):
        if a[i]==b[j]: i+=1; j+=1
        else:
            d+=1
            if d>1: return False
            if len(a)==len(b): i+=1; j+=1
            else: j+=1
    return d+(len(b)-j)+(len(a)-i)<=1
def place_match(A,B):
    """True if two place signatures name the same place (exact token, or one typo/inflection apart:
    Roma/Rome, Talpa/Talpa)."""
    if A & B: return True
    return any(_ed1(a,b) for a in A for b in B)
def loc_key(r):
    t=loc_toks(r)
    return min(t)[:7] if t else None
SYN={ # cross-language equivalents of the commonest Marian titles, mapped to one canonical token
 'dolorosa':'dolor','bolesna':'dolor','addolorata':'dolor','dolores':'dolor','perdolens':'dolor','perdolentis':'dolor','pieta':'dolor','sorrows':'dolor',
 'laskawa':'gratia','laskawej':'gratia','gratiarum':'gratia','grazie':'gratia','gracias':'gratia','graces':'gratia','gratiosa':'gratia',
 'rozancowa':'rosario','rozancowej':'rosario','rosario':'rosario','rosary':'rosario','rosarii':'rosario',
 'pocieszenia':'consol','consolatione':'consol','consolation':'consol','consolazione':'consol','consolatrix':'consol',
 'zwycieska':'victoria','victrix':'victoria','vittoria':'victoria','victoria':'victoria','victory':'victoria',
 'sniezna':'nivis','nivis':'nivis','neve':'nivis','nieves':'nivis','snows':'nivis',
 'niepokalana':'immac','immaculata':'immac','inmaculada':'immac','immacolata':'immac','immaculate':'immac','immaculatae':'immac',
 'czestochowska':'czestochow','czestochoviensis':'czestochow','jasnogorska':'czestochow',
 'wniebowzieta':'assumpta','assumpta':'assumpta','assunta':'assumpta','asuncion':'assumpta','assumption':'assumpta',
 'krolowa':'regina','regina':'regina','reina':'regina','queen':'regina','regine':'regina',
 'milosierdzia':'misericord','misericordiae':'misericord','misericordia':'misericord','mercy':'misericord','merced':'misericord'}
def title(r):
    return {SYN.get(x,x) for x in toks(r.get('image_title_vernacular'),r.get('image_title_latin'))}

tokloc=collections.defaultdict(set)
for r in R:
    for t in title(r): tokloc[t].add(loc_key(r) or '?')
def distinctive(ts): return {t for t in ts if len(tokloc[t])<=2}

for i,r in enumerate(R): r['_i']=i
clusters=[];bycountry=collections.defaultdict(list);noloc=[]
for r in R:
    (bycountry[r.get('country')] if loc_toks(r) else noloc).append(r)
def subj(x):
    s=norm(x.get('image_subject'))
    if not s: return None
    if 'virgin' in s or 'mary' in s or 'maria' in s: return 'bvm'
    for k in ('joseph','sacred heart','cord','infant','nino','family','famili','crucifi','christ','anne','nichol'):
        if k in s: return k
    return s[:12]
def subj_ok(g,r):
    """Never merge across different subjects (a St Joseph is not a Marian image)."""
    a={subj(x) for x in g if subj(x)}; b=subj(r)
    return (not a) or (b is None) or (b in a)
def tcompat(g,r):
    """Titles agree, OR one side carries no identifying word at all once descriptive praise is
    stripped — in which case the shared locality plus subject is what establishes identity."""
    if not subj_ok(g,r): return False
    tg=set().union(*[title(x) for x in g]); tr=title(r)
    return (not tg) or (not tr) or bool(tg&tr) or bool({t[:5] for t in tg}&{t[:5] for t in tr})
for c,rs in bycountry.items():
    groups=[]
    for r in rs:
        lr=loc_toks(r)
        if r.get('standalone'):            # insufficient identity to merge (e.g. a town and a year only)
            groups.append([r]); continue
        cands=[g for g in groups if place_match(set().union(*[loc_toks(x) for x in g]),lr) and tcompat(g,r)]
        if not cands and r.get('coronation_date'):
            # titles disagree (often just Latin vs vernacular) but the same place was crowned in the same year
            y=str(r['coronation_date'])[:4]
            same=[g for g in groups if place_match(set().union(*[loc_toks(x) for x in g]),lr) and subj_ok(g,r)
                  and any(str(x.get('coronation_date') or '')[:4]==y for x in g)]
            if len(same)==1: cands=same
        if len(cands)==1:
            cands[0].append(r)
        elif len(cands)>1:
            # ambiguous: prefer a cluster that shares a title token, else one sharing a coronation
            # date, else refuse to guess and keep the record separate
            tr=title(r)
            strong=[g for g in cands if tr and (tr & set().union(*[title(x) for x in g]))]
            if len(strong)!=1 and r.get('coronation_date'):
                y=str(r['coronation_date'])[:4]
                strong=[g for g in cands if any(str(x.get('coronation_date') or '')[:4]==y for x in g)]
            if len(strong)==1: strong[0].append(r)
            else: groups.append([r])
        else:
            groups.append([r])
    clusters.extend(groups)
for r in noloc:
    tr=title(r); dr=distinctive(tr); tgt=None
    cands=[g for g in clusters if g[0].get('country')==r.get('country')
           and (tr & set().union(*[title(x) for x in g]))]
    # a shared coronation date settles which shrine is meant
    if r.get('coronation_date'):
        y=str(r['coronation_date'])[:4]
        dated=[g for g in cands if any(str(x.get('coronation_date') or '')[:4]==y for x in g)]
        if len(dated)==1: tgt=dated[0]
    if tgt is None and dr:
        for g in cands:
            if dr & distinctive(set().union(*[title(x) for x in g])): tgt=g; break
    if tgt is not None: tgt.append(r)
    else: clusters.append([r])
# NOTE: an earlier build had a third pass merging clusters in the same country that shared a
# 'distinctive' title token even when their localities differed. It was removed: it wrongly fused
# Notre-Dame des Miracles at Rennes with Mauriac, the Carmine 'la Bruna' at Naples with Matera, and
# the four separate images John Paul II crowned together at Jasna Gora. Marian titles repeat; place
# is the identity. A false merge destroys a distinct image, a false split is merely a duplicate —
# so this errs toward splitting.

def collapse_dates(dates):
    """One crowning reported at two precisions is ONE crowning. '1954' and '1954-08-29' are the
    same event, so keep only the most precise form for each year; distinct years remain distinct,
    which is what makes a multi-entry list mean the image really was crowned more than once."""
    best={}
    for d in dates:
        d=str(d).strip()
        m=re.match(r'(\d{4})',d)
        if not m:
            best.setdefault(d,d); continue
        y=m.group(1)
        if y not in best or len(d)>len(best[y]): best[y]=d
    return sorted(best.values())

SRC=['series','volume','year','page','folio','folio_to','citation','source_pdf_url','act_number','act_type','pope',
     'evidence_type','act_date','concession_date','coronation_date','legate','deputy','register_refs','documents',
     'rubric_latin','incipit_latin','confidence','notes']
RANK={'papal_coronation_act':4,'chapter_decree':4,'papal_legate_deputation':3,'papal_personal_coronation':3,
      'retrospective_attestation':1,'norms':0,'petition_not_conceded':-1}
CONF={'high':3,'medium':2,'low':1}
def best(g,f):
    vals=[x.get(f) for x in g if x.get(f)]
    if not vals: return None
    c=collections.Counter(vals)
    return sorted(vals,key=lambda v:(c[v],len(str(v))),reverse=True)[0]
def slug(s,n=48):
    s=re.sub(r'[^a-z0-9]+','-',norm(s)).strip('-')
    return s[:n].rstrip('-') or 'image'

images=[];seen=collections.Counter()
for g in clusters:
    g=sorted(g,key=lambda r:(r.get('year') or 9999,{'ACSP':0,'LIT':1,'ASS':2,'AAS':3}.get(r.get('series'),4),r.get('page') or 0))
    cds=collapse_dates([x['coronation_date'] for x in g if x.get('coronation_date')])
    ev=sorted({x['evidence_type'] for x in g},key=lambda e:-RANK.get(e,0))
    base=slug((best(g,'image_title_vernacular') or best(g,'image_title_latin') or 'image')+'-'+(best(g,'locality') or best(g,'country') or ''))
    seen[base]+=1; iid=base if seen[base]==1 else f'{base}-{seen[base]}'
    images.append({
      'id':iid,
      'image_title_vernacular':best(g,'image_title_vernacular'),
      'image_title_latin':best(g,'image_title_latin'),
      'image_subject':best(g,'image_subject'),
      'church_or_sanctuary':best(g,'church_or_sanctuary'),
      'locality':best(g,'locality'),
      'diocese_latin':best(g,'diocese_latin'),
      'diocese_modern':best(g,'diocese_modern'),
      'country':best(g,'country'),
      'coronation_dates':cds,
      'first_coronation':cds[0] if cds else None,
      'strongest_evidence':ev[0] if ev else None,
      'evidence_types':ev,
      'popes':sorted({x['pope'] for x in g if x.get('pope')}),
      'legates':sorted({x['legate'] for x in g if x.get('legate')}),
      'confidence':max((x.get('confidence') for x in g),key=lambda c:CONF.get(c,0)),
      'source_count':len(g),
      'sources':[{k:x.get(k) for k in SRC} for x in g],
    })
def sk(im):
    d=im['first_coronation'] or ''
    m=re.match(r'(\d{4})',d)
    return (im['country'] or 'zz', im['locality'] or '', int(m.group(1)) if m else 9999)
images.sort(key=sk)
st={'images':len(images),'source_records':sum(i['source_count'] for i in images),
 'by_country':dict(collections.Counter(i['country'] for i in images if i['country']).most_common()),
 'by_strongest_evidence':dict(collections.Counter(i['strongest_evidence'] for i in images)),
 'by_confidence':dict(collections.Counter(i['confidence'] for i in images)),
 'multi_source_images':sum(1 for i in images if i['source_count']>1)}
meta=dict(META)
meta.update({'title':'Imagines Coronatae — crowned sacred images attested in the official acts of the Holy See',
 'generated':datetime.date.today().isoformat(),'record_count':len(images),
 'structure':('One record per CROWNED IMAGE. Every ASS/AAS act that attests it is kept in that '
   'image’s `sources` array, so an image cited in several volumes is ONE record with several '
   'sources, not several records. Images are identified by locality first, since Marian titles '
   'repeat worldwide; a distinctive title can also unite an image crowned away from its shrine.'),
 'statistics':st})
meta.pop('by_series',None)
json.dump({'metadata':meta,'images':images},open(REPO+'/data/imagines-coronatae.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
IMF=['id','image_title_vernacular','image_title_latin','image_subject','church_or_sanctuary','locality',
     'diocese_latin','diocese_modern','country','first_coronation','coronation_dates','strongest_evidence',
     'popes','legates','confidence','source_count']
with open(REPO+'/data/imagines-coronatae.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=IMF,extrasaction='ignore'); w.writeheader()
    for i in images: w.writerow({**i,'coronation_dates':'; '.join(i['coronation_dates']),
                                 'popes':'; '.join(i['popes']),'legates':'; '.join(i['legates'])})
with open(REPO+'/data/sources.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=['image_id','image_title_vernacular','country']+SRC,extrasaction='ignore')
    w.writeheader()
    for i in images:
        for s in i['sources']:
            w.writerow({'image_id':i['id'],'image_title_vernacular':i['image_title_vernacular'],'country':i['country'],**s})
print('unique images:',len(images),'| source records kept:',st['source_records'],'| multi-source:',st['multi_source_images'])
print('countries:',len(st['by_country']))
print('strongest evidence:',st['by_strongest_evidence'])
