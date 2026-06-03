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
# RASEAM 2026 - INDICADORES OFICIAIS
# =====================================================

raseam_2026 = pd.DataFrame([

    # NASCIDOS VIVOS DE MÃES COM ATÉ 14 ANOS - SINASC
    {"Ano": 2014, "Categoria": "Gravidez infantil", "Indicador": "Nascidos vivos de mães com até 14 anos", "Valor": 28245, "Unidade": "nascidos vivos", "Fonte": "RASEAM 2026 / Sinasc"},
    {"Ano": 2015, "Categoria": "Gravidez infantil", "Indicador": "Nascidos vivos de mães com até 14 anos", "Valor": 26701, "Unidade": "nascidos vivos", "Fonte": "RASEAM 2026 / Sinasc"},
    {"Ano": 2016, "Categoria": "Gravidez infantil", "Indicador": "Nascidos vivos de mães com até 14 anos", "Valor": 24139, "Unidade": "nascidos vivos", "Fonte": "RASEAM 2026 / Sinasc"},
    {"Ano": 2017, "Categoria": "Gravidez infantil", "Indicador": "Nascidos vivos de mães com até 14 anos", "Valor": 22146, "Unidade": "nascidos vivos", "Fonte": "RASEAM 2026 / Sinasc"},
    {"Ano": 2018, "Categoria": "Gravidez infantil", "Indicador": "Nascidos vivos de mães com até 14 anos", "Valor": 21172, "Unidade": "nascidos vivos", "Fonte": "RASEAM 2026 / Sinasc"},
    {"Ano": 2019, "Categoria": "Gravidez infantil", "Indicador": "Nascidos vivos de mães com até 14 anos", "Valor": 19333, "Unidade": "nascidos vivos", "Fonte": "RASEAM 2026 / Sinasc"},
    {"Ano": 2020, "Categoria": "Gravidez infantil", "Indicador": "Nascidos vivos de mães com até 14 anos", "Valor": 17579, "Unidade": "nascidos vivos", "Fonte": "RASEAM 2026 / Sinasc"},
    {"Ano": 2021, "Categoria": "Gravidez infantil", "Indicador": "Nascidos vivos de mães com até 14 anos", "Valor": 17458, "Unidade": "nascidos vivos", "Fonte": "RASEAM 2026 / Sinasc"},
    {"Ano": 2022, "Categoria": "Gravidez infantil", "Indicador": "Nascidos vivos de mães com até 14 anos", "Valor": 14293, "Unidade": "nascidos vivos", "Fonte": "RASEAM 2026 / Sinasc"},
    {"Ano": 2023, "Categoria": "Gravidez infantil", "Indicador": "Nascidos vivos de mães com até 14 anos", "Valor": 13941, "Unidade": "nascidos vivos", "Fonte": "RASEAM 2026 / Sinasc"},
    {"Ano": 2024, "Categoria": "Gravidez infantil", "Indicador": "Nascidos vivos de mães com até 14 anos", "Valor": 11977, "Unidade": "nascidos vivos", "Fonte": "RASEAM 2026 / Sinasc"},

    # VIOLÊNCIAS DOMÉSTICA, SEXUAL E OUTRAS - SINAN
    {"Ano": 2012, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 88668, "Unidade": "notificações", "Fonte": "RASEAM 2013 / SINAN"},
    {"Ano": 2013, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 123476, "Unidade": "notificações", "Fonte": "RASEAM 2026 / SINAN"},
    {"Ano": 2014, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 122222, "Unidade": "notificações", "Fonte": "RASEAM 2026 / SINAN"},
    {"Ano": 2015, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 132909, "Unidade": "notificações", "Fonte": "Ministério da Saúde  / SINAN"},
    {"Ano": 2016, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 145702, "Unidade": "notificações", "Fonte": "Ministério da Saúde  / SINAN"},
    {"Ano": 2017, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 174119, "Unidade": "notificações", "Fonte": "Ministério da Saúde  / SINAN"},
    {"Ano": 2018, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 191136, "Unidade": "notificações", "Fonte": "Ministério da Saúde  / SINAN"},
    {"Ano": 2019, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 199429, "Unidade": "notificações", "Fonte": "Ministério da Saúde  / SINAN"},
    {"Ano": 2020, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 165917, "Unidade": "notificações", "Fonte": "Ministério da Saúde  / SINAN"},
    {"Ano": 2021, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 187413, "Unidade": "notificações", "Fonte": "Ministério da Saúde  / SINAN"},
    {"Ano": 2022, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 219718, "Unidade": "notificações", "Fonte": "Ministério da Saúde  / SINAN"},
    {"Ano": 2023, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 292852, "Unidade": "notificações", "Fonte": "Ministério da Saúde  / SINAN"},
    {"Ano": 2024, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 305961, "Unidade": "notificações", "Fonte": "Ministério da Saúde  / SINAN"},
    {"Ano": 2025, "Categoria": "Violência registrada", "Indicador": "Notificações de violências doméstica, sexual e outras contra mulheres", "Valor": 330782, "Unidade": "notificações", "Fonte": "Ministério da Saúde / SINAN"},

    # ESTUPRO E ESTUPRO DE VULNERÁVEL - MJSP

    {"Ano": 2015, "Categoria": "Violência sexual", "Indicador": "Ocorrências de estupro de mulheres", "Valor": 42575, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2016, "Categoria": "Violência sexual", "Indicador": "Ocorrências de estupro de mulheres", "Valor": 48897, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2017, "Categoria": "Violência sexual", "Indicador": "Ocorrências de estupro de mulheres", "Valor": 53890, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2018, "Categoria": "Violência sexual", "Indicador": "Ocorrências de estupro de mulheres", "Valor": 61814, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2019, "Categoria": "Violência sexual", "Indicador": "Ocorrências de estupro de mulheres", "Valor": 66673, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2020, "Categoria": "Violência sexual", "Indicador": "Ocorrências de estupro de mulheres", "Valor": 58098, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2021, "Categoria": "Violência sexual", "Indicador": "Ocorrências de estupro de mulheres", "Valor": 63406, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2022, "Categoria": "Violência sexual", "Indicador": "Ocorrências de estupro de mulheres", "Valor": 70870, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2023, "Categoria": "Violência sexual", "Indicador": "Ocorrências de estupro de mulheres", "Valor": 77251, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2024, "Categoria": "Violência sexual", "Indicador": "Ocorrências de estupro de mulheres", "Valor": 76976, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2025, "Categoria": "Violência sexual", "Indicador": "Ocorrências de estupro de mulheres", "Valor": 71652, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},

    {"Ano": 2015, "Categoria": "Violência sexual", "Indicador": "Mulheres vítimas de estupro", "Valor": 26438, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2016, "Categoria": "Violência sexual", "Indicador": "Mulheres vítimas de estupro", "Valor": 27555, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2017, "Categoria": "Violência sexual", "Indicador": "Mulheres vítimas de estupro", "Valor": 24255, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2018, "Categoria": "Violência sexual", "Indicador": "Mulheres vítimas de estupro", "Valor": 27778, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2019, "Categoria": "Violência sexual", "Indicador": "Mulheres vítimas de estupro", "Valor": 28924, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2020, "Categoria": "Violência sexual", "Indicador": "Mulheres vítimas de estupro", "Valor": 22372, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2021, "Categoria": "Violência sexual", "Indicador": "Mulheres vítimas de estupro", "Valor": 24433, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2022, "Categoria": "Violência sexual", "Indicador": "Mulheres vítimas de estupro", "Valor": 24637, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2023, "Categoria": "Violência sexual", "Indicador": "Mulheres vítimas de estupro", "Valor": 25986, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2024, "Categoria": "Violência sexual", "Indicador": "Mulheres vítimas de estupro", "Valor": 26295, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2025, "Categoria": "Violência sexual", "Indicador": "Mulheres vítimas de estupro", "Valor": 21742, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},

    {"Ano": 2015, "Categoria": "Violência sexual", "Indicador": "Meninas e mulheres vítimas de estupro de vulnerável", "Valor": 16137, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2016, "Categoria": "Violência sexual", "Indicador": "Meninas e mulheres vítimas de estupro de vulnerável", "Valor": 21342, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2017, "Categoria": "Violência sexual", "Indicador": "Meninas e mulheres vítimas de estupro de vulnerável", "Valor": 29635, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2018, "Categoria": "Violência sexual", "Indicador": "Meninas e mulheres vítimas de estupro de vulnerável", "Valor": 34036, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2019, "Categoria": "Violência sexual", "Indicador": "Meninas e mulheres vítimas de estupro de vulnerável", "Valor": 37749, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2020, "Categoria": "Violência sexual", "Indicador": "Meninas e mulheres vítimas de estupro de vulnerável", "Valor": 35726, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2021, "Categoria": "Violência sexual", "Indicador": "Meninas e mulheres vítimas de estupro de vulnerável", "Valor": 38973, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2022, "Categoria": "Violência sexual", "Indicador": "Meninas e mulheres vítimas de estupro de vulnerável", "Valor": 46233, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2023, "Categoria": "Violência sexual", "Indicador": "Meninas e mulheres vítimas de estupro de vulnerável", "Valor": 51265, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2024, "Categoria": "Violência sexual", "Indicador": "Meninas e mulheres vítimas de estupro de vulnerável", "Valor": 50681, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2025, "Categoria": "Violência sexual", "Indicador": "Meninas e mulheres vítimas de estupro de vulnerável", "Valor": 49910, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},

    {"Ano": 2024, "Categoria": "Feminicídio", "Indicador": "Mulheres foram vítimas de feminicídio, homicídio doloso e lesão corporal seguida de morte", "Valor": 44761, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},
    {"Ano": 2025, "Categoria": "Feminicídio", "Indicador": "Tentativa de feminicídio ou homicídio de mulheres", "Valor": 89334, "Unidade": "vítimas", "Fonte": "RASEAM 2026 / MJSP"},

])

