# -*- coding: utf-8 -*-
# Regera ../index.html a partir do template e dos dados.
# Uso: python3 continuar/rebuild.py "https://swipealquimia.imanto.com.br/api"
# Sem argumento, o site funciona sem login (curtidas só no navegador).
import json,sys,os
AQUI=os.path.dirname(os.path.abspath(__file__)); RAIZ=os.path.dirname(AQUI)
API=sys.argv[1] if len(sys.argv)>1 else ''
L=lambda n: json.load(open(os.path.join(AQUI,'dados',n)))
cri=L('criativos_site.json'); prod=L('produtores.json'); fmt=L('formatos.json'); tst=L('testar.json')
fn={f['id']:f['nome'] for f in fmt}
for c in cri: c['formato_nome']=fn.get(c['formato'],c['formato'])
rank={'FORTE':0,'MODERADA':1,'LIMITADA':2}
cri.sort(key=lambda c:(0 if c.get('grupo')=='Relacionamento' else 1,0 if c.get('destaque') else 1,rank.get(c['evidencia'],3),c['produtor']))
stats=dict(criativos=len(cri),estaticos=sum(1 for c in cri if c['tipo']=='Estático'),videos=sum(1 for c in cri if c['tipo']=='Vídeo'),
  destaques=sum(1 for c in cri if c.get('destaque')),relacionamento=sum(1 for c in cri if c.get('grupo')=='Relacionamento'),
  produtores=len(prod),formatos=len(fmt),paises=5,nichos=len(set(c['nicho'] for c in cri)),data='17/09/2026')
html=open(os.path.join(AQUI,'template.html')).read().replace('__API__',API).replace('__DATA__',json.dumps(dict(criativos=cri,produtores=prod,formatos=fmt,testar=tst,stats=stats),ensure_ascii=False))
html=html.replace('<meta charset="utf-8">','<meta charset="utf-8"><meta name="robots" content="noindex,nofollow">',1)
html=html.replace('Coleta: <b id="dt"></b> na Meta Ad Library.','Coleta: <b id="dt"></b> na Meta Ad Library. %d vídeos tocam aqui mesmo; os demais abrem na Ad Library.'%sum(1 for c in cri if c.get('video')))
open(os.path.join(RAIZ,'index.html'),'w').write(html)
print('index.html gerado |',len(cri),'criativos | API:',API or '(sem login)')
