# O que ficou de fora da biblioteca, e por quê

O recorte é **criativo de venda**: anúncio, depois página de vendas ou VSL ou advertorial, depois checkout. Muita coisa boa apareceu na coleta e foi descartada por não caber nesse recorte. Este documento registra os descartes para que ninguém refaça o mesmo caminho na próxima atualização.

## Descartados por objetivo de campanha

| Operação | O que faz | Por que ficou de fora |
|---|---|---|
| Adam Lane Smith, Attachment Specialist (EUA) | 68 anúncios ativos, autoridade real (250 mil inscritos no YouTube, 45 mil na newsletter) | Os destinos são `links.adamlanesmith.com/quiz` e `bundle.adamlanesmith.com/masterclass-signup`: captura de lead e masterclass, não venda direta |
| Brave Thinking Institute, Mary Manin Morrissey e Mat Boggs (EUA) | 119 anúncios ativos, muitos estáticos bem construídos | Funil de workshop gratuito para programa caro. Fora do recorte de low ticket e de venda direta |
| The Personal Development School (Thais Gibson, EUA) | Quiz de estilo de apego | Quiz gratuito para captura |
| The Art of Healing by Trevor (EUA) | 38 anúncios ativos | Destino é workshop gratuito e ebook gratuito |
| Leslie Huddart (EUA) | 17 anúncios ativos | Página de captura ("5 Step Formula", formulário) |
| The Awake Network (EUA) | 13 anúncios | Workshop gratuito com Peter Levine, link de afiliado |
| We Need To Talk (EUA) | Quiz de estilo de apego | Captura |
| Vários perfis brasileiros de terapia e consulta | "Agende sua sessão", "Comente eu quero", "Chamar no WhatsApp" | Objetivo é conversa ou agendamento, não venda de produto digital |
| "Volte com seu Ex, Em 30 Dias" (BR) | Anúncios de reconquista | CTA é "comente eu quero" e link para o perfil do Instagram |

## Descartados por não serem do universo de infoproduto low ticket

- **Apps de microdrama** (ReelShort, Quick Drama, Mini Series Zone e dezenas de páginas clonadas). Dominaram várias buscas de "término" e "reconquista". O formato de anúncio é interessante, uma novela de 20 minutos rodando como criativo, mas o objetivo é instalação de app.
- **Sites de quiz por arbitragem** (Stay Bright Quizzes, com destino em logcabindaily.com e buzznewfeeds.com). 43 anúncios estáticos ativos, formato de quiz muito bem feito, mas monetização por conteúdo e anúncio, sem produto.
- **E-commerce e clínicas** que apareceram nas buscas por palavra genérica: odontologia, oftalmologia, estética, planos de saúde, moda.

## Incluídos apesar de estarem fora do recorte de produto, só pelo formato

Quatro casos entraram na biblioteca com marcação explícita, porque o **formato de criativo** é transferível:

- **Aquiete Agora** (BR): floral a R$84,90, produto físico. Está aqui pela copy longa de confissão em primeira pessoa.
- **Blood Sugar Journal e Blood Pressure Journal** (EUA): diários de saúde. Provam que o playbook de imagem silenciosa com copy longa roda em nichos diferentes.
- **Dragon Fire Method** (EUA): livro físico a US$27 usado como low ticket, com ebooks e audiobook empilhados como bônus.

Todos aparecem no painel com o grupo de nicho marcado, então dá para escondê-los com um clique no filtro.

## Limites da coleta que valem registrar

1. A Ad Library só mostra anúncios ativos na data da consulta. Toda contagem aqui é piso, não teto.
2. A busca por palavra-chave da Meta é aproximadamente OR entre os termos. Termos genéricos trazem ruído massivo; termos raros e compostos rendem muito mais.
3. Páginas de vendas americanas com bloqueio geográfico não puderam ser verificadas a partir do Brasil.
4. Muitas ofertas escondem o preço atrás de VSL ou quiz. Nesses casos o campo de preço está como "não identificado publicamente", e não foi estimado.

## Segunda passada do filtro (18/09/2026): corte de isca grátis

O recorte foi endurecido depois da primeira entrega. Agora só entra anúncio cujo destino seja **página de vendas, checkout, VSL ou quiz** (o quiz entra porque termina em oferta). Qualquer coisa que entregue material grátis como objetivo principal saiu, e a regra está codificada em `tools/build_criativos.py`, então ela vale para toda coleta futura.

O que saiu nessa segunda passada:

| Operação | Anúncios removidos | Motivo |
|---|---|---|
| Italo Ventura | 100 | O destino é aula gratuita com "ebook gratuito" de bônus. É captura de lead, mesmo com 100 anúncios ativos e 7 meses de veiculação |
| Dri Martini (parte dos anúncios) | 42 no total do catálogo | As peças que empurram "a aula é gratuita" saíram. As que levam ao teste de 3 minutos e ao Manual SOS de R$37 ficaram |
| Rachel Morrison (páginas paralelas) | 6 | A mesma página de anunciante também roda anúncios de suplemento para cães (doggysupps.com), outro nicho e outra oferta |
| Sarah Michelle (páginas paralelas) | 13 | Anúncios de curso para enfermeiras (npreviews.com) na mesma página do Sigil Magik Engine |
| Destino em perfil social ou app | 4 | Instagram, WhatsApp, Play Store |

Termos que acionam o corte automático na copy: "aula gratuita", "aula é gratuita", "masterclass gratuita", "ebook gratuito", "livro eletrônico gratuito", "material gratuito", "baixe grátis", "inscreva-se gratuitamente", "free ebook/guide/training/workshop/masterclass/class/pdf/download". Na URL: `/aula`, `webinar`, `inscricao`, `cadastro`, `lead`, `captura`, `signup`, `register`.

Cada criativo do painel agora carrega o campo **Destino do anúncio** (página de vendas, checkout, quiz ou VSL), e esse campo é filtrável. Se algum dia entrar algo que não deveria, dá para ver e cortar pelo filtro.
