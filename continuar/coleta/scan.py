import json,sys,re,collections
dom=re.compile(r'\n([A-Z0-9][A-Z0-9\.\-]+\.(?:COM|COM\.BR|BR|NET|IO|ME|APP|SITE|SHOP|ONLINE|CO|LINK|STORE|CLICK|FUN|XYZ|ORG|PRO|INFO|DIGITAL|LIVE))\n')
SKIP=re.compile(r'(WHATSAPP|INSTAGRAM\.COM|PLAY\.GOOGLE|AMAZON|FACEBOOK)')
n=int(sys.argv[1]); per=collections.defaultdict(list)
for f in sys.argv[2:]:
    for c in json.load(open(f)):
        t=c['text']; lines=[l for l in t.split('\n') if l.strip() and l.strip()!='​']
        adv=''; body=''
        if 'Patrocinado' in lines:
            i=lines.index('Patrocinado'); adv=lines[i-1] if i>0 else ''; body=' '.join(lines[i+1:])
        d=[x for x in set(dom.findall(t)) if not SKIP.search(x)]
        per[adv].append((c['id'],c['start'],c['variants'],('VID' if c.get('media')=='video' else 'IMG'),'|'.join(d),body))
for adv,items in sorted(per.items(), key=lambda kv:-len(kv[1])):
    doms=set(x[4] for x in items if x[4])
    print(f"### {adv} ({len(items)} ads) {';'.join(doms)}")
    for it in items[:n]:
        print(f"  [{it[0]}] {it[1]} var:{it[2]} {it[3]} :: {it[5][:130]}")
