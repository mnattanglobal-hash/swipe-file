# Continuar: swipe file com login da equipe em swipealquimia.imanto.com.br

Documento de passagem entre sessões do Claude Code. Quem está lendo é o agente que vai continuar o trabalho num computador com acesso ao GitHub e à VPS da Imanto.

## Estado atual (18/09/2026)

- Este repositório (`mnattanglobal-hash/swipe-file`) já contém o site estático completo e funcionando no GitHub Pages: https://mnattanglobal-hash.github.io/swipe-file/
- `index.html` é uma página única com os dados embutidos. `img/` tem 964 imagens (uma por criativo, nome = ID da Meta Ad Library) e `vid/` tem 446 vídeos MP4 comprimidos. Total de ~730 MB.
- O front já tem as curtidas (coração em cada card, filtro "meus curtidos", link de seleção) e já tem a **camada de login pronta**, desligada. Ela liga quando a constante `API` recebe uma URL.
- Hoje, sem API, as curtidas ficam só no `localStorage` do navegador. **É isso que precisa mudar.**

## Objetivo

A equipe (matheus, aline, anki) precisa selecionar os melhores criativos no próprio site e ter isso salvo **independente de sessão, navegador ou computador**. Ninguém da equipe usa Claude, então nada pode depender do claude.ai.

Critério de pronto:
1. O site abre em `https://swipealquimia.imanto.com.br` com HTTPS válido.
2. Cada pessoa entra com usuário e senha próprios.
3. O que cada pessoa curte fica salvo no servidor: saiu, entrou de outro navegador, está lá.
4. Todos veem o que os outros escolheram (chips com a inicial de quem curtiu, filtro "seleção da equipe", filtro "de aline" etc.).
5. As 964 imagens e os 446 vídeos carregam e tocam.

## O que fazer

