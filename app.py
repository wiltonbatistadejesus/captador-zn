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

st.divider()

st.subheader("📋 Leads")

st.dataframe(
    dados,
    use_container_width=True
)