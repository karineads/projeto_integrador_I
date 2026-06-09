# Violência contra Mulheres no Brasil

> Projeto Integrador — Ciência da Computação  
> Feminicídio, violência de gênero, conservadorismo, representação política e misoginia digital

## Sobre o projeto

Este projeto analisa a violência contra mulheres no Brasil a partir de uma perspectiva histórica, social, política e institucional.

A pesquisa reúne dados públicos relacionados a diferentes formas de violência contra mulheres e busca compreender como fatores estruturais ajudam a compor o contexto em que essas violências continuam ocorrendo.

Foram analisados indicadores sobre:

* homicídios de mulheres;
* feminicídios registrados;
* tentativas de feminicídio;
* violência doméstica;
* violência sexual;
* estupro e estupro de vulnerável;
* denúncias registradas no Ligue 180;
* autoria da violência;
* local de ocorrência da violência;
* instrumentos de proteção e justiça nos municípios;
* representação feminina nos espaços de poder;
* conservadorismo;
* misoginia digital.

A pesquisa entende a violência contra mulheres como um fenômeno multifatorial, influenciado por aspectos institucionais, culturais, econômicos, políticos e digitais que devem ser analisados de forma conjunta. 

O objetivo não é estabelecer relações simplificadas de causa e efeito, mas compreender como esses apectos aparecem simultaneamente em um cenário de persistência da violência contra mulheres.


## Objetivos

* Analisar a evolução histórica da violência contra mulheres no Brasil;
* Comparar homicídios femininos, feminicídios e tentativas de feminicídio;
* Investigar padrões de violência doméstica e sexual;
* Identificar os principais locais e autores das agressões;
* Avaliar a disponibilidade de instrumentos de proteção e justiça;
* Discutir a representação feminina nos espaços de poder;
* Relacionar indicadores de conservadorismo e misoginia digital ao contexto social analisado;
* Desenvolver visualizações interativas para apoiar a interpretação dos dados

## Organização dos arquivos

### tratamento_dados.py

Script principal responsável pelo tratamento, limpeza e integração das bases utilizadas no projeto.

### violencia_series.py

Script auxiliar utilizado para organizar indicadores históricos complementares utilizados na análise.

### index.html

Página principal do projeto publicada no GitHub Pages.

### style.css

Arquivo responsável pela estilização visual da página.

## Organização dos dados

### dados_brutos/

Pasta que contém as bases originais utilizadas no projeto.

### dados_tratados/

Arquivos gerados após o processamento em Python.

#### tabela_ano_powerbi.csv

Contém indicadores históricos relacionados à violência contra mulheres.

#### indicadores_sociais.csv

Tabela complementar com indicadores institucionais, políticos, sociais e digitais.

#### base_feminicidio_tratada.csv

Base tratada utilizada para análises exploratórias e geração dos indicadores.

#### homicidios_gerais_x_mulheres.csv

Tabela utilizada para cálculo proporcional entre homicídios gerais e homicídios femininos.

## Dashboard interativo

O dashboard reúne indicadores históricos relacionados à violência contra mulheres, incluindo:

* homicídios femininos;
* feminicídios;
* tentativas de feminicídio.
* notificações de violência;
* estupro;
* denúncias do Ligue 180;
* autoria da violência;
* local da violência;
* instrumentos de proteção;
* instrumentos de justiça;
* representação feminina nos espaços de poder;
* conservadorismo;
* misoginia digital.

O painel foi desenvolvido no Power BI e incorporado ao GitHub Pages.

## Tecnologias utilizadas

* Python
* Pandas
* Power BI
* HTML5
* CSS3
* GitHub Pages
  
## Limitações da pesquisa

Esta pesquisa utiliza exclusivamente bases públicas.

Os dados podem apresentar:

* subnotificação;
* diferenças metodológicas entre instituições;
* alterações nos critérios de registro ao longo do tempo;
* limitações na classificação de feminicídios;
* revisões posteriores dos dados oficiais.

