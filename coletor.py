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

dados = [

{
"titulo":"Apartamento particular Santana",
"descricao":"Direto com proprietário. Preciso vender",
"bairro":"Santana",
"valor":"680000"
},

{
"titulo":"Apartamento imobiliária",
"descricao":"Imobiliária especializada",
"bairro":"Tucuruvi",
"valor":"520000"
}

]

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