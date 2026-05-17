import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Captador ZN", layout="wide")

st.title("🏠 Captador ZN — CRM Imobiliário")
st.subheader("Captação de proprietários - Zona Norte SP")

arquivo = "leads.csv"

# Cria arquivo inicial
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
    ]).to_csv(arquivo, index=False)

# Formulário
col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome")
    whatsapp = st.text_input("WhatsApp")

    bairro = st.selectbox(
        "Bairro",
        [
            "Santana",
            "Tucuruvi",
            "Casa Verde",
            "Mandaqui",
            "Jardim São Paulo",
            "Tremembé"
        ]
    )

with col2:
    valor = st.text_input("Valor do imóvel")
    metragem = st.text_input("Metragem")

texto = st.text_area("Cole o texto do anúncio")

# Salvar lead
if st.button("Analisar e salvar lead"):

    score = 0
    t = texto.lower()

    regras = {
        "direto com proprietário":40,
        "particular":30,
        "sem corretor":25,
        "trato direto":15,
        "imobiliária":-40
    }

    for k, v in regras.items():
        if k in t:
            score += v

    score = max(0, min(score,100))

    novo = pd.DataFrame([{
        "Data": datetime.now().strftime("%d/%m/%Y"),
        "Nome": nome,
        "WhatsApp": whatsapp,
        "Bairro": bairro,
        "Valor": valor,
        "Metragem": metragem,
        "Score": score,
        "Status": "Novo"
    }])

    banco = pd.read_csv(arquivo)

    banco = pd.concat(
        [banco, novo],
        ignore_index=True
    )

    banco.to_csv(
        arquivo,
        index=False
    )

    st.success("Lead salvo")
    st.metric("Score", score)

# Carrega dados
dados = pd.read_csv(arquivo)

st.divider()

# Atualização de status
st.subheader("🔄 Atualizar status")

if len(dados) > 0:

    lead = st.selectbox(
        "Selecione o lead",
        dados["Nome"]
    )

    novo_status = st.selectbox(
        "Mover para",
        [
            "Novo",
            "Contatado",
            "Visita",
            "Captação",
            "Venda"
        ]
    )

    if st.button("Atualizar Status"):

        dados.loc[
            dados["Nome"] == lead,
            "Status"
        ] = novo_status

        dados.to_csv(
            arquivo,
            index=False
        )

        st.success("Status atualizado")
        st.rerun()

st.divider()

# CRM Visual
st.subheader("🏢 CRM Imobiliário")

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.markdown("### 📌 Novos")
    st.dataframe(
        dados[dados["Status"]=="Novo"][["Nome","Bairro","Valor"]],
        hide_index=True
    )

with c2:
    st.markdown("### 📞 Contatados")
    st.dataframe(
        dados[dados["Status"]=="Contatado"][["Nome","Bairro","Valor"]],
        hide_index=True
    )

with c3:
    st.markdown("### 🏠 Visitas")
    st.dataframe(
        dados[dados["Status"]=="Visita"][["Nome","Bairro","Valor"]],
        hide_index=True
    )

with c4:
    st.markdown("### ✍️ Captação")
    st.dataframe(
        dados[dados["Status"]=="Captação"][["Nome","Bairro","Valor"]],
        hide_index=True
    )

with c5:
    st.markdown("### 💰 Venda")
    st.dataframe(
        dados[dados["Status"]=="Venda"][["Nome","Bairro","Valor"]],
        hide_index=True
    )