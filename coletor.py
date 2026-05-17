def classificar(anuncio):

    score = 0

    texto = anuncio.lower()

    regras = {
        "direto com proprietário":40,
        "particular":30,
        "sem corretor":25,
        "trato direto":15,
        "não aceito imobiliária":20,
        "imobiliária":-40
    }

    for palavra, valor in regras.items():

        if palavra in texto:
            score += valor

    score = max(0,min(score,100))

    return score