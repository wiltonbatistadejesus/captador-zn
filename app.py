import streamlit as st
import pandas as pd

# ======================================
# CONFIGURAÇÃO
# ======================================

st.set_page_config(
    page_title="Captador ZN",
    layout="wide"
)

st.title("🏠 Captador ZN")
st.subheader("CRM Imobiliário Zona Norte")

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQSjdBGWIbfd-xrk-8YO_zafNu8zZOPdXmMHXc7wcUn0TeYD-uf8_qFNRtk3uhh_wow6yQ8onO2pOzs/pub?output=tsv"

# ======================================
# CARREGAR PLANILHA
# ======================================

try:

    dados = pd.read_csv(
        URL_PLANILHA,
        sep="\t"
    )

except Exception as e:

    st.error(
        f"Erro ao carregar planilha: {e}"
    )

    st.stop()

# ======================================
# AJUSTAR NOMES DE COLUNAS
# ======================================

mapa = {}

for coluna in dados.columns:

    nome = coluna.lower()

    if "nome" in nome:
        mapa[coluna] = "Nome"

    elif "whatsapp" in nome:
        mapa[coluna] = "WhatsApp"

    elif "bairro" in nome:
        mapa[coluna] = "Bairro"

    elif "valor" in nome:
        mapa[coluna] = "Valor"

    elif "metragem" in nome:
        mapa[coluna] = "Metragem"

    elif "descr" in nome:
        mapa[coluna] = "Descrição"

    elif "status" in nome:
        mapa[coluna] = "Status"

    elif "quart" in nome:
        mapa[coluna] = "Quartos"

    elif "fonte" in nome:
        mapa[coluna] = "Fonte"

dados = dados.rename(
    columns=mapa
)

# ======================================
# GARANTIR COLUNAS
# ======================================

colunas_necessarias = [
    "Nome",
    "WhatsApp",
    "Bairro",
    "Valor",
    "Metragem",
    "Descrição",
    "Quartos",
    "Fonte",
    "Status"
]

for coluna in colunas_necessarias:

    if coluna not in dados.columns:

        dados[coluna] = ""

# ======================================
# REMOVE COLUNAS ANTIGAS
# ======================================

for coluna in [
    "Score",
    "Score IA",
    "Urgência",
    "Urgencia"
]:

    if coluna in dados.columns:

        dados = dados.drop(
            columns=[coluna]
        )

# ======================================
# REMOVE DUPLICADOS
# ======================================

dados = dados.drop_duplicates(
    subset=[
        "WhatsApp",
        "Valor",
        "Bairro"
    ],
    keep="first"
)

# ======================================
# REGRAS IA
# ======================================

positivas = [
    "direto proprietário",
    "particular",
    "urgente",
    "preciso vender",
    "mudança",
    "venda rápida",
    "negociável"
]

negativas = [
    "imobiliária",
    "corretor",
    "creci"
]

bairros = [
    "santana",
    "tucuruvi",
    "mandaqui",
    "parada inglesa",
    "casa verde"
]

# ======================================
# SCORE IA
# ======================================

def calcular_score(row):

    score = 0

    texto = str(
        row["Descrição"]
    ).lower()

    bairro = str(
        row["Bairro"]
    ).lower()

    valor = pd.to_numeric(
        row["Valor"],
        errors="coerce"
    )

    metragem = pd.to_numeric(
        row["Metragem"],
        errors="coerce"
    )

    quartos = pd.to_numeric(
        row["Quartos"],
        errors="coerce"
    )

    if pd.isna(valor):
        valor = 0

    if pd.isna(metragem):
        metragem = 0

    if pd.isna(quartos):
        quartos = 0

    # palavras positivas

    for p in positivas:

        if p in texto:
            score += 15

    # palavras negativas

    for n in negativas:

        if n in texto:
            score -= 30

    # bairros prioritários

    if bairro in bairros:
        score += 30

    # faixa de preço ideal

    if 450000 <= valor <= 750000:
        score += 40
    else:
        score -= 20

    # metragem ideal

    if 50 <= metragem <= 80:
        score += 25
    else:
        score -= 10

    # quartos

    if quartos == 2:
        score += 35

    return max(score,0)

dados["Score"] = dados.apply(
    calcular_score,
    axis=1
)

# ======================================
# URGÊNCIA
# ======================================

def urgencia(score):

    if score >= 100:
        return "🔥 Quente"

    elif score >= 60:
        return "🟡 Morno"

    return "❄️ Frio"

dados["Urgência"] = dados[
    "Score"
].apply(
    urgencia
)

# ======================================
# DASHBOARD
# ======================================

st.divider()

c1,c2,c3=st.columns(3)

c1.metric(
    "Total Leads",
    len(dados)
)

c2.metric(
    "Leads Quentes",
    len(
        dados[
            dados["Urgência"]=="🔥 Quente"
        ]
    )
)

c3.metric(
    "Alta Prioridade",
    len(
        dados[
            dados["Score"]>=80
        ]
    )
)

# ======================================
# FILTROS
# ======================================

st.divider()

bairro = st.selectbox(
    "Filtrar Bairro",
    ["Todos"] +
    list(
        dados["Bairro"]
        .dropna()
        .unique()
    )
)

if bairro != "Todos":

    dados = dados[
        dados["Bairro"] == bairro
    ]

# ======================================
# TABELA
# ======================================

st.divider()

st.subheader(
    "📋 Leads"
)

st.dataframe(
    dados,
    use_container_width=True
)

# ======================================
# WHATSAPP
# ======================================

dados["WhatsApp Link"] = dados[
    "WhatsApp"
].apply(
    lambda x:
    f"https://wa.me/55{str(x).replace('.0','')}"
)

lead = st.selectbox(
    "Selecionar Lead",
    dados["Nome"]
)

selecionado = dados[
    dados["Nome"]==lead
].iloc[0]

if st.button(
    "📲 Abrir WhatsApp"
):

    st.markdown(
        f"""
        <meta http-equiv="refresh"
        content="0;url={selecionado['WhatsApp Link']}">
        """,
        unsafe_allow_html=True
    )