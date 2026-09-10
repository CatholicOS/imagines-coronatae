import re,glob,os,json,collections
# Reproduce the ORIGINAL filters, then find matches they rejected that carry a
# devotional TITLE nearby (Nuestra Senora / Notre-Dame / Madonna / Matka Boza / Our Lady...)
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
# devotional title markers, incl. vernacular
TITLE=re.compile(r'nuestra\s+se[nñ]ora|notre[- ]dame|our\s+lady|madonna\s+d|matka\s+bo[zż]|panna\s+maria|nossa\s+senhora'
  r'|beata\s+maria\s+virg|b\.\s*m\.\s*v|virgen\s+de|vergine\s+d|domina\s+nostra|dominae\s+nostrae|santo\s+ni[nñ]o'
  r'|sacratissim\w+\s+cord|sagrado\s+coraz|santissima\s+vergine',re.I)
EXTRA=re.compile(r'martyri|laurea|rosari|corona\s+de\s+espinas|spine|tiara|conclav',re.I)
rows=[]
for f in sorted(glob.glob('txt/*.txt'))+sorted(glob.glob('ass_txt/*.txt')):
    fn=os.path.basename(f)[:-4]
    if fn.startswith('AAS_Index') or fn=='AAS-42-1950': continue
    t=open(f,encoding='utf-8',errors='replace').read()
    t=re.sub(r'[-‐‑]\s*\n\s*','',t)
    chunks=[]
    for c in t.split('\f'):
        m=re.match(r'\[\[PDFPAGE (\d+)\]\]\n?',c)
        if m: chunks.append((int(m.group(1)),c[m.end():]))
    for pg,b in chunks:
        for m in CORO.finditer(b):
            w=b[max(0,m.start()-500):m.end()+500]
            strong=bool(STRONG.search(w))
            accepted = (not (NOISE.search(w) and not strong)) and (strong or IMG.search(w))
            if accepted: continue                      # original pipeline already had it
            if not TITLE.search(w): continue           # needs a devotional title nearby
            if EXTRA.search(w): continue               # obvious noise
            rows.append({'file':fn,'page':pg,'snippet':re.sub(r'\s+',' ',w)})
seen=set();ded=[]
for r in rows:
    k=(r['file'],r['page'])
    if k in seen: continue
    seen.add(k); ded.append(r)
json.dump(ded,open('gap_candidates.json','w'),ensure_ascii=False,indent=1)
print('pages rejected by the original filter but carrying a devotional title:',len(ded))
print('by series:',collections.Counter('ASS' if r['file'].startswith('ASS') else 'AAS' for r in ded))