# =====================================================
# PERFIL DA VIOLÊNCIA E PROTEÇÃO INSTITUCIONAL
# RASEAM 2026 / SINAN / IBGE MUNIC
# =====================================================

perfil_violencia = pd.DataFrame([

    # =========================
    # LOCAL DE OCORRÊNCIA
    # =========================
    {
        "Ano": 2025,
        "Categoria": "Local de ocorrência",
        "Indicador": "Residência",
        "Valor": 72.2,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Local de ocorrência",
        "Indicador": "Via pública",
        "Valor": 13.4,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Local de ocorrência",
        "Indicador": "Outros locais",
        "Valor": 7.0,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Local de ocorrência",
        "Indicador": "Bar ou similar",
        "Valor": 2.2,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Local de ocorrência",
        "Indicador": "Comércio ou serviços",
        "Valor": 2.1,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Local de ocorrência",
        "Indicador": "Escola",
        "Valor": 2.0,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },

    # =========================
    # AUTORIA DA VIOLÊNCIA
    # =========================
    {
        "Ano": 2025,
        "Categoria": "Autoria da violência",
        "Indicador": "Parceiro íntimo",
        "Valor": 38.2,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Autoria da violência",
        "Indicador": "Cônjuge",
        "Valor": 20.8,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Autoria da violência",
        "Indicador": "Amigos/conhecidos",
        "Valor": 12.3,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Autoria da violência",
        "Indicador": "Desconhecido(a)",
        "Valor": 9.6,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Autoria da violência",
        "Indicador": "Ex-cônjuge",
        "Valor": 9.5,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Autoria da violência",
        "Indicador": "Mãe",
        "Valor": 9.4,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Autoria da violência",
        "Indicador": "Pai",
        "Valor": 7.9,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Autoria da violência",
        "Indicador": "Namorado(a)",
        "Valor": 5.0,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Autoria da violência",
        "Indicador": "Filho(a)",
        "Valor": 4.2,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },
    {
        "Ano": 2025,
        "Categoria": "Autoria da violência",
        "Indicador": "Irmão(ã)",
        "Valor": 3.2,
        "Unidade": "%",
        "Fonte": "RASEAM 2026 / SINAN"
    },

    # =========================
    # PROTEÇÃO INSTITUCIONAL
    # =========================
    {
        "Ano": 2018,
        "Categoria": "Proteção institucional",
        "Indicador": "Municípios sem nenhum instrumento de proteção",
        "Valor": 70,
        "Unidade": "%",
        "Fonte": "IBGE MUNIC 2018"
    },
    {
        "Ano": 2018,
        "Categoria": "Proteção institucional",
        "Indicador": "Municípios sem nenhum instrumento de justiça",
        "Valor": 90,
        "Unidade": "%",
        "Fonte": "IBGE MUNIC 2018"
    },
    {
        "Ano": 2018,
        "Categoria": "Proteção institucional",
        "Indicador": "Municípios com Conselho Municipal de Direitos da Mulher",
        "Valor": 23.58,
        "Unidade": "%",
        "Fonte": "IBGE MUNIC 2018"
    },
    {
        "Ano": 2018,
        "Categoria": "Proteção institucional",
        "Indicador": "Municípios com Centro Especializado de Atendimento à Mulher",
        "Valor": 6.91,
        "Unidade": "%",
        "Fonte": "IBGE MUNIC 2018"
    },
    {
        "Ano": 2018,
        "Categoria": "Proteção institucional",
        "Indicador": "Municípios com Casas-Abrigo",
        "Valor": 2.41,
        "Unidade": "%",
        "Fonte": "IBGE MUNIC 2018"
    },
    {
        "Ano": 2018,
        "Categoria": "Proteção institucional",
        "Indicador": "Municípios com Delegacia Especializada de Atendimento às Mulheres",
        "Valor": 8.26,
        "Unidade": "%",
        "Fonte": "IBGE MUNIC 2018"
    }
])
# =====================================================
# REPRESENTAÇÃO FEMININA NOS ESPAÇOS DE PODER
# =====================================================

