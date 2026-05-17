import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Captador ZN", layout="wide")

st.title("🏠 Captador ZN — Versão 2")
st.subheader("Captação de proprietários - Zona Norte SP")

arquivo="leads.csv"

if not os.path.exists(arquivo):
    pd.DataFrame(columns=[
        "Data",
        "Nome",
        "WhatsApp",
        "Bairro",
        "Valor",
        "Metragem",
        "Score",
        "Status"
    ]).to_csv(arquivo,index=False)

col1,col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome")
    whatsapp = st.text_input("WhatsApp")

    bairro = st.selectbox(
        "Bairro",
        ["Santana","Tucuruvi","Casa Verde",
        "Mandaqui","Jardim São Paulo","Tremembé"]
    )

with col2:
    valor = st.text_input("Valor do imóvel")
    metragem = st.text_input("Metragem")

texto = st.text_area("Cole o anúncio")

if st.button("Analisar e salvar lead"):

    score=0
    t=texto.lower()

    regras = {
        "direto com proprietário":40,
        "particular":30,
        "sem corretor":25,
        "trato direto":15,
        "imobiliária":-40
    }

    for k,v in regras.items():
        if k in t:
            score += v

    score=max(0,min(score,100))

    novo = pd.DataFrame([{
        "Data":datetime.now().strftime("%d/%m/%Y"),
        "Nome":nome,
        "WhatsApp":whatsapp,
        "Bairro":bairro,
        "Valor":valor,
        "Metragem":metragem,
        "Score":score,
        "Status":"Novo"
    }])

    banco = pd.read_csv(arquivo)

    banco = pd.concat(
        [banco,novo],
        ignore_index=True
    )

    banco.to_csv(
        arquivo,
        index=False
    )

    st.success("Lead salvo")

    st.metric(
        "Score",
        score
    )

st.divider()

st.subheader("📋 Banco de Leads")

dados = pd.read_csv(arquivo)

st.dataframe(
    dados,
    use_container_width=True
)