Por esse motivo, os indicadores devem ser interpretados como instrumentos de análise e não como representação absoluta da realidade.

## Bases de dados utilizadas

### Base principal

* [Kaggle — Feminicídio no Brasil](https://www.kaggle.com/datasets/rafatrindade/feminicidio-br)

### Feminicídios registrados

* [Fórum Brasileiro de Segurança Pública (FBSP)](https://dossies.agenciapatriciagalvao.org.br/dados-e-fontes/pesquisa/retrato-dos-feminicidios-no-brasil-fbsp-2026/)

### Violência doméstica e denúncias

* [DataSenado — Pesquisa Nacional de Violência contra a Mulher](https://www12.senado.leg.br/institucional/datasenado/materias/pesquisas/pesquisa-nacional-de-violencia-contra-a-mulher-datasenado-2025)
  
* [Ligue 180 — Ministério das Mulheres](https://www.gov.br/mulheres/pt-br/ligue180/balancos)

* [RASEAM — Relatório Anual Socioeconômico da Mulher](https://www.gov.br/mulheres/pt-br/observatorio-brasil-da-igualdade-de-genero/raseam)


### Segurança pública e violência

* [Atlas da Violência — Ipea](https://www.ipea.gov.br/atlasviolencia/publicacoes/276/atlas-2023-violencia-contra-mulher)

* [DataSUS / SIM / TabNet](https://datasus.saude.gov.br/informacoes-de-saude-tabnet/)

* [SINAN](https://datasus.saude.gov.br/sistema-de-informacao-de-agravos-de-notificacao-sinan/)


### Conservadorismo e contexto social

* [Ipsos/Ipec — Índice de Conservadorismo Brasileiro](https://www.ipsos.com/pt-br/indice-de-conservadorismo-brasileiro-2025)

* [AtlasIntel / Opera Mundi](https://operamundi.uol.com.br/brasil/conservadorismo-cresce-entre-jovens-52-da-geracao-z-e-de-direita-aponta-pesquisa/)

* [Unicamp — Conservadorismo e violência contra mulheres](https://www2.unicamp.br/unicamp/noticias/2023/03/08/aumento-da-violencia-contra-mulheres-tem-relacao-com-avanco-do-conservadorismo/)


### Misoginia digital

* [NetLab-UFRJ](https://netlab.eco.ufrj.br/post/misoginia-no-youtube-90-dos-canais-com-mapeados-em-2024-seguem-dispon%C3%ADveis-na-plataforma)

* [Ministério das Mulheres — pesquisa sobre misoginia digital](https://www.gov.br/mulheres/pt-br/central-de-conteudos/noticias/2024/dezembro/pesquisa-inedita-mostra-como-influenciadores-lucram-com-conteudos-misoginos-no-youtube)

* [MINA-BR — Base sobre misoginia online](https://redu.unicamp.br/dataset.xhtml?persistentId=doi:10.25824/redu/MQD68Z)

### Representação feminina nos espaços de poder

Dados compilados a partir de informações divulgadas por:

* Câmara dos Deputados;
* Senado Federal;
* Supremo Tribunal Federal (STF);
* Ministério da Gestão e da Inovação em Serviços Públicos.


## Visualização do projeto

[GitHub Pages](https://karineads.github.io/projeto_integrador_I/)

[Dashboard Power BI](https://app.powerbi.com/reportEmbed?reportId=ee7acaa0-e72c-4576-82d9-bfd257d4d264&autoAuth=true&ctid=dfb66dc4-3f3c-492c-991d-727dbd1c89d4&filterPaneEnabled=false&navContentPaneEnabled=true)

## Autora

Karine Araujo dos Santos

Projeto Integrador — Ciência da Computação
UniCEUB

### Observação

Este projeto utiliza exclusivamente dados públicos e possui finalidade acadêmica e educacional.
