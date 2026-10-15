import json
import os
import random
import xml.etree.ElementTree as ET
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def carregar_dados(caminho_arquivo="data.json"):
    with open(caminho_arquivo, "r", encoding="utf-8") as file:
        return json.load(file)


def sortear_produtos(produtos):
    alimenticios = [p for p in produtos if p["categoria"] == "alimentício"]
    nao_alimenticios = [
        p for p in produtos if p["categoria"] == "não-alimentício"
    ]

    prod_alim = random.sample(alimenticios, 1)
    prod_nao_alim = random.sample(nao_alimenticios, 2)

    selecionados = prod_alim + prod_nao_alim

    total_desejado = random.randint(3, 10)
    qtd_restante = total_desejado - 3

    if qtd_restante > 0:
        restantes = [p for p in produtos if p not in selecionados]
        selecionados.extend(random.sample(restantes, qtd_restante))

    random.shuffle(selecionados)
    return selecionados


def emitirNFCe(xml_str):
    return {"status": 200, "xml": xml_str}


@app.post("/api/gerar-compra/")
def gerar_compra():
    dados = carregar_dados("data.json")
    supermercado = random.choice(dados["supermercados"])

    root = ET.Element("nfce")

    emitente = ET.SubElement(root, "emitente")
    ET.SubElement(emitente, "nome").text = supermercado["nome"]
    ET.SubElement(emitente, "cnpj").text = supermercado["cnpj"]

    itens_elem = ET.SubElement(root, "itens")

    produtos_sorteados = sortear_produtos(supermercado["produtos"])
    valor_total_compra = 0.0

    for prod in produtos_sorteados:
        qtd = random.randint(1, 6)
        preco_unitario = float(prod["preco_unitario"])
        valor_total_produto = round(preco_unitario * qtd, 2)
        valor_total_compra += valor_total_produto

        item_elem = ET.SubElement(itens_elem, "item")
        ET.SubElement(item_elem, "nome").text = prod["nome"]
        ET.SubElement(item_elem, "categoria").text = prod["categoria"]
        ET.SubElement(item_elem, "quantidade").text = str(qtd)
        ET.SubElement(
            item_elem, "valorUnitario"
        ).text = f"{preco_unitario:.2f}"
        ET.SubElement(
            item_elem, "valorTotal"
        ).text = f"{valor_total_produto:.2f}"

    ET.SubElement(
        root, "totalCompra"
    ).text = f"{round(valor_total_compra, 2):.2f}"

    formas_pagamento = [
        "Em espécie",
        "Cartão de crédito",
        "Cartão de débito",
        "Pix",
    ]
    ET.SubElement(root, "formaPagamento").text = random.choice(
        formas_pagamento
    )

    ET.indent(root, space="  ")
    xml_content = ET.tostring(root, encoding="utf-8").decode("utf-8")

    resposta = emitirNFCe(xml_content)

    return Response(content=resposta["xml"], media_type="application/xml")


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)