import streamlit as st
import pandas as pd

# =====================================
# CONFIGURAÇÃO
# =====================================

st.set_page_config(
    page_title="Captador ZN",
    layout="wide"
)

st.title("🏠 Captador ZN")
st.subheader("CRM Imobiliário Zona Norte SP")

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQSjdBGWIbfd-xrk-8YO_zafNu8zZOPdXmMHXc7wcUn0TeYD-uf8_qFNRtk3uhh_wow6yQ8onO2pOzs/pub?output=tsv"

# =====================================
# CARREGA PLANILHA
# =====================================

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

# =====================================
# AJUSTA NOMES
# =====================================

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

# =====================================
# REMOVE COLUNAS ANTIGAS
# =====================================

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

# =====================================
# REMOVE DUPLICADOS
# =====================================

if "WhatsApp" in dados.columns:

    dados = dados.drop_duplicates(
        subset=[
            "WhatsApp",
            "Valor",
            "Bairro"
        ],
        keep="first"
    )

# =====================================
# REGRAS IA
# =====================================

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

# =====================================
# SCORE IA
# =====================================

def calcular_score(row):

    score = 0

    texto = str(
        row.get(
            "Descrição",
            ""
        )
    ).lower()

    bairro = str(
        row.get(
            "Bairro",
            ""
        )
    ).lower()

    valor = float(
        pd.to_numeric(
            row.get(
                "Valor",
                0
            ),
            errors="coerce"
        )
    )

    metragem = float(
        pd.to_numeric(
            row.get(
                "Metragem",
                0
            ),
            errors="coerce"
        )
    )

    quartos = float(
        pd.to_numeric(
            row.get(
                "Quartos",
                0
            ),
            errors="coerce"
        )
    )

    # palavras positivas

    for p in positivas:

        if p in texto:
            score +=15

    # palavras negativas

    for n in negativas:

        if n in texto:
            score -=30

    # bairros

    if bairro in bairros:
        score +=30

    # faixa ideal

    if 450000 <= valor <= 750000:
        score +=40
    else:
        score -=20

    # metragem ideal

    if 50 <= metragem <= 80:
        score +=25
    else:
        score -=10

    # quartos

    if quartos == 2:
        score +=35

    return max(
        score,
        0
    )

dados["Score"] = dados.apply(
    calcular_score,
    axis=1
)

# =====================================
# DEFINE URGÊNCIA
# =====================================

def urgencia(score):

    if score >=100:
        return "🔥 Quente"

    elif score >=60:
        return "🟡 Morno"

    return "❄️ Frio"

dados["Urgência"] = dados[
    "Score"
].apply(
    urgencia
)

# =====================================
# DASHBOARD
# =====================================

st.divider()

c1,c2,c3=st.columns(3)

c1.metric(
    "Total Leads",
    len(dados)
)

quentes=len(
    dados[
        dados["Urgência"]=="🔥 Quente"
    ]
)

c2.metric(
    "Leads Quentes",
    quentes
)

alta=len(
    dados[
        dados["Score"]>=80
    ]
)

c3.metric(
    "Alta Prioridade",
    alta
)

# =====================================
# FILTROS
# =====================================

st.divider()

bairro_filtro=st.selectbox(
    "Filtrar Bairro",
    ["Todos"]+
    list(
        dados["Bairro"]
        .dropna()
        .unique()
    )
)

if bairro_filtro!="Todos":

    dados=dados[
        dados["Bairro"]==
        bairro_filtro
    ]

# =====================================
# TABELA
# =====================================

st.divider()

st.subheader(
    "📋 Leads"
)

st.dataframe(
    dados,
    use_container_width=True
)

# =====================================
# WHATSAPP
# =====================================

if "WhatsApp" in dados.columns:

    dados["WhatsApp Link"]=dados[
        "WhatsApp"
    ].apply(
        lambda x:
        f"https://wa.me/55{str(x).replace('.0','')}"
    )

    lead=st.selectbox(
        "Selecionar lead",
        dados["Nome"]
    )

    selecionado=dados[
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