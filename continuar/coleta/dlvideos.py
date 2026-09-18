# -*- coding: utf-8 -*-
# Baixa os vídeos dos criativos catalogados (URL da fbcdn expira, por isso salvamos local).
import json,os,subprocess,sys,concurrent.futures as cf
os.makedirs('videos',exist_ok=True)
cards={c['id']:c for c in json.load(open('dados/cards_all.json'))}
alvo=[c for c in json.load(open('dados/criativos.json')) if c['tipo']=='Vídeo']
def baixar(c):
    cid=c['id']; dst='videos/%s.mp4'%cid
    if os.path.exists(dst) and os.path.getsize(dst)>50000: return 'ok-existente'
    url=(cards.get(cid) or {}).get('video') or c.get('video_url') or ''
    if not url: return 'sem-url'
    r=subprocess.run(['curl','-sL','--max-time','90','-o',dst,url],capture_output=True)
    if os.path.exists(dst) and os.path.getsize(dst)>50000: return 'ok'
    if os.path.exists(dst): os.remove(dst)
    return 'falhou'
res={}
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    for c,r in zip(alvo,ex.map(baixar,alvo)): res[r]=res.get(r,0)+1
print('vídeos:',res)
print('total em disco:',len(os.listdir('videos')),'arquivos',round(sum(os.path.getsize('videos/'+f) for f in os.listdir('videos'))/1e6,1),'MB')
