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

    # VIOLÊNCIA DOMÉSTICA DECLARADA

    {
        "Ano": 2005,
        "Categoria": "Violência doméstica",
        "Indicador": "Brasileiras que conheciam mulheres vítimas de violência doméstica",
        "Valor": 51,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    {
        "Ano": 2011,
        "Categoria": "Violência doméstica",
        "Indicador": "Brasileiras que conheciam mulheres vítimas de violência doméstica",
        "Valor": 56,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    {
        "Ano": 2013,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam já ter sofrido violência doméstica",
        "Valor": 27,
        "Unidade": "%",
        "Fonte": "PNS/DataSenado"
    },

    {
        "Ano": 2015,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam já ter sofrido violência doméstica",
        "Valor": 18,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    {
        "Ano": 2017,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam já ter sofrido violência doméstica",
        "Valor": 29,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    {
        "Ano": 2019,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam já ter sofrido violência doméstica",
        "Valor": 29,
        "Unidade": "%",
        "Fonte": "PNS/DataSenado"
    },

    {
        "Ano": 2023,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam já ter sofrido violência doméstica",
        "Valor": 30,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    {
        "Ano": 2025,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam já ter sofrido violência doméstica",
        "Valor": 27,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },


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
    "Valor": 52957 ,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2015,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 76651,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2016,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 140350,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2017,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 73668,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2018,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 92663,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2019,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 85412,  
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},
{
    "Ano": 2020,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor":  105671, 
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},

{
    "Ano": 2022,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 87700,
    "Unidade": "denúncias",
    "Fonte": "MMFDH"
},

{
    "Ano": 2023,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 114626,
    "Unidade": "denúncias",
    "Fonte": "Ministério das Mulheres"
},

{
    "Ano": 2024,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 132084,
    "Unidade": "denúncias",
    "Fonte": "Ministério das Mulheres"
},

{
    "Ano": 2025,
    "Categoria": "Denúncias",
    "Indicador": "Denúncias registradas no Ligue 180",
    "Valor": 155111,
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
    "Valor": 1549768,
    "Unidade": "denúncias",
    "Fonte": "Ministério das Mulheres"
}
])

salvar_csv(
    violencia_series,
    "violencia_series_historicas.csv"
)

print("violencia_series_historicas.csv criado")