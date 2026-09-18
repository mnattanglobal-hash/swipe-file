# -*- coding: utf-8 -*-
# Monta o catálogo final a partir de dados/cards_all.json + dados/mapa_anunciantes.json.
# Regra do recorte: só criativo de VENDA. Destino aceito: página de vendas, checkout, VSL ou quiz.
# Descarta isca grátis (ebook/aula/workshop gratuito), captura de lead, perfil social e app.
import json,glob,os,re,collections
cards=json.load(open('dados/cards_all.json'))
prods=[]
for f in ['dados/produtores_parte1.json','dados/produtores_parte2.json','dados/produtores_parte3.json']:
    prods+=json.load(open(f))
json.dump(prods,open('dados/produtores.json','w'),ensure_ascii=False,indent=1)
M=json.load(open('dados/mapa_anunciantes.json'))

SOCIAL=re.compile(r'(instagram\.com|api\.whatsapp|wa\.me|play\.google|youtube\.com|itunes|apps\.apple|linktr)',re.I)
CHECKOUT=re.compile(r'(pay\.|p\.pagtrust|checkout|kiwify|hotmart|lastlink|wiapy|monetizze|braip|eduzz|ticto|cakto|perfectpay|kirvano)',re.I)
QUIZ=re.compile(r'(quiz|/test|teste)',re.I)
VSLD=re.compile(r'(/vsl|/video|/vídeo|/aula-|/assista)',re.I)
ISCA_TXT=re.compile(r'(aula (é )?gratuita|aula gratuita|masterclass gratuita|e-?book gratuito|livro eletr[ôo]nico gratuito|material gratuito|baixe gr[áa]tis|baixar gr[áa]tis|download gr[áa]tis|inscreva-se gratu|gratuitamente no link|free (e-?book|guide|training|workshop|masterclass|class|pdf|download))',re.I)
ISCA_URL=re.compile(r'(/aula$|/aula/|/aula\?|webinar|inscricao|inscrição|cadastro|lead|captura|signup|sign-up|register|masterclass-signup)',re.I)

def tipo_destino(dest,copy):
    d=dest or ''; t=copy or ''
    if ISCA_TXT.search(t) or ISCA_URL.search(d): return 'ISCA'
    if CHECKOUT.search(d): return 'CHECKOUT'
    if QUIZ.search(d): return 'QUIZ'
    if VSLD.search(d): return 'VSL'
    return 'PAGINA DE VENDAS'

def thumb(cid):
    for p in glob.glob('referencias/*/*/%s.jpg'%cid): return p
    return ''
def video_local(cid):
    p='videos/%s.mp4'%cid
    return p if os.path.exists(p) else ''

out=[]; descartes=collections.Counter()
for c in cards:
    key=None
    for k in M:
        if c['advertiser'].startswith(k): key=k; break
    if not key: continue
    m=M[key]
    if m.get('excluir'): descartes['produtor fora do recorte: '+key]+=1; continue
    if m.get('dest_filtro') and m['dest_filtro'] not in (c['dest'] or ''):
        descartes['destino fora da oferta mapeada: '+key]+=1; continue
    if SOCIAL.search(c['dest'] or ''): descartes['destino social/app']+=1; continue
    t=thumb(c['id'])
    if not t: descartes['sem imagem salva']+=1; continue
    td=tipo_destino(c['dest'],c['copy'])
    if td=='ISCA': descartes['isca grátis / captura de lead']+=1; continue
    out.append(dict(id=c['id'],produtor=m['produtor'],produtor_id=m['produtor_id'],expert=m.get('expert',''),
      pais=m['pais'],nicho=m['nicho'],grupo=m.get('grupo','Outro nicho (só o formato)'),oferta=m['oferta'],
      preco=m['preco'],faixa=m['faixa'],plataforma=m.get('plataforma',''),evidencia=m['evidencia'],
      tipo='Vídeo' if c['media']=='video' else 'Estático',
      formato=m['formato_video'] if c['media']=='video' else m['formato_img'],
      destino_tipo=td,dor=m['dor'],desejo=m['desejo'],angulo=m['angulo'],aplicabilidade=m['aplicabilidade'],
      data_inicio=c['start'],data_observacao='2026-09-17',duracao=c['dur'],variacoes=c['variants'],
      thumb=t,video=video_local(c['id']),video_url=c.get('video',''),
      lib_url=c['lib_url'],destino=c['dest'],copy=c['copy'],
      hook=(c['copy'].split('\n')[0][:160] if c['copy'] else ''),destaque=False,analise_manual=False))
json.dump(out,open('dados/criativos_auto.json','w'),ensure_ascii=False,indent=1)
print(len(out),'criativos no catálogo |',collections.Counter(x['tipo'] for x in out))
print('por tipo de destino:',dict(collections.Counter(x['destino_tipo'] for x in out)))
print('descartes:',dict(descartes))
