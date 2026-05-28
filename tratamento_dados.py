import pandas as pd
import os
import re


PASTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_ENTRADA = os.path.join(PASTA_BASE, "dados_brutos")
PASTA_SAIDA = os.path.join(PASTA_BASE, "dados_tratados")

os.makedirs(PASTA_SAIDA, exist_ok=True)

ARQUIVO_FEMINICIDIO = os.path.join(PASTA_ENTRADA, "feminicidio_serie_historica.csv")
ARQUIVO_HOMICIDIOS_GERAIS = os.path.join(PASTA_ENTRADA, "Homicídios_países.csv")
ARQUIVO_HOMICIDIOS_MULHERES = os.path.join(PASTA_ENTRADA, "Homicídios Mulheres_países.csv")


# FUNÇÕES
def ler_csv(caminho):
    encodings = ["utf-8", "utf-8-sig", "latin1", "cp1252"]

    for enc in encodings:
        try:
            return pd.read_csv(caminho, sep=None, engine="python", encoding=enc)
        except Exception:
            pass

    raise Exception(f"Não foi possível ler o arquivo: {caminho}")


def extrair_ano(valor):
    if pd.isna(valor):
        return None

    texto = re.sub(r"\D", "", str(valor))

    if len(texto) >= 8:
        return int(texto[-4:])

    if len(texto) == 4:
        return int(texto)

    return None


def definir_decada(ano):
    if pd.isna(ano):
        return "Não informado"

    ano = int(ano)

    if 1998 <= ano <= 2009:
        return "1998-2009"
    elif 2010 <= ano <= 2019:
        return "2010-2019"
    elif 2020 <= ano <= 2025:
        return "2020-2025"
    else:
        return "Fora do período"


def extrair_idade(row):
    ano_obito = row["Ano"]
    nascimento = row.get("DT_NASCIMENTO", None)

    if pd.isna(ano_obito) or pd.isna(nascimento):
        return None

    texto = re.sub(r"\D", "", str(nascimento))

    if len(texto) >= 8:
        ano_nascimento = int(texto[-4:])
        idade = ano_obito - ano_nascimento

        if 0 <= idade <= 120:
            return idade

    return None


def faixa_etaria(idade):
    if pd.isna(idade):
        return "Não informado"
    elif idade <= 17:
        return "0-17"
    elif idade <= 29:
        return "18-29"
    elif idade <= 44:
        return "30-44"
    else:
        return "45+"

print("Lendo arquivo original...")

df = ler_csv(ARQUIVO_FEMINICIDIO)

df["Ano"] = df["DT_OBITO"].apply(extrair_ano)
df = df[df["Ano"].between(1998, 2024)]

df["Decada"] = df["Ano"].apply(definir_decada)
df["Idade"] = df.apply(extrair_idade, axis=1)
df["Faixa_Etaria"] = df["Idade"].apply(faixa_etaria)

if "SEXO" in df.columns:
    df = df[df["SEXO"].astype(str).str.upper().str.contains("FEMININO|F", na=False)]

# TABELAS 
base_tratada = df.copy()

homicidios_ano = (
    df.groupby("Ano")
    .size()
    .reset_index(name="Total_Homicidios_Mulheres")
)

homicidios_ano["Decada"] = homicidios_ano["Ano"].apply(definir_decada)

homicidios_decada = (
    df.groupby("Decada")
    .size()
    .reset_index(name="Total_Homicidios_Mulheres")
)

tabela_raca = (
    df.groupby(["Ano", "RACA_COR"])
    .size()
    .reset_index(name="Total")
) if "RACA_COR" in df.columns else pd.DataFrame()

tabela_local = (
    df.groupby(["Ano", "LOCAL_OCORRENCIA_OBITO"])
    .size()
    .reset_index(name="Total")
) if "LOCAL_OCORRENCIA_OBITO" in df.columns else pd.DataFrame()

