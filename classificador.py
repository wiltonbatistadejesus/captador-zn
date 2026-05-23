import requests
import time

WEBHOOK = "https://hook.us2.make.com/7nv6skeuu5cwybd8yaylpy915y7mbc34"

leads = [

    {
        "nome":"Carlos",
        "telefone":"11987654321",
        "bairro":"Santana",
        "quartos":2,
        "valor":620000,
        "metragem":67,
        "descricao":"Particular. Preciso vender urgente",
        "fonte":"Robô"
    },

    {
        "nome":"Marcos",
        "telefone":"11998765432",
        "bairro":"Tucuruvi",
        "quartos":2,
        "valor":700000,
        "metragem":72,
        "descricao":"Direto proprietário. Mudança",
        "fonte":"Robô"
    }

]

for lead in leads:

    try:

        resposta = requests.post(
            WEBHOOK,
            json=lead,
            timeout=15
        )

        print(
            f"Enviado: {lead['nome']} | Status: {resposta.status_code}"
        )

    except Exception as erro:

        print(
            f"Erro: {erro}"
        )

    time.sleep(2)