import json,sys,os,subprocess,hashlib
# uso: thumbs.py <raw.json> <destdir>
f,dest=sys.argv[1],sys.argv[2]
os.makedirs(dest,exist_ok=True)
cards=json.load(open(f)); ok=0; skip=0
for c in cards:
    th=c.get('thumbs') or []
    if not th: continue
    p=os.path.join(dest,f"{c['id']}.jpg")
    if os.path.exists(p) and os.path.getsize(p)>2000: skip+=1; continue
    r=subprocess.run(['curl','-sL','--max-time','25','-o',p,th[0]],capture_output=True)
    if os.path.exists(p) and os.path.getsize(p)>2000: ok+=1
    else:
        if os.path.exists(p): os.remove(p)
print(f"{f}: baixadas {ok}, já existiam {skip}, total cards {len(cards)}")
