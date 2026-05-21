import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Captador ZN",
    layout="wide"
)

st.title("🏠 Captador ZN")
st.subheader("CRM Imobiliário - Zona Norte SP")

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQSjdBGWIbfd-xrk-8YO_zafNu8zZOPdXmMHXc7wcUn0TeYD-uf8_qFNRtk3uhh_wow6yQ8onO2pOzs/pub?output=tsv"

try:
    dados = pd.read_csv(
        URL_PLANILHA,
        sep="\t"
    )

except Exception as e:
    st.error(f"Erro ao carregar planilha: {e}")
    st.stop()

# Ajusta nomes automaticamente
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

    elif "score" in nome:
        mapa[coluna] = "Score"

    elif "urg" in nome:
        mapa[coluna] = "Urgencia"

dados = dados.rename(columns=mapa)
st.sidebar.title("⚙️ Configuração Captador")

st.sidebar.subheader("Palavras que aumentam score")

positivas = st.sidebar.text_area(
    "Separar por vírgula",
    "direto proprietário,particular,sem corretor,urgente,preciso vender,mudança,venda rápida,negociável"
)

st.sidebar.subheader("Palavras que reduzem score")

negativas = st.sidebar.text_area(
    "Separar por vírgula",
    "imobiliária,corretor,creci,consultor imobiliário"
)

st.sidebar.subheader("Bairros prioritários")

bairros = st.sidebar.text_area(
    "Separar por vírgula",
    "Santana,Tucuruvi,Casa Verde,Mandaqui"
)

positivas = [x.strip().lower() for x in positivas.split(",")]

negativas = [x.strip().lower() for x in negativas.split(",")]

bairros = [x.strip().lower() for x in bairros.split(",")]
st.divider()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Leads",
    len(dados)
)

quentes = 0

if "Urgencia" in dados.columns:
    quentes = len(
        dados[
            dados["Urgencia"]=="🔥 Quente"
        ]
    )

c2.metric(
    "Leads Quentes",
    quentes
)

alta = 0

if "Score" in dados.columns:

    dados["Score"] = pd.to_numeric(
        dados["Score"],
        errors="coerce"
    )

    alta = len(
        dados[
            dados["Score"]>=80
        ]
    )

c3.metric(
    "Alta Prioridade",
    alta
)

def calcular_score(texto,bairro):

    score = 0

    texto = str(texto).lower()
    bairro = str(bairro).lower()

    for p in positivas:
        if p in texto:
            score += 20

    for n in negativas:
        if n in texto:
            score -= 20

    if bairro in bairros:
        score += 15

    return max(score,0)


if "Descrição" in dados.columns and "Bairro" in dados.columns:

    dados["Score IA"] = dados.apply(
        lambda x:
        calcular_score(
            x["Descrição"],
            x["Bairro"]
        ),
        axis=1
    )

st.divider()

# Dashboard de conversão
st.divider()

st.subheader("📈 Dashboard de Conversão")

c1, c2, c3 = st.columns(3)

visitas = 0
captacoes = 0

if "Status" in dados.columns:

    visitas = len(
        dados[
            dados["Status"]=="Visita"
        ]
    )

    captacoes = len(
        dados[
            dados["Status"]=="Venda"
        ]
    )

total = len(dados)

taxa = 0

if total > 0:
    taxa = round(
        (captacoes/total)*100,
        1
    )

c1.metric(
    "📅 Visitas",
    visitas
)

c2.metric(
    "🏠 Captações",
    captacoes
)

c3.metric(
    "📊 Taxa Fechamento",
    f"{taxa}%"
)

st.divider()

# Botão WhatsApp
st.subheader("📋 Leads")

if "WhatsApp" in dados.columns:

    dados["WhatsApp Link"] = dados.apply(
        lambda x:
        f"https://wa.me/55{str(x['WhatsApp']).replace('.0','')}"
        if pd.notnull(x["WhatsApp"])
        else "",
        axis=1
    )

st.dataframe(
    dados,
    use_container_width=True
)

st.subheader("📲 Abrir conversa")

lead = st.selectbox(
    "Selecione o lead",
    dados["Nome"]
)

selecionado = dados[
    dados["Nome"]==lead
].iloc[0]

if st.button("Abrir WhatsApp"):

    st.markdown(
        f"""
        <meta http-equiv="refresh"
        content="0; url={selecionado['WhatsApp Link']}">
        """,
        unsafe_allow_html=True
    )