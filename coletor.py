import pandas as pd
from classificador import classificar

BAIRROS = [
    "Santana",
    "Tucuruvi",
    "Casa Verde",
    "Mandaqui",
    "Jardim São Paulo",
    "Tremembé"
]

import pandas as pd

# Exemplo lendo dados de uma fonte CSV
dados = pd.read_csv(
    "novos_leads.csv"
)

leads = []

for _, anuncio in dados.iterrows():

    score = classificar(
        anuncio["descricao"]
    )

    if score >= 50:

        leads.append({

            "Nome": anuncio["nome"],
            "WhatsApp": anuncio["whatsapp"],
            "Bairro": anuncio["bairro"],
            "Valor": anuncio["valor"],
            "Score": score,
            "Status": "Novo"

        })

leads=[]

for anuncio in dados:

    if anuncio["bairro"] in BAIRROS:

        score = classificar(
            anuncio["descricao"]
        )

        if score >= 50:

            anuncio["score"]=score

            leads.append(
                anuncio
            )

df = pd.DataFrame(
    leads
)

print(df)