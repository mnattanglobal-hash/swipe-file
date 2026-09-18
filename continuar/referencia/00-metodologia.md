# Metodologia da pesquisa

**Última varredura:** 17/09/2026
**Responsável pela coleta:** Claude Code (auto mode), a pedido do Matheus. Pesquisa pessoal, sem vínculo com projeto de cliente ou de marca.
**Objetivo:** montar um swipe file permanente de criativos de VENDA de infoproduto low ticket (R$27 a R$150, ou US$5 a US$40 no exterior) para o nicho de relacionamento, com prioridade para operações que mostram sinais verificáveis de escala em mídia paga.

## 1. Fontes primárias usadas

| Fonte | Como foi usada | O que ela prova |
|---|---|---|
| Meta Ad Library (UI em pt-BR, renderizada em navegador) | Coleta estruturada de cada card: ID de biblioteca, data de início de veiculação, nº de anúncios que compartilham o mesmo criativo, copy integral, domínio de destino, URL final decodificada de `l.facebook.com`, thumbnail do vídeo ou imagem do estático | Existência do anúncio, data de início, continuidade, volume de variações, destino comercial |
| Meta Ad Library API (MCP `ads_library_search`) | Contagem de anúncios ativos por página (`estimated_total_count` com filtro ACTIVE), descoberta de `page_id`, moeda da conta | Volume de anúncios ativos na data da coleta |
| Páginas de vendas, VSLs e checkouts (Hotmart, Kiwify, Lastlink, PagTrust, Wiapy, Shopify) | Leitura direta para identificar produto, preço, plataforma, mecanismo, bônus e garantia | Preço e estrutura de oferta |
| Blog oficial do ClickBank | Métricas públicas de EPC, valor médio por venda e conversão das ofertas de relacionamento | Números publicados pela própria plataforma |

## 2. Pipeline técnico

Tudo em `tools/` é reexecutável:

```
tools/harvest.sh <slug> <url> <scrolls> <sessão>   abre a Ad Library, rola N vezes, extrai os cards
tools/extract.js                                   extrator DOM: 1 card = 1 registro
tools/byname.sh <slug> "<nome do anunciante>"      deep dive por nome de página (search_type=page)
tools/deepdive.sh <slug> <page_id>                 deep dive por page_id (view_all_page_id)
tools/thumbs.py <raw.json> <destino>               baixa thumbnail/estático para disco
tools/digest.py <raw.json>                         agrupa por copy distinta e mostra a janela de veiculação
tools/scan.py <n> <raw.json>                       agrupa por anunciante (triagem de descoberta)
tools/catalog.py                                   consolida tudo em dados/cards_all.json
tools/build_criativos.py                           gera o catálogo final a partir do mapa de anunciantes
tools/build_site.py                                gera SWIPE-FILE.html e web/index.html
tools/template.html                                template do painel (o build injeta os dados)
```

O extrator identifica o card pela âncora textual "Identificação da biblioteca" e sobe na árvore DOM até o último ancestral que contém exatamente uma ocorrência dessa âncora. Isso o torna imune às classes CSS ofuscadas do Facebook.

## 3. Estratégia de busca

1. **Descoberta por palavra-chave de nicho** na Ad Library (BR, US, e conteúdo em espanhol). A busca da Meta é aproximadamente OR entre os termos, então termos raros e compostos ("dependência emocional", "attachment style") rendem muito mais que termos genéricos ("término", "autoestima"), que trazem ruído de e-commerce, clínicas e apps de microdrama.
2. **Filtro de criativo de venda:** só entra na biblioteca o anúncio cujo destino é página de vendas, VSL, advertorial ou checkout. Foram descartados anúncios com destino para perfil do Instagram, WhatsApp, "comente eu quero", app store e agendamento de consulta. O filtro está codificado em `tools/build_criativos.py`.
3. **Deep dive por anunciante:** para cada operação relevante, coleta de todos os anúncios ativos da página, agrupando por copy distinta para revelar a estratégia criativa (quantos conceitos, quantas variações por conceito, desde quando cada conceito roda).
4. **Busca dedicada a estáticos** com `media_type=image`, porque a busca padrão é dominada por vídeo.

