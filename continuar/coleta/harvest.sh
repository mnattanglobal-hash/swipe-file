#!/bin/zsh
# uso: harvest.sh <slug> <url> [n_scrolls] [session]
SLUG="$1"; URL="$2"; N="${3:-6}"; export AGENT_BROWSER_SESSION="${4:-s1}"
DIR="${SWIPE_DIR:-$(cd "$(dirname "$0")" && pwd)}"
mkdir -p "$DIR/dados/raw"
agent-browser open "$URL" >/dev/null 2>&1
agent-browser wait --load networkidle >/dev/null 2>&1
for i in $(seq 1 $N); do
  agent-browser scroll down 4000 >/dev/null 2>&1
  agent-browser wait 1500 >/dev/null 2>&1
done
agent-browser eval "$(cat $DIR/extract.js)" > "$DIR/dados/raw/$SLUG.rawjson" 2>&1
python3 - "$DIR/dados/raw/$SLUG.rawjson" <<'PY'
import json,sys
p=sys.argv[1]; s=open(p).read().strip()
try: data=json.loads(json.loads(s)) if s.startswith('"') else json.loads(s)
except Exception as e: print("PARSE FAIL",p,e,s[:150]); sys.exit()
json.dump(data,open(p.replace('.rawjson','.json'),'w'),ensure_ascii=False,indent=1)
print(f"{len(data)} cards -> {p.split('/')[-1].replace('.rawjson','.json')}")
PY
