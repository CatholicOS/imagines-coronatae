import fitz, sys, os, pathlib
src=pathlib.Path(sys.argv[1]); dst=pathlib.Path('txt')/(src.stem+'.txt')
if dst.exists() and dst.stat().st_size>0: print('SKIP',src.name); sys.exit()
try:
    d=fitz.open(src)
    with open(dst,'w',encoding='utf-8') as f:
        for i,p in enumerate(d):
            f.write('\f[[PDFPAGE %d]]\n'%(i+1)); f.write(p.get_text())
    print('OK',src.name,d.page_count)
except Exception as e:
    print('ERR',src.name,e)
