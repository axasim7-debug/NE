#!/usr/bin/env bash
# Re-download all official Kohberger documents (PDFs are git-ignored; extracted text IS in git).
# Usage: tools/fetch_kohberger_docs.sh   (from repo root)   needs: curl, python3, pdftotext (poppler)
set -euo pipefail
P=projects/2026-11-idaho-kohberger/docs_raw; mkdir -p $P/mpd $P/court/files $P/court/files_latah
for id in 34071 34072 34073 34074 34075 34076 34077; do
  curl -sSL -A "Mozilla/5.0" -o $P/MPD_$id.zip "https://www.ci.moscow.id.us/DocumentCenter/View/$id"
  python3 -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" $P/MPD_$id.zip $P/mpd/MPD_$id
done
curl -sS -A "Mozilla/5.0" -o $P/court/index.html https://coi.isc.idaho.gov/docs/Cases/CR01-24-31665.html
python3 - "$P/court" <<'PY'
import re,sys
d=sys.argv[1]; t=open(d+'/index.html',encoding='utf8',errors='ignore').read()
a=sorted(set(re.findall(r'https://coi\.isc\.idaho\.gov/docs/CR01-24-31665/[^"\' ]+',t)))
b=set(re.findall(r'https://coi\.isc\.idaho\.gov/docs/CR29-22-2805/[^"\' ]+',t))|{'https://coi.isc.idaho.gov'+x for x in re.findall(r'"(/docs/CR29-22-2805/[^"]+)"',t)}
open(d+'/links.txt','w').write('\n'.join(a)+'\n'); open(d+'/links_latah.txt','w').write('\n'.join(sorted(b))+'\n')
PY
dl(){ while read -r u; do f="$2/$(echo "$u" | sed 's#https://coi.isc.idaho.gov/docs/##; s#/#__#g; s#+#_#g')"; [ -s "$f" ] || curl -sS -A "Mozilla/5.0" -o "$f" "$u"; done < "$1"; }
dl $P/court/links.txt $P/court/files; dl $P/court/links_latah.txt $P/court/files_latah
echo "done. Text versions already in git: $P/mpd_txt, $P/court/txt, $P/court/txt_latah"