## 4. Classificação de evidência de escala

A classificação é sobre a **qualidade da evidência disponível**, nunca sobre faturamento presumido.

- **FORTE:** pelo menos três sinais independentes. Exemplo: 100 ou mais anúncios ativos na data da coleta, mesmo conceito com início há mais de 6 meses, e afiliados ou páginas terceiras veiculando o mesmo criativo.
- **MODERADA:** bons proxies, sem número público conclusivo. Exemplo: 20 a 100 anúncios ativos, conceito com 2 a 6 meses de veiculação, várias variações do mesmo criativo.
- **LIMITADA:** o formato é interessante, mas há poucos anúncios ativos, veiculação recente ou nenhuma continuidade observável.

## 5. Como cada afirmação é rotulada

- **FATO COMPROVADO:** existe fonte pública verificável (preço na página de vendas, métrica publicada pela plataforma, contagem de anúncios na Ad Library na data da coleta).
- **EVIDÊNCIA / PROXY:** sinal observável que sugere escala, sem confirmar receita (volume de anúncios, tempo de veiculação, repetição de conceito, presença de afiliados).
- **HIPÓTESE:** leitura de Creative Strategy sobre por que o criativo funciona, sempre marcada como interpretação.

Nenhum número de faturamento, ROAS, spend ou volume de vendas foi estimado. Onde não havia fonte, o campo está explicitamente vazio ou marcado como não identificado.

## 6. Limitações conhecidas

1. A Ad Library mostra **anúncios ativos na data da consulta**. Anúncios pausados antes de 17/09/2026 não aparecem, então a contagem é um piso, não um teto.
2. O campo "Veiculação iniciada em" é a data daquele anúncio específico, não da campanha nem do conceito. Quando vários anúncios compartilham a mesma copy, usei a data mais antiga do grupo como proxy da idade do conceito, e isso está sinalizado como proxy.
3. A Meta não expõe verba, impressões (fora da UE) nem performance. Qualquer leitura de performance aqui é hipótese.
4. Preço: muitas ofertas escondem o preço atrás de VSL com botão liberado por tempo ou de quiz. Nesses casos o preço está marcado como não identificado publicamente.
5. O link `facebook.com/ads/library/?id=<ID>` nem sempre abre o anúncio específico: quando o anúncio pertence a um grupo, a Meta redireciona para a lista de anúncios da página. O identificador confiável é o ID da biblioteca registrado na ficha, e a imagem está salva localmente.
6. URLs de thumbnail da Meta (fbcdn) expiram. Por isso toda imagem relevante foi baixada para `referencias/`, e o artefato aponta para o arquivo local.
7. Vídeos não foram baixados (peso e direitos). Foram preservados thumbnail, duração, copy e engenharia da estrutura.
8. Páginas com bloqueio geográfico (BlossomUp, nos EUA) não puderam ser verificadas a partir do Brasil. Onde isso aconteceu, está escrito na ficha.

## 7. Como atualizar sem começar do zero

```bash
cd swipe-file-low-ticket
./tools/byname.sh p-<produtor> "<Nome da Página>" 10 s1 BR
python3 tools/thumbs.py dados/raw/p-<produtor>.json referencias/brasil/<produtor>
python3 tools/digest.py dados/raw/p-<produtor>.json
python3 tools/catalog.py && python3 tools/build_criativos.py && python3 tools/build_site.py
```

Regra de manutenção: ao recoletar, não sobrescreva a data de coleta antiga dos criativos já catalogados. Acrescente a nova observação. A série histórica, um conceito que continua ativo em duas coletas distantes, é a evidência mais valiosa que esta base pode acumular.