1. **Hospedar o estático na VPS da Imanto.** Clonar este repositório na VPS e servir a raiz dele no subdomínio `swipealquimia.imanto.com.br`, usando o servidor web que já existe lá (nginx, Caddy ou o que estiver em uso). Não mexer na configuração dos outros sites da VPS além de adicionar este.
2. **DNS.** Criar o registro A (ou CNAME) de `swipealquimia` apontando para a VPS, onde quer que o DNS de `imanto.com.br` esteja gerenciado. Se não houver acesso, pedir ao Matheus.
3. **HTTPS.** Certificado válido para o subdomínio (Let's Encrypt/certbot ou o automático do Caddy).
4. **Backend pequeno em `/api`** no mesmo domínio (sem CORS para resolver). Qualquer stack simples serve (Node, Python/FastAPI, etc.), com SQLite ou arquivo JSON em disco e processo gerenciado (systemd, pm2 ou docker, o que a VPS já usa). O contrato está abaixo e **precisa ser seguido exatamente**, porque o front já está escrito para ele.
5. **Usuários.** Criar `matheus`, `aline` e `anki`, cada um com senha aleatória forte, guardada com hash (bcrypt/argon2 ou sha256 com salt). **Nunca mostrar as senhas no chat**: gravar num arquivo local fora de qualquer repositório (ou no 1Password, se o Matheus pedir) e dizer ao Matheus onde está.
6. **Ligar o login no front:** `python3 continuar/rebuild.py "https://swipealquimia.imanto.com.br/api"` regera o `index.html` com a API. Publicar o `index.html` novo na VPS.
7. **Testar de verdade:** entrar com um usuário, curtir 3 criativos, abrir em outro navegador (ou aba anônima), entrar de novo e confirmar que os 3 estão lá; entrar com outro usuário e confirmar que ele vê as escolhas do primeiro nos chips e no filtro "seleção da equipe".
8. Opcional, depois de validar: decidir com o Matheus se o GitHub Pages continua no ar ou sai.

## Fase 2: atualização automática, novidades e reciclagem de mídia

Pedido do Matheus: o sistema na Imanto tem que se renovar sozinho. Fazer depois que a fase 1 (login e seleção salva) estiver validada.

### O que precisa acontecer

1. **Coleta recorrente.** Rodar a coleta na Meta Ad Library de forma agendada, uma vez por semana como padrão (configurável para diária), com cron ou systemd timer na VPS. A coleta revisita os produtores já mapeados e as buscas de descoberta, baixa imagem e vídeo dos anúncios novos e atualiza o catálogo.
2. **Novidades em destaque.** Todo criativo tem a data em que foi visto pela primeira vez (`primeira_observacao`). O site ganha uma aba ou faixa **"Novidades"** no topo com o que entrou na última coleta, e um selo "novo" nos cards por 7 dias (ou até a coleta seguinte). O `start` da Ad Library é a data de início do anúncio, não a data em que a gente o encontrou: usar os dois campos separados.
3. **Continua valendo o recorte:** só criativo de venda (página de vendas, checkout, VSL ou quiz). Isca grátis, aula gratuita, captura de lead, perfil social e app ficam fora. A regra já está em `coleta/build_criativos.py`, e o que ela bloqueia está documentado no README original.
4. **Reciclagem de mídia.** Para a VPS não encher:
   - Criativo **selecionado por alguém da equipe** nunca perde a mídia.
   - Criativo **não selecionado** perde a mídia (imagem grande e vídeo) depois de um prazo, por exemplo 30 dias após a primeira observação. Proponha o prazo ao Matheus antes de ligar.
   - Ao apagar a mídia, manter um registro leve: ID, produtor, copy, links e uma miniatura pequena, para o histórico não sumir. Isso também evita baixar de novo algo que já foi descartado.
   - Criativo que sumiu da Ad Library (parou de rodar) e não foi selecionado pode sair do catálogo principal e ir para um "arquivo".
   - Mostrar no site, para o Matheus, quanto espaço a mídia está ocupando e quanto a última reciclagem liberou.
   - A limpeza apaga arquivos: rodar primeiro em modo simulação, mostrar ao Matheus o que seria apagado e só então ligar o automático.
5. **Seleção da equipe manda na retenção.** O backend da fase 1 precisa expor para o job de limpeza a lista de IDs selecionados por qualquer usuário.

### Ferramentas de coleta (pasta `continuar/coleta/`)

Pipeline usado na coleta original, validado em 17/09/2026:
- `harvest.sh <slug> <url> <scrolls> <sessão>`: abre a Ad Library com o `agent-browser` (Chrome headless), rola a página e roda `extract.js`, que extrai cada card (ID, data de início, nº de anúncios com o mesmo criativo, copy, destino, thumbnail, URL do vídeo). Na VPS vai precisar do `agent-browser` e do Chrome instalados (`npm i -g agent-browser && agent-browser install --with-deps`).
- `byname.sh <slug> "<nome da página>" <scrolls> <sessão> <país>`: deep dive de um anunciante (usa `search_type=page`, não precisa de page_id).
- `deepdive.sh`: o mesmo, por page_id.
- `catalog.py`: consolida `dados/raw/*.json` em `dados/cards_all.json` **acumulando** (nunca sobrescreve o que já foi coletado). A base histórica completa está em `coleta/dados/cards_all.json.gz`.
- `build_criativos.py`: aplica o recorte de venda e o mapa de anunciantes (`dados/mapa_anunciantes.json`) e gera o catálogo final.
- `thumbs.py` e `dlvideos.py`: baixam imagem e vídeo. As URLs da Meta (fbcdn) expiram em poucos dias, então o download precisa acontecer logo depois da coleta.
- `digest.py` e `scan.py`: relatórios de apoio (agrupar por copy, por anunciante).
- `dados/`: mapa de anunciantes, dossiês de produtores (`produtores_parte*.json`) e as 50 fichas de análise manual (`destaques_*.json`; 47 seguem no catálogo depois do corte de isca grátis).

Os scripts vieram de um Mac. Ajuste caminhos e o que for preciso para Linux. Rodar no máximo 3 sessões de navegador em paralelo: com 5 a Ad Library começa a devolver página vazia. A busca por palavra-chave da Meta funciona como OR entre os termos, então termo genérico traz muito ruído.

Anunciante novo que aparecer nas buscas de descoberta só entra no catálogo depois de mapeado em `mapa_anunciantes.json`. Proponha ao Matheus uma forma simples de revisar os candidatos novos: por exemplo, uma lista "anunciantes descobertos esta semana" no próprio site, com botão para aprovar.

## Contrato da API (o front já chama exatamente isto)

Uma única rota: `POST /api`. Corpo em JSON (o front envia com `fetch(API,{method:'POST',body:JSON.stringify(...)})`, então o `Content-Type` chega como `text/plain;charset=UTF-8`: o backend precisa aceitar JSON nesse content-type). Resposta sempre JSON com `ok: true|false`.

| `acao` | Envia | Responde quando dá certo | Erros |
|---|---|---|---|
| `login` | `{acao:"login", usuario, senha}` | `{ok:true, token, usuario}` | `{ok:false, erro:"credenciais"}` |
| `dados` | `{acao:"dados", token}` | `{ok:true, usuario, minhas:[ids], equipe:{matheus:[ids], aline:[ids], anki:[ids]}}` | `{ok:false, erro:"sessao"}` |
| `salvar` | `{acao:"salvar", token, ids:[ids]}` | `{ok:true, total}` | `{ok:false, erro:"sessao"}` |
| `sair` | `{acao:"sair", token}` | `{ok:true}` | |

Regras:
- `usuario` chega em qualquer caixa: normalizar com `trim().toLowerCase()`.
- `token`: string aleatória longa, validade de 60 dias, guardada no servidor.
- `salvar` **substitui** a lista inteira do usuário (não é incremental). Aceitar só IDs numéricos de 5 a 25 dígitos, no máximo 2000.
- `equipe` inclui o próprio usuário e todos os outros; usuário sem nada salvo pode vir como lista vazia ou ausente.
- Limitar tentativas de login (por exemplo 10 por minuto por IP) para evitar força bruta.

A implementação de referência (Google Apps Script, que não chegou a ser publicada) está em `continuar/referencia/Code.gs.referencia.js`. Serve só para ler a lógica; os usuários foram removidos dela.

## Como o front usa a API (em `continuar/template.html`)

- `const API='__API__'...`: o `rebuild.py` troca `__API__` pela URL. Vazio = modo sem login.
- Token salvo em `localStorage` na chave `swipefile_sessao_v1`. Isso só guarda a sessão; os dados ficam no servidor.
- Curtir sem estar logado abre a tela de login. As gravações têm debounce de 700 ms e mandam a lista completa.

## Arquivos desta pasta

- `template.html`: template do painel (HTML + CSS + JS, com os marcadores `__API__` e `__DATA__`).
- `rebuild.py`: gera o `index.html` da raiz do repositório.
- `dados/`: `criativos_site.json` (964 criativos já com caminhos `img/` e `vid/`), `produtores.json`, `formatos.json`, `testar.json`.
- `referencia/Code.gs.referencia.js`: lógica de referência do backend.
- `coleta/`: ferramentas e dados para a coleta recorrente (fase 2).

## Regras do Matheus para este trabalho

- Português do Brasil, texto sem travessão.
- Nunca exibir senha ou token no chat. Credenciais em `.env` ou arquivo fora do repositório, nunca em commit.
- Não inventar dados. Os números do swipe file vêm da coleta de 17/09/2026 na Meta Ad Library.
- Ações irreversíveis ou que afetem outros sistemas na VPS: confirmar antes.
