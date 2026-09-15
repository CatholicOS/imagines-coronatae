import json,re,collections,unicodedata as U,datetime,os,csv,pathlib
import pathlib
REPO=str(pathlib.Path(__file__).resolve().parent.parent)
src=json.load(open(REPO+'/data/attestations.json',encoding='utf-8'))
R=src['records'] if isinstance(src,dict) else src
for _extra in ('attestations-acsp.json','attestations-lit.json'):   # Chapter-archive and literature layers
    _p=pathlib.Path(REPO)/'data'/_extra
    if _p.exists(): R=R+json.load(open(_p,encoding='utf-8'))['records']
META=src.get('metadata',{}) if isinstance(src,dict) else {}
SPECIAL=str.maketrans({'ł':'l','Ł':'l','ø':'o','đ':'d','æ':'ae','œ':'oe','ß':'ss','þ':'th','’':"'",'‘':"'",'´':"'",'`':"'"})   # curly apostrophes split words too
STOP=set('''nuestra senora nossa senhora notre dame madonna matka boza bozej panna beata beatae maria mariae
mariam marii virgo virgen vergine virginis virgin imago imaginem imagen simulacrum simulacro effigies effigie
statua statue icon iconem sacra sacrae sacro sacrum santa sancta sanctae santo san sao our lady domina dominae
nostra nostrae della delle del dei los las sub titulo vulgo appellata appellatae invocatae dicta dictae
deipara deiparae genetricis the and que pie colitur servatur templo ecclesia templi loco urbe urbis oppido dioecesis built
archidioecesis fines intra quae cum divino puero iesu christi mater matris madre nuncupata nuncupatae
antiqua antiquum vetus vetusta miraculis clara insignis titulus
bambino gesu puero pueri iesu child figlio divin vergine santissima ssma sma miracolosa effigie vera suo sua detta holy swieta
majka bozja matki obraz bozej bozi boze mother dievo motina gottes mutter signora signore copy madonnina mare deu senyora
dell nell sull dall coll degli alla alle nella nel
existentes existente loci reformatorum francisci dipinta luca fratrum minorum dalmatia
scuole schole pie padri frati monaci teatini cappuccini agostiniani domenicani francescani gesuiti serviti
sant sanct saint sankt sainte santi sancti chapel cappella capilla chapelle palazzo palace
chiesa nella nelle receipt imagines jesu roma rome esistente chiesa ordine congregazione convento
# Latin/vernacular DESCRIPTIVE adjectives. These praise an image, they do not identify it, and if
# left in they block real merges: Notre-Dame du Cap reduced to {rosario} in one act and
# {perinsigne} in another, so two records for one shrine survived side by side.
perinsigne perinsignis mirifica mirificam insigne insignem praeclara praeclarum praeclarus veneranda venerandum
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
 'frazione','frazioen','quartiere','villaggio','sobborgo','zona','distretto','comune','localita','contrada',
 'les','des','juarez',
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
 'diocese','archdiocese','province','state','departamento','department','county','district','shrine','sanctuary',
 'valle','val','vall','vallis','valley','della','delle','dei','degli','delli','alla','alle','nel','nella','madonna',
 'vergine','maria','citta','city','dell','nell','sull','all','del','maggiore','minore','nuova','nuovo','vecchia','vecchio','grande','piccola'}
ECCL_STOP={'ecclesia','ecclesiae','paroecialis','paroeciali','templum','templo','templi','basilica',
 'basilicae','minoris','sanctuario','santuario','sanctuary','shrine','aedes','aede','cathedral','cathedralis',
 'cathedrali','collegiata','conventus','monasterii','monastery','church','parish','chiesa','iglesia','igreja',
 'kosciol','sacra','sacro','sacrum','dedicata','dicata','dicatum','honorem','beatae','mariae','virginis',
 'sanctae','sancti','sanctus','santa','santo','maria','virgin','nostra','domina','dominae','deiparae'}
CITY={'naples':'napoli','neapolis':'napoli','neapolim':'napoli','genoa':'genova','genua':'genova','venice':'venezia','venetiae':'venezia',
 'florence':'firenze','florentia':'firenze','milan':'milano','mediolanum':'milano','turin':'torino','padua':'padova','patavium':'padova',
 'mantua':'mantova','syracuse':'siracusa','leghorn':'livorno','lucerne':'luzern','cologne':'koln','vienna':'wien','prague':'praha',
 'cracow':'krakow','warsaw':'warszawa','lisbon':'lisboa','seville':'sevilla','saragossa':'zaragoza','antwerp':'antwerpen',
 'brussels':'bruxelles','geneva':'geneve','mexicopolis':'mexico',
 # the Italian exonyms of Basilici-Bigliazzi, and a sanctuary's village against the city or diocese another source names
 'messico':'mexico','cracovia':'krakow','siviglia':'sevilla','ginevra':'geneve','colonia':'koln','gorica':'gorizia',
 'bologhine':'algiers','icosium':'algiers','algeri':'algiers','alger':'algiers','ourem':'fatima','orselina':'locarno',
 'tongre':'chievres','chevremont':'chaudfontaine','lajas':'ipiales','rivieres':'madeleine','bergheim':'plain',
 'montaigu':'scherpenheuvel','zichem':'scherpenheuvel','bonsecours':'peruwelz','mompantero':'rocciamelone',
 'laghi':'lagos','tlaxcalensis':'tlaxcala'}
def loc_toks(r):
    """Place signature: the LOCALITY only, keeping any parenthetical gloss (usually the Latin or
    modern equivalent of the same place, e.g. 'Mexicopolis (Mexico City)'). Sanctuary names were
    tried here too and had to be removed: they dragged unrelated shrines together."""
    raw=norm(r.get('locality')).replace('romae','rome').replace('roma','rome')   # one token for the city
    for a,b in CITY.items(): raw=re.sub(r'\b'+a+r'\b',b,raw)
    raw=raw.replace('(',' ').replace(')',' ').replace(';',' ').replace('/',' ')
    out={p for p in re.sub(r'[^a-z0-9 ]',' ',raw).split()
            if len(p)>2 and p not in GEO_STOP and p not in ECCL_STOP}
    if not out:   # 'Re' (Val Vigezzo) is a place, not a missing locality
        out={p for p in re.sub(r'[^a-z0-9 ]',' ',raw).split() if len(p)==2 and p.isalpha()}
    return out
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
ROME_NOISE={'della','delle','del','dei','degli','alla','alle','nel','nella','nell','col','con','per','the',
 'near','vicino','presso','madonna','ceremony','copy','vatican','vaticana','vaticano','rione','church','chiesa','basilica'}
def rome_sig(A): return {a for a in A if a!='rome' and a not in ROME_NOISE}
def _sub(A,B):
    """A ⊆ B, one typo per token allowed."""
    return all(a in B or any(_ed1(a,b) for b in B) for a in A)
def place_match(A,B):
    """True if two place signatures name the same place (exact token, or one typo/inflection apart:
    Roma/Rome, Talpa/Talpa).
    ROME is the exception: over a hundred distinct images were crowned there, so the city alone
    is not a place. Two Roman records match only if their church signatures agree — one is a
    subset of the other, so 'Rome' or 'Rome (Borgo)' still reaches 'Rome, S. Lorenzo in Borgo' and
    the title decides — and a Roman record never matches a record from anywhere else, however many
    saints' names the two churches share (San Giovanni in Fonte is not San Giovanni Valdarno)."""
    ra,rb='rome' in A,'rome' in B
    if ra!=rb: return False
    if ra and rb:
        A2,B2=rome_sig(A),rome_sig(B)
        return _sub(A2,B2) or _sub(B2,A2)
    if A & B:
        # a saint's name is not a place: San Giovanni Rotondo is not San Giovanni Valdarno — unless a
        # side has nothing else ('San Sebastian')
        if (A & B) <= SAINTS and (A-SAINTS) and (B-SAINTS): return False
        return True
    return any(_ed1(a,b) for a in A for b in B)
SAINTS={'giovanni','pietro','paolo','martino','giorgio','michele','nicola','nicolo','lorenzo','stefano','giacomo','andrea',
 'antonio','francesco','salvatore','vito','marco','angelo','benedetto','severino','miniato','gennaro','felice','vincenzo',
 'sebastian','sebastiano','juan','pedro','pablo','jose','miguel','francisco','antonio','martin','jean','pierre','paul',
 'martin','georges','michel','nicolas','laurent','etienne','jacques','andre','sebastien'}
def loc_key(r):
    t=loc_toks(r)
    return min(t)[:7] if t else None
SYN={ # cross-language equivalents of the commonest Marian titles, mapped to one canonical token
 'dolorosa':'dolor','bolesna':'dolor','addolorata':'dolor','dolores':'dolor','perdolens':'dolor','perdolentis':'dolor','pieta':'dolor','sorrows':'dolor',
 'laskawa':'gratia','laskawej':'gratia','gratiarum':'gratia','grazie':'gratia','gracias':'gratia','graces':'gratia','gratiosa':'gratia',
 'rozancowa':'rosario','rozancowej':'rosario','rosario':'rosario','rosary':'rosario','rosarii':'rosario','rosarium':'rosario','rosarij':'rosario',
 'pocieszenia':'consol','consolatione':'consol','consolation':'consol','consolazione':'consol','consolatrix':'consol',
 'zwycieska':'victoria','victrix':'victoria','vittoria':'victoria','victoria':'victoria','victory':'victoria',
 'sniezna':'nivis','nivis':'nivis','neve':'nivis','nieves':'nivis','snows':'nivis',
 'niepokalana':'immac','immaculata':'immac','inmaculada':'immac','immacolata':'immac','immaculate':'immac','immaculatae':'immac',
 'czestochowska':'czestochow','czestochoviensis':'czestochow','jasnogorska':'czestochow',
 'wniebowzieta':'assumpta','assumpta':'assumpta','assunta':'assumpta','asuncion':'assumpta','assumption':'assumpta',
 'krolowa':'regina','regina':'regina','reina':'regina','queen':'regina','regine':'regina',
 'milosierdzia':'misericord',
 'rodzina':'family','famiglia':'family','familia':'family','famille':'family','familiae':'family','family':'family',
 'febre':'febbre','febbre':'febbre','sanita':'salute','salute':'salute','anna':'anne','annae':'anne','anne':'anne','lapurdi':'lourdes','lapurdensis':'lourdes','misericordiae':'misericord','misericordia':'misericord','mercy':'misericord','merced':'misericord'}
TITLE_STOP=ECCL_STOP|{'cattedrale','catedrale','collegiata','metropolitana','monastero','oratorio','eremo','ritiro',
 'monache','chierici','regolari','teatini','carmelitani','cappucini','cappuccini','benedettini','domenicani',
 'camaldolesi','camandolesi','basiliani','premostratensi','bernabiti','riformati','osservanti','minori','parrochiale',
 'benedictine','coenobium','coenobio','monasterium','monasterii','territoriale','territorial',
 'citta','regno','diocesi','provincia','vicino','fuori','presso','dentro','sopra','sulla','sul','incontro','detta',
 'della','delle','degli','alla','alle','nella','nell','stanze','cappella','portico','congregazione','madre','madri',
 'chapel','shrine','sanctuary','cathedral','collegiate','monastery','convent','church','abbey','abbazia','parish',
 'santuario','indie','occidentali','maggiore','minore','nuova','nuovo','vecchia','vecchio'}
def title_full(r):
    """Title words including any place word — used only for records that name no locality at all,
    where the title is the only thing that can carry the place ('Nossa Senhora Aparecida')."""
    return {SYN.get(x,x) for x in toks(r.get('image_title_vernacular'),r.get('image_title_latin')) if x not in TITLE_STOP}
def title(r):
    """Identifying words of the title: the place's own tokens and words for kinds of building are
    not identity ('Santa Maria della Neve di Frosinone' identifies by 'neve', not by 'frosinone',
    which the locality already carries; 'Santa Maria nella Cattedrale di Verona' by nothing at all,
    and then the place and the year have to carry it)."""
    lt=loc_toks(r)
    return {SYN.get(x,x) for x in toks(r.get('image_title_vernacular'),r.get('image_title_latin'))
            if x not in TITLE_STOP and x not in lt and not any((len(l)>=4 and x.startswith(l)) or (len(x)>=5 and l.startswith(x)) or (len(x)>=8 and _ed1(x,l)) for l in lt)}

tokloc=collections.defaultdict(set)
for r in R:
    if str(r.get('act_number') or '').startswith('BB'): continue    # their thousand copies of Fátima and Lourdes would make no title distinctive
    for t in title_full(r): tokloc[t].add(loc_key(r) or '?')
def distinctive(ts): return {t for t in ts if len(tokloc[t])<=2}

for i,r in enumerate(R): r['_i']=i
clusters=[];bycountry=collections.defaultdict(list);noloc=[]
for r in R:
    (bycountry[r.get('country')] if loc_toks(r) else noloc).append(r)
def subj(x):
    s=norm(x.get('image_subject'))
    if not s: return None
    # 'other (St Anne, mother of the Blessed Virgin Mary)' names Mary without being her
    if ('virgin' in s or 'mary' in s or 'maria' in s) and not s.startswith(('other','saint','st ','st.','sant')): return 'bvm'
    for k in ('joseph','sacred heart','cord','infant','nino','family','famili','crucifi','christ','anne','anna','nichol'):
        if k in s: return k
    return s[:12]
def subj_ok(g,r):
    """Never merge across different subjects (a St Joseph is not a Marian image)."""
    a={subj(x) for x in g if subj(x)}; b=subj(r)
    return (not a) or (b is None) or (b in a)
def yr_of(r):
    """The year a record dates its crowning to — the ceremony, else the decree, else the act."""
    gaz=r.get('series') in ('ASS','AAS')     # a gazette act's own date says nothing about the crowning
    for k in (('coronation_date',) if gaz else ('coronation_date','concession_date','act_date')):
        m=re.match(r'(\d{4})',str(r.get(k) or ''))
        if m: return int(m.group(1))
    return r.get('year') if isinstance(r.get('year'),int) and not gaz else None
def work(r):
    """Which source a record comes from: the series, or for the literature layer the work."""
    if r.get('series')!='LIT': return r.get('series')
    return re.match(r'[A-Za-z]*',str(r.get('act_number') or '')).group(0)
def rome_church_ok(g,r):
    """In Rome, when both sides name their church, the churches must agree: the Madonna degli
    Angeli of Sant'Agata dei Tessitori (1729) is not Santa Maria degli Angeli alle Terme (1920)."""
    lr=loc_toks(r)
    if 'rome' not in lr: return True
    if rome_sig(lr) and any(rome_sig(lr)==rome_sig(loc_toks(x)) for x in g): return True   # same church already
    cr={t for t in toks(r.get('church_or_sanctuary')) if t not in ECCL_STOP and t not in ROME_NOISE}
    if not cr: return True
    for x in g:
        cx={t for t in toks(x.get('church_or_sanctuary')) if t not in ECCL_STOP and t not in ROME_NOISE}
        if cx and not (cx&cr) and not any(_ed1(a,b) or (len(a)>=7 and len(b)>=7 and a[:7]==b[:7]) for a in cx for b in cr): return False
    return True
def tcompat(g,r):
    """Titles agree, OR one side carries no identifying word at all once descriptive praise is
    stripped — in which case the shared locality plus subject is what establishes identity."""
    if not subj_ok(g,r): return False
    tg=set().union(*[title(x) for x in g]); tr=title(r)
    if not tg or not tr:
        # One side has no identifying word once place and building words are gone. If the other
        # side's title names the first side's church ('Madonna ... di S. Lorenzo ... di Borgo' /
        # 'Rome, San Lorenzo in Borgo'), that is the identification.
        T=tg or tr
        P=set().union(*[loc_toks(x)|{t for t in toks(x.get('church_or_sanctuary')) if t not in TITLE_STOP} for x in (g if not tg else [r])])
        if T & P or ({t[:7] for t in T if len(t)>=7} & {t[:7] for t in P if len(t)>=7}): return True
        # Otherwise the place alone must carry identity — in Rome only the same church (a church
        # may hold several crowned images, so a bare 'Rome' never suffices); elsewhere only the
        # SAME token, not one letter away (Krzeszów is not Rzeszów); and never between two entries
        # of the same register (a register lists distinct images, and if it meant the same one it
        # would have said so). Between registers the years must agree to within a year — a
        # register may give the decree year, a dossier the ceremony; a gazette act joining is
        # exempt, as its wording often praises the image rather than naming it.
        if 'rome' in loc_toks(r):
            sr=rome_sig(loc_toks(r))
            if not sr or not any(rome_sig(loc_toks(x)) and (_sub(sr,rome_sig(loc_toks(x))) or _sub(rome_sig(loc_toks(x)),sr)) for x in g):
                return False   # not the same church
        elif not (set().union(*[loc_toks(x) for x in g]) & loc_toks(r)): return False
        if r.get('series') in ('ASS','AAS'): return True
        if r.get('series')=='LIT' and any(work(x)==work(r) for x in g): return False
        yg={yr_of(x) for x in g if yr_of(x)}
        yr=yr_of(r)
        if not yg or not yr: return True
        tol=2 if 'rome' in loc_toks(r) else 1      # the same Roman church: registers differ by up to two years
        return any(abs(yr-y)<=tol for y in yg)
    return bool(tg&tr) or bool({t[:7] for t in tg if len(t)>=7}&{t[:7] for t in tr if len(t)>=7})
for c,rs in bycountry.items():
    groups=[]
    for r in rs:
        lr=loc_toks(r)
        if r.get('standalone'):            # insufficient identity to merge (e.g. a town and a year only)
            groups.append([r]); continue
        if r.get('aligned'):               # its locality string was aligned by hand to the catalogue's (Basilici-Bigliazzi, Rome)
            same=[g for g in groups if any(x.get('locality')==r['locality'] for x in g) and subj_ok(g,r)]
            if len(same)==1: same[0].append(r); continue
        if r.get('parent_act'):            # a second crown on an image listed just above (the Child's)
            par=[g for g in groups if any(x.get('act_number')==r['parent_act'] and work(x)==work(r) for x in g)]
            if len(par)==1: par[0].append(r); continue
        # a standalone record (a town and a year, or a title with no date) accepts a joiner only on
        # the strength of a shared title word, never on place and year alone
        cands=[g for g in groups if (not g[0].get('standalone') or (title_full(r) & set().union(*[title_full(x) for x in g])))
               and place_match(set().union(*[loc_toks(x) for x in g]),lr) and tcompat(g,r) and rome_church_ok(g,r)]
        if not cands and r.get('coronation_date'):
            # Titles disagree but the same place was crowned in the same year. This is how a Latin
            # gazette rubric meets an Italian dossier or register ('Templum Tersactense B. M. V.
            # Matris Gratiarum' / 'Madonna di Tersatto'). Two full dates that differ are two
            # crownings, not one: Genoa's Madonnetta (27 June 1920) and Nostra Signora delle Vigne
            # (21 November 1920) are not the same image. And between two literature registers the
            # year alone is not enough (Benevento 1723: Balzamo's Incoronata of the Camaldolese and
            # Briccolani's Madonna delle Grazie are two images) unless one of them gives the day —
            # a register that says 10 May 1736 at Brno means one crowning.
            d=str(r['coronation_date']); y=d[:4]
            def same_day(x):
                xd=str(x.get('coronation_date') or '')
                return xd[:4]==y and not (len(xd)==10 and len(d)==10 and xd!=d)
            def precise(x): return len(str(x.get('coronation_date') or ''))==10
            same=[g for g in groups if place_match(set().union(*[loc_toks(x) for x in g]),lr) and subj_ok(g,r)
                  and any(same_day(x) for x in g)
                  and not (r.get('series')=='LIT' and any(work(x)==work(r) for x in g))   # a register lists distinct images (Caldarola, 17 May 1814: two)
                  and (r.get('series')!='LIT' or any(x.get('series')!='LIT' for x in g)
                       or precise(r) or any(precise(x) and same_day(x) for x in g))]
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
def generic(t): return len(tokloc[t])>8      # a title word used at more than eight places identifies nothing, even with a matching year
for r in noloc:
    tr=title_full(r); dr=distinctive(tr); tgt=None
    # never a Roman cluster: Rome holds a hundred crowned images, and a Roman act says 'Romae' or
    # 'in Urbe' — the Madonna del Rimedio of Arborea (Sardinia) is not the one in S. Dionigi
    # a cluster known only from Basilici-Bigliazzi is reached only on a distinctive word AND the year
    # (the Caysasay act of 1954 finds their Taal, a Fátima act finds none of their copies)
    y0=str(r.get('coronation_date') or '')[:4]
    cands=[g for g in clusters if g[0].get('country')==r.get('country')
           and (tr & set().union(*[title_full(x) for x in g]))
           and not any('rome' in loc_toks(x) for x in g)
           and (any(work(x)!='BB' for x in g)
                or (y0 and (dr & distinctive(set().union(*[title_full(x) for x in g])))
                    and any(str(x.get('coronation_date') or '')[:4]==y0 for x in g)))]
    # a shared DISTINCTIVE title word settles it ('Lattani', 'Coromoto')
    if dr:
        for g in cands:
            if dr & distinctive(set().union(*[title_full(x) for x in g])): tgt=g; break
    # else a shared coronation date, provided the shared word is not one used everywhere ('regina')
    if tgt is None and r.get('coronation_date'):
        y=str(r['coronation_date'])[:4]
        dated=[g for g in cands if any(str(x.get('coronation_date') or '')[:4]==y for x in g)
               and any(not generic(t) for t in tr & set().union(*[title_full(x) for x in g]))]
        if len(dated)==1: tgt=dated[0]
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
    # A bare year from a register close to a full date from a dossier or act is the same
    # crowning too: registers often give the year of the decree, the dossier the day of the
    # ceremony (Lucca: decree 1689, crowned 30 April 1690; Cava de' Tirreni: 1764, crowned 15 June
    # 1766). Up to two years before the full date, one year after.
    for y in list(best):
        if len(best[y])==4 and y.isdigit() and any(len(best[z])>4 and z.isdigit() and -1<=int(z)-int(y)<=2 for z in best):
            del best[y]
    return sorted(best.values())

SRC=['series','volume','year','page','folio','folio_to','citation','source_pdf_url','act_number','act_type','pope',
     'evidence_type','act_date','concession_date','coronation_date','legate','deputy','register_refs','documents',
     'rubric_latin','incipit_latin','confidence','notes','parent_act']
RANK={'papal_coronation_act':4,'chapter_decree':4,'papal_legate_deputation':3,'papal_personal_coronation':3,
      'retrospective_attestation':1,'norms':0,'petition_not_conceded':-1}
CONF={'high':3,'medium':2,'low':1}
def best(g,f):
    # a Child's-crown entry names the image by its parent, and a Basilici-Bigliazzi row gives Italian
    # exonyms ('Santiago del Cile'): let the image's own records name it where there are any
    own=[x for x in g if not x.get('parent_act') and work(x)!='BB'] or [x for x in g if not x.get('parent_act')] or g
    vals=[x.get(f) for x in own if x.get(f)]
    if not vals: return None
    c=collections.Counter(vals)
    # on a tie a title that is nothing but praise ('mirifica Beatissimae Mariae Virginis imago') loses
    # to one with an identifying word ('Antiquissima imago mariana loci Piekary'); then the longer wins
    ident=(lambda v:any(t not in TITLE_STOP for t in toks(v))) if f.startswith('image_title') else (lambda v:0)
    return sorted(vals,key=lambda v:(c[v],ident(v),len(str(v))),reverse=True)[0]
def slug(s,n=48):
    s=re.sub(r'[^a-z0-9]+','-',norm(s)).strip('-')
    return s[:n].rstrip('-') or 'image'

images=[];seen=collections.Counter()
for g in clusters:
    g=sorted(g,key=lambda r:(r.get('year') or 9999,{'ACSP':0,'LIT':1,'ASS':2,'AAS':3}.get(r.get('series'),4),r.get('page') or 0))
    # a crown for the Child of an image already crowned (a register's 'Bambino Gesù' entry) is not a re-crowning of the image
    # first-hand sources first, so that where two full dates fall in one year (Coromoto: the act's 12
    # September 1952, Basilici-Bigliazzi's 11th) the one read at first hand is the one kept
    cds=collapse_dates([x['coronation_date'] for x in sorted(g,key=lambda x:x.get('series')=='LIT') if x.get('coronation_date') and not x.get('parent_act')])
    ev=sorted({x['evidence_type'] for x in g},key=lambda e:(-RANK.get(e,0),e))   # tie-break by name: set order is not stable across runs
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