representacao_poder = pd.DataFrame([
    {
        "Ano": 2026,
        "Poder": "Legislativo",
        "Indicador": "Mulheres na Câmara dos Deputados",
        "Valor": 18.0,
        "Unidade": "%",
        "Quantidade_Mulheres": 91,
        "Total_Cadeiras": 513,
        "Fonte": "Câmara dos Deputados / Agência Câmara"
    },
    {
        "Ano": 2026,
        "Poder": "Legislativo",
        "Indicador": "Mulheres no Senado Federal",
        "Valor": 19.7,
        "Unidade": "%",
        "Quantidade_Mulheres": 16,
        "Total_Cadeiras": 81,
        "Fonte": "Senado Federal"
    },
    {
        "Ano": 2026,
        "Poder": "Executivo",
        "Indicador": "Mulheres governadoras",
        "Valor": 7.4,
        "Unidade": "%",
        "Quantidade_Mulheres": 2,
        "Total_Cadeiras": 27,
        "Fonte": "Levantamento contextual"
    },
    {
        "Ano": 2026,
        "Poder": "Judiciário",
        "Indicador": "Mulheres no STF",
        "Valor": 9.1,
        "Unidade": "%",
        "Quantidade_Mulheres": 1,
        "Total_Cadeiras": 11,
        "Fonte": "STF"
    }
])

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

raseam_2026.to_csv(
    os.path.join(PASTA_SAIDA, "raseam_2026_indicadores_violencia.csv"),
    index=False,
    encoding="utf-8-sig",
    sep=";",
    decimal=","
)
perfil_violencia.to_csv(
    os.path.join(PASTA_SAIDA, "perfil_violencia_protecao.csv"),
    index=False,
    encoding="utf-8-sig",
    sep=";",
    decimal=","
)
representacao_poder.to_csv(
    os.path.join(PASTA_SAIDA, "representacao_feminina_poder.csv"),
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
print("- raseam_2026_indicadores_violencia.csv")
print("- perfil_violencia_protecao.csv")
print("- representacao_poder.csv")