tabela_faixa = (
    df.groupby(["Ano", "Faixa_Etaria"])
    .size()
    .reset_index(name="Total")
)

# FEMINICÍDIOS 

feminicidios_fbsp = pd.DataFrame([
    {"Ano": 2015, "Feminicidios_FBSP": 449},
    {"Ano": 2016, "Feminicidios_FBSP": 929},
    {"Ano": 2017, "Feminicidios_FBSP": 1075},
    {"Ano": 2018, "Feminicidios_FBSP": 1229},
    {"Ano": 2019, "Feminicidios_FBSP": 1330},
    {"Ano": 2020, "Feminicidios_FBSP": 1354},
    {"Ano": 2021, "Feminicidios_FBSP": 1347},
    {"Ano": 2022, "Feminicidios_FBSP": 1455},
    {"Ano": 2023, "Feminicidios_FBSP": 1475},
    {"Ano": 2024, "Feminicidios_FBSP": 1492},
    {"Ano": 2025, "Feminicidios_FBSP": 1568},
])

feminicidios_fbsp["Decada"] = feminicidios_fbsp["Ano"].apply(definir_decada)

# TABELA FINAL POR ANO

anos = pd.DataFrame({"Ano": list(range(1998, 2026))})

tabela_ano = anos.copy()

tabela_ano = tabela_ano.merge(
    homicidios_ano[["Ano", "Total_Homicidios_Mulheres"]],
    on="Ano",
    how="left"
)

tabela_ano = tabela_ano.merge(
    feminicidios_fbsp[["Ano", "Feminicidios_FBSP"]],
    on="Ano",
    how="left"
)

tabela_ano["Decada"] = tabela_ano["Ano"].apply(definir_decada)

# HOMICÍDIOS GERAIS X HOMICÍDIOS DE MULHERES

def preparar_homicidios_comparacao():
    df_geral = ler_csv(ARQUIVO_HOMICIDIOS_GERAIS)
    df_mulheres = ler_csv(ARQUIVO_HOMICIDIOS_MULHERES)

    # Extrair ano
    df_geral["Ano"] = pd.to_datetime(df_geral["Período"], errors="coerce").dt.year
    df_mulheres["Ano"] = pd.to_datetime(df_mulheres["Período"], errors="coerce").dt.year

    # Padronizar nomes
    df_geral = df_geral[["Ano", "Valor"]].rename(
        columns={"Valor": "Homicidios_Gerais"}
    )

    df_mulheres = df_mulheres[["Ano", "Valor"]].rename(
        columns={"Valor": "Homicidios_Mulheres"}
    )

    # Juntar as duas tabelas
    comparacao = df_geral.merge(
        df_mulheres,
        on="Ano",
        how="left"
    )

    # Manter período usado no projeto
    comparacao = comparacao[comparacao["Ano"].between(1998, 2024)]

    comparacao["Decada"] = comparacao["Ano"].apply(definir_decada)

    # Percentual de homicídios de mulheres dentro dos homicídios gerais
    comparacao["Percentual_Mulheres"] = (
        comparacao["Homicidios_Mulheres"] / comparacao["Homicidios_Gerais"] * 100
    ).round(2)

    # Adicionar feminicídios oficiais FBSP
    comparacao = comparacao.merge(
        feminicidios_fbsp[["Ano", "Feminicidios_FBSP"]],
        on="Ano",
        how="left"
    )

    # Diferença entre homicídios de mulheres e feminicídios registrados
    comparacao["Diferenca_Homicidios_Feminicidios"] = (
        comparacao["Homicidios_Mulheres"] - comparacao["Feminicidios_FBSP"]
    )

    return comparacao


homicidios_comparacao = preparar_homicidios_comparacao()


# INDICADORES SOCIAIS 

