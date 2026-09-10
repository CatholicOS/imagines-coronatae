#!/usr/bin/env bash
# Download every AAS volume PDF listed on vatican.va, then verify each against Content-Length.
set -euo pipefail
OUT="${1:-pdf}"; mkdir -p "$OUT"
INDEX="https://www.vatican.va/archive/aas/index_sp.htm"

curl -sL "$INDEX" -o aas_index.html

python3 - <<'PY'
import re,urllib.parse
h=open('aas_index.html',encoding='iso-8859-1').read()
docs=sorted(set(re.findall(r'href="(documents/[^"]+)"',h,re.I)))
with open('urls.tsv','w') as f:
    for d in docs:
        url='https://www.vatican.va/archive/aas/'+d
        name=urllib.parse.unquote(d[len('documents/'):]).replace('/','_').replace(' ','_')
        if not name.lower().endswith('.pdf'): name+='.pdf'
        f.write(f"{url}\t{name}\n")
print('listed',len(docs),'documents')
PY

# Download with resume; some volumes are very large (one is ~304 MB) and get truncated.
cat urls.tsv | xargs -P 8 -n 1 -d '\n' bash -c '
u=$(echo "$0"|cut -f1); n=$(echo "$0"|cut -f2)
for try in 1 2 3 4 5 6 7 8; do
  curl -sL --max-time 900 -C - "$u" -o "'"$OUT"'/$n" 2>/dev/null || true
  r=$(curl -sIL --max-time 60 "$u" | grep -i "^content-length" | tail -1 | tr -d "\r" | awk "{print \$2}")
  l=$(stat -c%s "'"$OUT"'/$n" 2>/dev/null || echo 0)
  [ "$r" = "$l" ] && { echo "OK $n $l"; exit 0; }
done
echo "INCOMPLETE $n"
'

echo "--- verifying ---"
cat urls.tsv | xargs -P 10 -n 1 -d '\n' bash -c '
u=$(echo "$0"|cut -f1); n=$(echo "$0"|cut -f2)
r=$(curl -sIL --max-time 60 "$u" | grep -i "^content-length" | tail -1 | tr -d "\r" | awk "{print \$2}")
l=$(stat -c%s "'"$OUT"'/$n" 2>/dev/null || echo 0)
[ "$r" != "$l" ] && echo "MISMATCH $n remote=$r local=$l"
' || true
echo "done"
