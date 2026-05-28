# Violência contra Mulheres no Brasil

> Projeto Integrador — Ciência da Computação  
> Feminicídio, violência de gênero, conservadorismo e misoginia digital

## Sobre o projeto

Este projeto tem como objetivo analisar a evolução da violência contra mulheres no Brasil a partir de dados públicos sobre:

* homicídios de mulheres;
* feminicídios;
* violência doméstica;
* denúncias registradas;
* machismo estrutural;
* conservadorismo social;
* misoginia digital e discursos de ódio nas redes sociais.

O projeto não pretende afirmar relações simplificadas de causalidade, mas investigar como elementos como fragilidade institucional, discursos conservadores sobre papéis femininos e a expansão da misoginia digital podem contribuir para a normalização da violência contra mulheres.

## Metodologia

Os dados utilizados no projeto foram coletados a partir de bases públicas,
tratados e organizados com Python e Pandas para posterior integração ao
Power BI.

O projeto utiliza visualização de dados para comparar séries históricas,
identificar padrões e relacionar indicadores sociais e criminais em um
dashboard interativo disponibilizado via GitHub Pages.

## Organização dos arquivos

### tratamento_dados.py

Script principal responsável pelo tratamento, limpeza e integração das bases utilizadas no projeto.

O arquivo realiza:

* padronização dos dados;
* tratamento de datas;
* agrupamentos históricos;
* integração entre homicídios, feminicídios e indicadores sociais;
* criação das tabelas finais utilizadas no Power BI.

Também é responsável pela geração automática dos arquivos presentes em `dados_tratados/`.


### violencia_series.py

Script auxiliar utilizado para processamento e organização de séries históricas relacionadas à violência contra mulheres.

Auxilia na preparação de indicadores históricos utilizados nas análises e visualizações do dashboard.


### index.html

Página principal do projeto publicada no GitHub Pages.

Contém:

* contextualização da pesquisa;
* discussão social e histórica;
* conceitos utilizados;
* incorporação do dashboard Power BI;
* interpretação dos dados;
* referências utilizadas.

### style.css

Arquivo responsável pela estilização visual da página.

## Organização dos dados

### dados_brutos/

Pasta que contém as bases originais utilizadas no projeto.

#### Arquivos principais:

#### feminicidio_serie_historica.csv

Base histórica consolidada com registros de óbitos femininos por causas externas com potencial enquadramento como feminicídio.

Utilizada para construção das séries históricas de homicídios femininos.


#### Homicídios_países.csv

Base contendo os homicídios gerais registrados no Brasil ao longo dos anos.

Utilizada para comparação proporcional com os homicídios femininos.


#### Homicídios Mulheres_países.csv

Base contendo exclusivamente homicídios femininos registrados no país.

Utilizada para:

* cálculo proporcional;
* comparação entre homicídios gerais e femininos;

## Dados processados

### dados_tratados/

Pasta com os arquivos gerados após o processamento em Python.

#### base_feminicidio_tratada.csv

Base detalhada tratada para análises exploratórias.

#### tabela_ano_powerbi.csv

Tabela principal utilizada no Power BI.

#### indicadores_sociais.csv

Tabela complementar utilizada nos gráficos sociais do dashboard.

#### homicidios_gerais_x_mulheres.csv

Utilizada para demonstrar a proporção da violência letal contra mulheres em relação aos homicídios gerais no Brasil.

## Dashboard interativo

O dashboard reúne indicadores históricos relacionados à violência contra mulheres, incluindo:

* homicídios de mulheres;
* feminicídios;
* violência doméstica;
* denúncias;
* percepção do machismo;
* indicadores de conservadorismo;
* misoginia digital.

O painel foi desenvolvido no Power BI e incorporado ao GitHub Pages.

## Principais temas abordados

#### Feminicídio, violência letal e subnotificação

Análise histórica dos homicídios de mulheres e feminicídios registrados no Brasil.

#### Violência doméstica

Dados sobre violência doméstica, denúncias e subnotificação.

#### Conservadorismo

Indicadores sociais relacionados ao conservadorismo, papéis tradicionais de gênero e discursos que reforçam desigualdades estruturais entre homens e mulheres.

#### Misoginia digital

Análise da circulação de discursos misóginos em plataformas digitais, machosfera e monetização do ódio contra mulheres.

#### Denúncia e proteção institucional

Discussão sobre os limites entre denúncia, acolhimento, investigação e proteção efetiva das vítimas.

## Tecnologias utilizadas

* Python
* Pandas
* Power BI
* HTML5
* CSS3
* GitHub Pages
  
## Limitações da pesquisa

Esta pesquisa utiliza exclusivamente dados públicos e séries históricas produzidas por diferentes instituições. Dessa forma, os dados podem apresentar:

*diferenças metodológicas entre bases;
*subnotificação;
*alterações nos critérios de registro ao longo do tempo;
*limitações institucionais na classificação de feminicídios;
*lacunas temporais em determinados indicadores sociais.

## Bases de dados utilizadas

### Base principal

* [Kaggle — Feminicídio no Brasil](https://www.kaggle.com/datasets/rafatrindade/feminicidio-br)
  
  Base consolidada com os registros finais e validados de óbitos femininos por causas externas, com potencial enquadramento como feminicídio

### Feminicídios registrados

* [Fórum Brasileiro de Segurança Pública (FBSP)](https://dossies.agenciapatriciagalvao.org.br/dados-e-fontes/pesquisa/retrato-dos-feminicidios-no-brasil-fbsp-2026/)


### Violência doméstica e denúncias

* [DataSenado — Pesquisa Nacional de Violência contra a Mulher](https://www12.senado.leg.br/institucional/datasenado/materias/pesquisas/pesquisa-nacional-de-violencia-contra-a-mulher-datasenado-2025)
  
* [Ligue 180 — Ministério das Mulheres](https://www.gov.br/mulheres/pt-br/ligue180/balancos)

* [RASEAM 2025 — Relatório Anual Socioeconômico da Mulher](https://www.gov.br/mulheres/pt-br/central-de-conteudos/publicacoes/raseam-2025.pdf)


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


## Visualização do projeto

[GitHub Pages](https://karineads.github.io/projeto_integrador_I/)

[Dashboard Power BI](https://app.powerbi.com/reportEmbed?reportId=ee7acaa0-e72c-4576-82d9-bfd257d4d264&autoAuth=true&ctid=dfb66dc4-3f3c-492c-991d-727dbd1c89d4&filterPaneEnabled=false&navContentPaneEnabled=true)


## Autora

Karine Araujo dos Santos

Projeto Integrador — Ciência da Computação
UniCEUB

## Observação

Este projeto utiliza exclusivamente dados públicos e possui finalidade acadêmica e educacional.


