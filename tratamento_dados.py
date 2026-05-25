import pandas as pd
import os
import re

# =====================================================
# CAMINHOS
# =====================================================

PASTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_ENTRADA = os.path.join(PASTA_BASE, "dados_brutos")
PASTA_SAIDA = os.path.join(PASTA_BASE, "dados_tratados")

os.makedirs(PASTA_SAIDA, exist_ok=True)

ARQUIVO_FEMINICIDIO = os.path.join(PASTA_ENTRADA, "feminicidio_serie_historica.csv")


# =====================================================
# FUNÇÕES
# =====================================================

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


# =====================================================
# 1. LER BASE ORIGINAL
# =====================================================

print("Lendo arquivo original...")

df = ler_csv(ARQUIVO_FEMINICIDIO)

df["Ano"] = df["DT_OBITO"].apply(extrair_ano)
df = df[df["Ano"].between(1998, 2024)]

df["Decada"] = df["Ano"].apply(definir_decada)
df["Idade"] = df.apply(extrair_idade, axis=1)
df["Faixa_Etaria"] = df["Idade"].apply(faixa_etaria)

if "SEXO" in df.columns:
    df = df[df["SEXO"].astype(str).str.upper().str.contains("FEMININO|F", na=False)]


# =====================================================
# 2. TABELAS DA BASE ORIGINAL
# =====================================================

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


# =====================================================
# 3. FEMINICÍDIOS - FBSP 2015 A 2025
# =====================================================

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


# =====================================================
# 4. CONSERVADORISMO - IPSOS/IPEC
# =====================================================

conservadorismo = pd.DataFrame([
    {"Ano": 2021, "Indice_Conservadorismo": 0.639, "Percentual_Alto_Conservadorismo": None},
    {"Ano": 2022, "Indice_Conservadorismo": 0.637, "Percentual_Alto_Conservadorismo": None},
    {"Ano": 2023, "Indice_Conservadorismo": 0.665, "Percentual_Alto_Conservadorismo": None},
    {"Ano": 2025, "Indice_Conservadorismo": 0.652, "Percentual_Alto_Conservadorismo": 49},
])

conservadorismo["Decada"] = conservadorismo["Ano"].apply(definir_decada)


# =====================================================
# 5. DATASENADO
# =====================================================

datasenado = pd.DataFrame([
    {"Ano": 2013, "Perc_Mulheres_Ja_Sofreram_Violencia_Domestica": 27, "Perc_Brasil_Muito_Machista": None},
    {"Ano": 2019, "Perc_Mulheres_Ja_Sofreram_Violencia_Domestica": 29, "Perc_Brasil_Muito_Machista": None},
    {"Ano": 2023, "Perc_Mulheres_Ja_Sofreram_Violencia_Domestica": 30, "Perc_Brasil_Muito_Machista": None},
    {"Ano": 2025, "Perc_Mulheres_Ja_Sofreram_Violencia_Domestica": None, "Perc_Brasil_Muito_Machista": 70},
])

datasenado["Decada"] = datasenado["Ano"].apply(definir_decada)


# =====================================================
# 6. MISOGINIA DIGITAL
# =====================================================

misoginia_digital = pd.DataFrame([
    {
        "Ano": 2024,
        "Indicador_Misoginia": "Vídeos analisados sobre machosfera/misoginia",
        "Valor_Misoginia": 76300,
        "Unidade_Misoginia": "vídeos"
    },
    {
        "Ano": 2024,
        "Indicador_Misoginia": "Canais brasileiros analisados",
        "Valor_Misoginia": 7812,
        "Unidade_Misoginia": "canais"
    },
    {
        "Ano": 2024,
        "Indicador_Misoginia": "Canais com conteúdo explicitamente misógino",
        "Valor_Misoginia": 137,
        "Unidade_Misoginia": "canais"
    },
    {
        "Ano": 2024,
        "Indicador_Misoginia": "Visualizações em conteúdos misóginos",
        "Valor_Misoginia": 3900000000,
        "Unidade_Misoginia": "visualizações"
    },
    {
        "Ano": 2024,
        "Indicador_Misoginia": "Canais misóginos monetizados",
        "Valor_Misoginia": 80,
        "Unidade_Misoginia": "%"
    },
    {
        "Ano": 2026,
        "Indicador_Misoginia": "Canais misóginos ainda ativos",
        "Valor_Misoginia": 123,
        "Unidade_Misoginia": "canais"
    },
    {
        "Ano": 2026,
        "Indicador_Misoginia": "Crescimento de inscritos em canais misóginos",
        "Valor_Misoginia": 18.55,
        "Unidade_Misoginia": "%"
    }
])

misoginia_digital["Decada"] = misoginia_digital["Ano"].apply(definir_decada)


# =====================================================
# 7. TABELA FINAL POR ANO
# =====================================================

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

tabela_ano = tabela_ano.merge(
    conservadorismo[["Ano", "Indice_Conservadorismo", "Percentual_Alto_Conservadorismo"]],
    on="Ano",
    how="left"
)

tabela_ano = tabela_ano.merge(
    datasenado[
        [
            "Ano",
            "Perc_Mulheres_Ja_Sofreram_Violencia_Domestica",
            "Perc_Brasil_Muito_Machista"
        ]
    ],
    on="Ano",
    how="left"
)

tabela_ano["Decada"] = tabela_ano["Ano"].apply(definir_decada)


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

# =====================================================
# 10. EXPORTAR
# =====================================================

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


print("\nPROCESSAMENTO FINALIZADO COM SUCESSO!")
print("Arquivos criados em:", PASTA_SAIDA)
print("- base_feminicidio_tratada.csv")
print("- tabela_ano_powerbi.csv")
print("- indicadores_sociais.csv")