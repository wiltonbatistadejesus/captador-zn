import streamlit as st
import pandas as pd
from flask import Flask, request, jsonify
import threading
from datetime import datetime

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Captador ZN",
    layout="wide"
)

st.title("🏠 Captador ZN")
st.subheader("CRM Imobiliário Zona Norte")

URL_PLANILHA = "COLE_SUA_PLANILHA_PUBLICADA_AQUI"

# =========================
# API RECEBIMENTO ROBÔ
# =========================

app = Flask(__name__)

LEADS_RECEBIDOS = []

@app.route("/captar", methods=["POST"])
def captar():

    lead = request.json

    LEADS_RECEBIDOS.append({
        "Data":datetime.now(),
        "Nome":lead.get("nome",""),
        "WhatsApp":lead.get("telefone",""),
        "Bairro":lead.get("bairro",""),
        "Valor":lead.get("valor",0),
        "Metragem":lead.get("metragem",0),
        "Quartos":lead.get("quartos",0),
        "Descrição":lead.get("descricao",""),
        "Link":lead.get("link",""),
        "Fonte":lead.get("fonte","Robô")
    })

    return jsonify({
        "status":"ok"
    })

def iniciar_api():
    app.run(
        host="0.0.0.0",
        port=5000
    )

threading.Thread(
    target=iniciar_api,
    daemon=True
).start()

# =========================
# CARREGA PLANILHA
# =========================

try:

    dados = pd.read_csv(
        URL_PLANILHA,
        sep="\t"
    )

except:

    dados = pd.DataFrame()

# =========================
# INSERE LEADS ROBÔ
# =========================

if len(LEADS_RECEBIDOS)>0:

    novos = pd.DataFrame(
        LEADS_RECEBIDOS
    )

    dados = pd.concat(
        [dados,novos],
        ignore_index=True
    )

# =========================
# REMOVE DUPLICADOS
# =========================

if "WhatsApp" in dados.columns:

    dados = dados.drop_duplicates(
        subset=[
            "WhatsApp",
            "Valor",
            "Bairro"
        ],
        keep="first"
    )

# =========================
# CONFIG IA
# =========================

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

# =========================
# SCORE
# =========================

def calcular_score(row):

    score = 0

    texto = str(
        row.get(
            "Descrição",""
        )
    ).lower()

    bairro = str(
        row.get(
            "Bairro",""
        )
    ).lower()

    valor = pd.to_numeric(
        row.get(
            "Valor",0
        ),
        errors="coerce"
    )

    metragem = pd.to_numeric(
        row.get(
            "Metragem",0
        ),
        errors="coerce"
    )

    quartos = pd.to_numeric(
        row.get(
            "Quartos",0
        ),
        errors="coerce"
    )

    for palavra in positivas:

        if palavra in texto:
            score +=20

    for palavra in negativas:

        if palavra in texto:
            score -=20

    if bairro in bairros:
        score +=30

    if 450000 <= valor <= 750000:
        score +=40

    if 50 <= metragem <=80:
        score +=25

    if quartos == 2:
        score +=35

    return max(
        score,
        0
    )

# =========================
# CALCULA SCORE
# =========================

dados["Score IA"] = dados.apply(
    calcular_score,
    axis=1
)

# =========================
# DEFINE URGÊNCIA
# =========================

def urgencia(score):

    if score >=100:
        return "🔥 Quente"

    elif score >=60:
        return "🟡 Morno"

    return "❄️ Frio"

dados["Urgencia"] = dados[
    "Score IA"
].apply(
    urgencia
)

# =========================
# DASHBOARD
# =========================

st.divider()

c1,c2,c3=st.columns(3)

c1.metric(
    "Leads",
    len(dados)
)

quentes=len(
    dados[
        dados["Urgencia"]=="🔥 Quente"
    ]
)

c2.metric(
    "Quentes",
    quentes
)

alta=len(
    dados[
        dados["Score IA"]>=80
    ]
)

c3.metric(
    "Alta prioridade",
    alta
)

st.divider()

st.subheader(
    "📋 Leads"
)

st.dataframe(
    dados,
    use_container_width=True
)

# =========================
# WHATSAPP
# =========================

if "WhatsApp" in dados.columns:

    dados["Link WhatsApp"] = dados[
        "WhatsApp"
    ].apply(
        lambda x:
        f"https://wa.me/55{str(x).replace('.0','')}"
    )

    lead = st.selectbox(
        "Selecionar lead",
        dados["Nome"]
    )

    selecionado = dados[
        dados["Nome"]==lead
    ].iloc[0]

    if st.button(
        "Abrir WhatsApp"
    ):

        st.markdown(
            f"""
            <meta http-equiv="refresh"
            content="0; url={selecionado['Link WhatsApp']}">
            """,
            unsafe_allow_html=True
        )