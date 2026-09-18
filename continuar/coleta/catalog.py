import json,glob,re,os,collections,datetime,sys
MES={'jan':1,'fev':2,'mar':3,'abr':4,'mai':5,'jun':6,'jul':7,'ago':8,'set':9,'out':10,'nov':11,'dez':12}
SOCIAL=re.compile(r'(instagram\.com|api\.whatsapp|wa\.me|facebook\.com|play\.google|itunes\.apple|apps\.apple|youtube\.com|linktr)',re.I)
def pdate(s):
    m=re.match(r'(\d+) de (\w+)\.? de (\d+)',s or '')
    return f"{m.group(3)}-{MES[m.group(2)[:3]]:02d}-{int(m.group(1)):02d}" if m else ''
cards={}
# preserva o que já foi coletado antes (a Ad Library muda a cada consulta)
if os.path.exists('dados/cards_all.json'):
    for c in json.load(open('dados/cards_all.json')): cards[c['id']]=c
for f in sorted(glob.glob('dados/raw/*.json')):
    src=os.path.basename(f)[:-5]
    try: raw=json.load(open(f))
    except: continue
    for c in raw:
        t=c['text']; lines=[l for l in t.split('\n') if l.strip() and l.strip()!='​']
        adv=''; body=''
        if 'Patrocinado' in lines:
            i=lines.index('Patrocinado'); adv=lines[i-1] if i>0 else ''; body='\n'.join(lines[i+1:])
        dur=re.search(r'0:00 / (\d+:\d+)',body)
        body=re.sub(r'0:00 / \d+:\d+','',body).strip()
        # remove trailing link block noise
        cid=c['id']
        if 'media' not in c:  # formato antigo do extractor
            vids=c.get('vids') or []; imgs=c.get('imgs') or []
            thumbs=[v['poster'] for v in vids if isinstance(v,dict) and v.get('poster')] or imgs[:2]
            links=[l for l in (c.get('links') or [])]
            def _clean(h):
                m=re.search(r'l\.facebook\.com/l\.php\?u=([^&]+)',h)
                import urllib.parse
                return urllib.parse.unquote(m.group(1)) if m else h
            links=[_clean(l) for l in links]
            c['media']='video' if vids else ('image' if imgs else '')
            c['thumbs']=thumbs
            c['dest']=next((l for l in links if 'facebook.com' not in l),'')
            c['page']=next((l for l in links if 'facebook.com' in l),'')
        rec=dict(id=cid,advertiser=adv,start=pdate(c['start']),start_raw=c['start'],video=c.get('video',''),
                 variants=c.get('variants',''),media=c.get('media',''),dur=dur.group(1) if dur else '',
                 dest=c.get('dest',''),page=c.get('page',''),copy=body,thumbs=c.get('thumbs',[]),
                 lib_url=f"https://www.facebook.com/ads/library/?id={cid}",sources=[src])
        if cid in cards:
            old=cards[cid]
            old['sources']=sorted(set(old.get('sources',[])+[src]))
            if not old.get('copy') and body: old['copy']=body
            if c.get('video') and not old.get('video'): old['video']=c['video']
            if not old.get('dest') and rec['dest']: old['dest']=rec['dest']
            if not old.get('thumbs') and rec['thumbs']: old['thumbs']=rec['thumbs']
        else: cards[cid]=rec
json.dump(list(cards.values()),open('dados/cards_all.json','w'),ensure_ascii=False,indent=1)
adv=collections.defaultdict(list)
for c in cards.values(): adv[c['advertiser']].append(c)
print(f"TOTAL cards únicos: {len(cards)} | anunciantes: {len(adv)}")
if '--cand' in sys.argv:
    rows=[]
    for a,v in adv.items():
        dests=[re.sub(r'^https?://','',x['dest']).split('/')[0] for x in v if x['dest'] and not SOCIAL.search(x['dest'])]
        if not dests: continue
        ds=sorted(set(dests),key=lambda d:-dests.count(d))
        st=[x['start'] for x in v if x['start']]
        rows.append((len(v),a,ds[:2],min(st) if st else '',sum(1 for x in v if x['media']=='image')))
    for n,a,ds,mn,im in sorted(rows,reverse=True):
        if n>=2: print(f"{n:4d} ads (img:{im:3d}) desde {mn} | {a[:38]:38s} | {';'.join(ds)}")
