import re,glob,os,json,collections
def unspace(s): return re.sub(r'(?:\b[A-Z] ){2,}[A-Z]\b', lambda m: m.group(0).replace(' ',''), s)
def meta(fn):
    m=re.match(r'AAS-(\d+)(?:-(I{1,2}))?-(\d{4})(?:-(I{1,2}))?-ocr',fn)
    if m: return int(m.group(1)),int(m.group(3)),(m.group(2) or m.group(4))
    m=re.match(r'(\d{4})_',fn)
    if m: return int(m.group(1))-1908,int(m.group(1)),None
    return None,None,None
# expanded lexicon: + sertum (garland), redimiend*, and de-hyphenated matching
CORO=re.compile(r'coronat|coronand|coronav|coronet|coronar|coronass|corona\b|coronam|coronae|coronis|coronas'
  r'|diadem|redimit|redimir|redimiat|redimiv|redimiend|redimien|incoronaz|cingi\b|cingend|sert[uoia]',re.I)
STRONG=re.compile(r'(aure[ao]\s+coron|coron\w*\s+aure|(?:aureo|pretioso|sacro)\s+diademat|diademat\w*\s+(?:redim|coron|cing|orna)'
  r'|coron\w*\s+redim|redimit\w*\s+coron|coronand\w*\s+(?:imagin|simulacr|signum)|(?:imagin|simulacr)\w*\s+coronand'
  r'|coronat\w*\s+(?:imagin|simulacr)|(?:imagin|simulacr|signum)\w*\s+coronat|corona\w*\s+imposit|coronam\s+appon'
  r'|coron\w*\s+impon|capitul\w*\s+vatican|coronare\s+secundum|coronari\s+sinitur|redimiri\s+sinitur|diademate\s+cing'
  r'|coronasse\s+imagin|imagin\w*\s+coronass|nomine\s+et\s+auctoritate\s+summi|redimiend\w*\s+sert|sert[uo]\s+pretios'
  r'|pretioso\s+sert|redimiat\s+secundum|fit\s+potestas[^.]{0,60}redimi)',re.I)
IMG=re.compile(r'imag|simulacr|effigie|statua|icon\b|iconem|deipara|thaumaturg|signum\s+beat|signum\s+illud|marial',re.I)
NOISE=re.compile(r'quat[t]?uor\s+coronat|coronatio\s+summi\s+pontificis|montis\s+coronae|monte\s+corona|martyri\w*\s+coron'
  r'|coron\w*\s+martyri|laurea\s+coronat|coronat\w*\s+laurea|corona\s+marmorea|coronis\s+precatori|rosarii?\s+bened'
  r'|corona\s+pretiosissimi|coronae\s+septem|marialem\s+coronam|corona\s+stellarum|corona\s+circumdat|spine'
  r'|incoronazione\s+di\s+sua',re.I)
DATUM=re.compile(r'Datum\s+Romae|Datum\s+ex\s+Aedibus|die\s+[IVXLCDM]{1,12}\s+mensis',re.I)
out=[]
for path in sorted(glob.glob('txt/*.txt')):
    fn=os.path.basename(path)[:-4]
    if fn=='AAS-42-1950' or fn.startswith('AAS_Index'): continue
    vol,year,part=meta(fn)
    raw=open(path,encoding='utf-8',errors='replace').read()
    chunks=[]
    for c in raw.split('\f'):
        m=re.match(r'\[\[PDFPAGE (\d+)\]\]\n?',c)
        if m: chunks.append((int(m.group(1)),c[m.end():]))
    offs=collections.Counter()
    for p,b in chunks:
        n=re.findall(r'(?m)^\s*(\d{1,4})\s*$','\n'.join(b.split('\n')[:6]))
        if n: offs[p-int(n[0])]+=1
    off=offs.most_common(1)[0][0] if offs else 0
    # build char list with parallel page map, THEN de-hyphenate
    chars=[];pmap=[]
    for pdfp,b in chunks:
        chars.extend(b); pmap.extend([pdfp]*len(b))
    T0=''.join(chars)
    keep=[True]*len(T0)
    for m in re.finditer(r'[-‐‑]\s*\n\s*',T0):
        for i in range(m.start(),m.end()): keep[i]=False
    T=''.join(c for c,k in zip(T0,keep) if k)
    P=[p for p,k in zip(pmap,keep) if k]
    hits=[]
    for m in CORO.finditer(T):
        w=T[max(0,m.start()-500):m.end()+500]
        strong=bool(STRONG.search(w))
        if NOISE.search(w) and not strong: continue
        if not (strong or IMG.search(w)): continue
        # 'sertum' alone is very noisy: require STRONG
        if re.match(r'sert',m.group(0),re.I) and not strong: continue
        hits.append((m.start(),strong))
    hits.sort(); merged=[]
    for p,s in hits:
        if merged and p-merged[-1][1]<2000: merged[-1][1]=p; merged[-1][2]=merged[-1][2] or s
        else: merged.append([p,p,s])
    for a,b,s in merged:
        st=max(0,a-1800); en=min(len(T),b+4200)
        ctx=unspace(re.sub(r'[ \t]+',' ',T[st:en]))
        pg=P[a] if a<len(P) else 0
        out.append({'id':f"{fn}#{pg}",'file':fn,'volume':vol,'year':year,'part':part,
            'pdf_page':pg,'printed_page':pg-off,'strong':s,
            'has_datum':bool(DATUM.search(ctx)),'context':ctx})
json.dump(out,open('passages2.json','w'),ensure_ascii=False,indent=1)
print('passages (de-hyphenated):',len(out),'| strong:',sum(1 for x in out if x['strong']))
old={(p['file'],p['printed_page']) for p in json.load(open('passages.json'))}
new=[p for p in out if (p['file'],p['printed_page']) not in old]
json.dump(new,open('passages_new.json','w'),ensure_ascii=False,indent=1)
print('NEW passages not in first sweep:',len(new),'| strong:',sum(1 for x in new if x['strong']))
print('new by decade:',sorted(collections.Counter((x['year']//10)*10 for x in new).items()))
