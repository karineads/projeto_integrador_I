import pandas as pd
import os

PASTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_SAIDA = os.path.join(PASTA_BASE, "dados_tratados")

os.makedirs(PASTA_SAIDA, exist_ok=True)


def salvar_csv(df, nome_arquivo):
    df.to_csv(
        os.path.join(PASTA_SAIDA, nome_arquivo),
        index=False,
        encoding="utf-8-sig",
        sep=";",
        decimal=","
    )


violencia_series = pd.DataFrame([

# DENÚNCIAS - LIGUE 180
{
    "Ano": 2010,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 108026 ,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2011,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 434734 ,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2012,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 306576 ,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2013,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 530000,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2014,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 485105 ,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2015,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 749024,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2016,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 1133024,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2017,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 1170580,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2018,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 1185690,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2019,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 1540529,  
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2020,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor":  1312230, 
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},

{
    "Ano": 2021,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 1077090,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},

{
    "Ano": 2022,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 761701,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},

{
    "Ano": 2023,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 568608,
    "Unidade": "denúncias",
    "Fonte": "Ministério das Mulheres"
},

{
    "Ano": 2024,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 691455,
    "Unidade": "denúncias",
    "Fonte": "Ministério das Mulheres"
},

{
    "Ano": 2025,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 864765,
    "Unidade": "denúncias",
    "Fonte": "Ministério das Mulheres"
},
{
    "Ano": 2026,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor":  45735,
    "Unidade": "denúncias",
    "Fonte": "Ministério das Mulheres"
},
{
    "Ano": 2025,
    "Categoria": "Denúncias_totais",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 16000000,
    "Unidade": "denúncias",
    "Fonte": "Ministério das Mulheres"
}
])

salvar_csv(
    violencia_series,
    "violencia_series_historicas.csv"
)

print("violencia_series_historicas.csv criado")