indicadores_sociais = pd.DataFrame([


    # VIOLÊNCIA DOMÉSTICA / PERCEPÇÃO
    {
        "Ano": 2005,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam ter sofrido violência doméstica",
        "Valor": 17,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },
    {
        "Ano": 2007,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam ter sofrido violência doméstica",
        "Valor": 15,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },
    {
        "Ano": 2009,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam ter sofrido violência doméstica",
        "Valor": 19,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },
    {
        "Ano": 2011,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam ter sofrido violência doméstica",
        "Valor": 19,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },
    {
        "Ano": 2013,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam ter sofrido violência doméstica",
        "Valor": 19,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    {
        "Ano": 2015,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam ter sofrido violência doméstica",
        "Valor": 18,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    {
        "Ano": 2017,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam ter sofrido violência doméstica",
        "Valor": 29,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    {
        "Ano": 2019,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam ter sofrido violência doméstica",
        "Valor": 27,
        "Unidade": "%",
        "Fonte": "PNS/DataSenado"
    },
    {
        "Ano": 2021,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam ter sofrido violência doméstica",
        "Valor": 27,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    {
        "Ano": 2023,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam ter sofrido violência doméstica",
        "Valor": 30,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    {
        "Ano": 2025,
        "Categoria": "Violência doméstica",
        "Indicador": "Mulheres que declararam ter sofrido violência doméstica",
        "Valor": 27,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    # MACHISMO / PERCEPÇÃO SOCIAL
    {
        "Ano": 2025,
        "Categoria": "Machismo",
        "Indicador": "Mulheres que consideram o Brasil um país machista",
        "Valor": 94,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },
    {
        "Ano": 2025,
        "Categoria": "Machismo",
        "Indicador": "Mulheres que consideram o Brasil muito machista",
        "Valor": 70,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    {
        "Ano": 2025,
        "Categoria": "Machismo",
        "Indicador": "Mulheres que dizem que mulheres não são tratadas com respeito",
        "Valor": 46,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    {
        "Ano": 2025,
        "Categoria": "Machismo",
        "Indicador": "Mulheres que conhecem vítima de violência doméstica",
        "Valor": 67,
        "Unidade": "%",
        "Fonte": "DataSenado"
    },

    # CONSERVADORISMO
        {
        "Ano": 2010,
        "Categoria": "Conservadorismo",
        "Indicador": "Índice de conservadorismo brasileiro",
        "Valor": 0.657,
        "Unidade": "",
        "Fonte": "Ibope "
    },
    {
        "Ano": 2016,
        "Categoria": "Conservadorismo",
        "Indicador": "Índice de conservadorismo brasileiro",
        "Valor": 0.686,
        "Unidade": "",
        "Fonte": "Ibope "
    },
    {
        "Ano": 2018,
        "Categoria": "Conservadorismo",
        "Indicador": "Índice de conservadorismo brasileiro",
        "Valor": 0.693,
        "Unidade": "",
        "Fonte": "Ibope "
    },
    {
        "Ano": 2021,
        "Categoria": "Conservadorismo",
        "Indicador": "Índice de conservadorismo brasileiro",
        "Valor": 0.639,
        "Unidade": "",
        "Fonte": "Ipsos/Ipec"
    },

    {
        "Ano": 2022,
        "Categoria": "Conservadorismo",
        "Indicador": "Índice de conservadorismo brasileiro",
        "Valor": 0.637,
        "Unidade": "",
        "Fonte": "Ipsos/Ipec"
    },

    {
        "Ano": 2023,
        "Categoria": "Conservadorismo",
        "Indicador": "Índice de conservadorismo brasileiro",
        "Valor": 0.665,
        "Unidade": "",
        "Fonte": "Ipsos/Ipec"
    },
    {
        "Ano": 2024,
        "Categoria": "Conservadorismo",
        "Indicador": "Índice de conservadorismo brasileiro",
        "Valor": 0.652,
        "Unidade": "",
        "Fonte": "Ipsos/Ipec"
    },

    {
        "Ano": 2025,
        "Categoria": "Conservadorismo",
        "Indicador": "Índice de conservadorismo brasileiro",
        "Valor": 0.652,
        "Unidade": "",
        "Fonte": "Ipsos/Ipec"
    },
    
    {
        "Ano": 2010,
        "Categoria": "Conservadorismo",
        "Indicador": "População com alto grau de conservadorismo",
        "Valor": 54,
        "Unidade": "%",
        "Fonte": "Ibope "
    },
        {
        "Ano": 2016,
        "Categoria": "Conservadorismo",
        "Indicador": "População com alto grau de conservadorismo",
        "Valor": 49,
        "Unidade": "%",
        "Fonte": "Ibope "
    },
    {
        "Ano": 2018,
        "Categoria": "Conservadorismo",
        "Indicador": "População com alto grau de conservadorismo",
        "Valor": 55,
        "Unidade": "%",
        "Fonte": "Ibope "
    },
    {
        "Ano": 2024,
        "Categoria": "Conservadorismo",
        "Indicador": "População com alto grau de conservadorismo",
        "Valor": 49,
        "Unidade": "%",
        "Fonte": "Ipsos/Ipec"
    },

    {
        "Ano": 2025,
        "Categoria": "Conservadorismo",
        "Indicador": "População com alto grau de conservadorismo",
        "Valor": 49,
        "Unidade": "%",
        "Fonte": "Ipsos/Ipec"
    },

    # MISOGINIA DIGITAL
    {
        "Ano": 2024,
        "Categoria": "Misoginia Digital",
        "Indicador": "Vídeos sobre machosfera e misoginia analisados",
        "Valor": 76300,
        "Unidade": "vídeos",
        "Fonte": "NetLab-UFRJ / Ministério das Mulheres"
    },

    {
        "Ano": 2024,
        "Categoria": "Misoginia Digital",
        "Indicador": "Canais com conteúdo explicitamente misógino",
        "Valor": 137,
        "Unidade": "canais",
        "Fonte": "NetLab-UFRJ / Ministério das Mulheres"
    },

    {
        "Ano": 2024,
        "Categoria": "Misoginia Digital",
        "Indicador": "Canais misóginos monetizados",
        "Valor": 80,
        "Unidade": "%",
        "Fonte": "NetLab-UFRJ / Ministério das Mulheres"
    },

    {
        "Ano": 2024,
        "Categoria": "Misoginia Digital",
        "Indicador": "Visualizações em conteúdos misóginos",
        "Valor": 3900000000,
        "Unidade": "visualizações",
        "Fonte": "NetLab-UFRJ / Ministério das Mulheres"
    }
])

indicadores_sociais["Decada"] = indicadores_sociais["Ano"].apply(definir_decada)

# EXPORTAR

base_tratada.to_csv(
    os.path.join(PASTA_SAIDA, "base_feminicidio_tratada.csv"),
    index=False,
    encoding="utf-8-sig",
    sep=";",
    decimal=","
)

tabela_ano.to_csv(
    os.path.join(PASTA_SAIDA, "tabela_ano_powerbi.csv"),
    index=False,
    encoding="utf-8-sig",
    sep=";",
    decimal=","
)

indicadores_sociais.to_csv(
    os.path.join(PASTA_SAIDA, "indicadores_sociais.csv"),
    index=False,
    encoding="utf-8-sig",
    sep=";",
    decimal=","
)

homicidios_comparacao.to_csv(
    os.path.join(PASTA_SAIDA, "homicidios_gerais_x_mulheres.csv"),
    index=False,
    encoding="utf-8-sig",
    sep=";",
    decimal=","
)

print("\nPROCESSAMENTO FINALIZADO COM SUCESSO!")
print("Arquivos criados em:", PASTA_SAIDA)
print("- base_feminicidio_tratada.csv")
print("- tabela_ano_powerbi.csv")
print("- indicadores_sociais.csv")
print("- homicidios_gerais_x_mulheres.csv")