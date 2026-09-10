import re,glob,os,json,collections
def unspace(s): return re.sub(r'(?:\b[A-Z] ){2,}[A-Z]\b', lambda m: m.group(0).replace(' ',''), s)
def meta(fn):
    m=re.match(r'AAS-(\d+)(?:-(I{1,2}))?-(\d{4})(?:-(I{1,2}))?-ocr',fn)
    if m: return int(m.group(1)),int(m.group(3))
    m=re.match(r'(\d{4})_',fn)
    if m: return int(m.group(1))-1908,int(m.group(1))
    return None,None
VERN=re.compile(r'coronaci[oó]n|coronazion|incoronazion|couronnement|couronn\w*\s+(?:de\s+la\s+)?(?:vierge|image|statue)|koronacj|kr[oö]nung|coroa[çc][aã]o|coronaç',re.I)
IMG=re.compile(r'imagen|imagine|imago|imagin|simulacr|statua|statue|estatua|virgen|vergine|vierge|madonna|nuestra|senora|señora|notre[- ]dame|obraz|matki|marii|santuario|sanctuaire|effigie|icon',re.I)
NOISE=re.compile(r'coronazione\s+(?:del|di)\s+(?:sua\s+santit|s\.\s*s\.|pontefice|papa|giovanni|paolo|pio|benedetto)|papal\s+coronation|coronation\s+of\s+(?:his|the)\s+(?:holiness|pope|king|queen)|incoronazione\s+di\s+sua\s+maest|coronaci[oó]n\s+(?:del|de\s+su\s+santidad)|kr[oö]nung\s+(?:des\s+papstes|seiner)',re.I)
out=[]
for path in sorted(glob.glob('txt/*.txt')):
    fn=os.path.basename(path)[:-4]
    if fn=='AAS-42-1950' or fn.startswith('AAS_Index'): continue
    vol,year=meta(fn)
    raw=open(path,encoding='utf-8',errors='replace').read()
    chunks=[]
    for c in raw.split('\f'):
        m=re.match(r'\[\[PDFPAGE (\d+)\]\]\n?',c)
        if m: chunks.append((int(m.group(1)),c[m.end():]))
    offs=collections.Counter()
    for pdfp,b in chunks:
        n=re.findall(r'(?m)^\s*(\d{1,4})\s*$','\n'.join(b.split('\n')[:6]))
        if n: offs[pdfp-int(n[0])]+=1
    off=offs.most_common(1)[0][0] if offs else 0
    full=[];idx=[]
    for pdfp,b in chunks:
        idx.append((sum(len(x) for x in full),pdfp)); full.append(b)
    T=''.join(full)
    def page_at(p):
        lo=idx[0][1] if idx else 0
        for st,pg in idx:
            if st<=p: lo=pg
            else: break
        return lo
    hits=[]
    for m in VERN.finditer(T):
        w=T[max(0,m.start()-600):m.end()+600]
        if NOISE.search(w): continue
        if not IMG.search(w): continue
        hits.append(m.start())
    hits.sort(); merged=[]
    for h in hits:
        if merged and h-merged[-1][1]<2000: merged[-1][1]=h
        else: merged.append([h,h])
    for a,b in merged:
        ctx=unspace(re.sub(r'[ \t]+',' ',T[max(0,a-1800):min(len(T),b+3500)]))
        out.append({'id':f"{fn}#v{page_at(a)}",'file':fn,'volume':vol,'year':year,
            'pdf_page':page_at(a),'printed_page':page_at(a)-off,'strong':False,'context':ctx})
json.dump(out,open('vern_passages.json','w'),ensure_ascii=False,indent=1)
print('vernacular passages:',len(out))
import collections as C
print('by decade:',sorted(C.Counter((x['year']//10)*10 for x in out).items()))
