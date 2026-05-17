import streamlit as st

st.set_page_config(page_title="Captador ZN")

st.title("🏠 Captador ZN")
st.subheader("Captação de proprietários - Zona Norte SP")

bairro = st.selectbox(
    "Bairro",
    ["Santana","Tucuruvi","Casa Verde","Mandaqui","Jardim São Paulo","Tremembé"]
)

texto = st.text_area("Cole o texto do anúncio")

if st.button("Analisar"):
    score = 0
    t = texto.lower()

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

    score = max(0,min(score,100))

    st.metric("Score", score)

    if score >= 80:
        st.success("Provável proprietário")
    elif score >= 50:
        st.warning("Revisar manualmente")
    else:
        st.error("Baixa probabilidade")