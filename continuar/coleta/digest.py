import json,sys,re,collections,datetime
MES={'jan':1,'fev':2,'mar':3,'abr':4,'mai':5,'jun':6,'jul':7,'ago':8,'set':9,'out':10,'nov':11,'dez':12}
def d(s):
    m=re.match(r'(\d+) de (\w+)\.? de (\d+)',s or '')
    return datetime.date(int(m.group(3)),MES[m.group(2)[:3]],int(m.group(1))) if m else None
def load(f):
    raw=json.load(open(f)); out=[]
    for c in raw:
        t=c['text']; lines=[l for l in t.split('\n') if l.strip() and l.strip()!='​']
        adv=''; body=''
        if 'Patrocinado' in lines:
            i=lines.index('Patrocinado'); adv=lines[i-1] if i>0 else ''; body=' '.join(lines[i+1:])
        dur=re.search(r'0:00 / (\d+:\d+)',body); body=re.sub(r'0:00 / \d+:\d+','',body)
        out.append(dict(id=c['id'],adv=adv,start=c['start'],sd=d(c['start']),var=c.get('variants',''),
             media=c.get('media',''),dur=dur.group(1) if dur else '',dest=c.get('dest',''),copy=body.strip(),thumbs=c.get('thumbs',[])))
    return out
if __name__=='__main__':
    cards=[]
    for f in sys.argv[1:]: cards+=load(f)
    g=collections.defaultdict(list)
    for c in cards: g[re.sub(r'\s+',' ',c['copy'])[:90]].append(c)
    print(f"TOTAL {len(cards)} cards / {len(g)} copies distintas")
    for k,v in sorted(g.items(),key=lambda kv:-len(kv[1])):
        ds=[x['sd'] for x in v if x['sd']]
        rng=f"{min(ds)}→{max(ds)}" if ds else '?'
        med=collections.Counter(x['media'] for x in v)
        durs=sorted(set(x['dur'] for x in v if x['dur']))
        dest=set(re.sub(r'https?://','',x['dest']).split('/')[0] for x in v if x['dest'])
        print(f"\n[{len(v)}x] {rng} {dict(med)} dur:{','.join(durs[:4])} → {';'.join(list(dest)[:2])}")
        print(f"  {v[0]['id']} :: {k}")
