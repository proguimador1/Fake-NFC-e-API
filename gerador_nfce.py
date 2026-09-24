import random
import json
import xml.etree.ElementTree as ET
from datetime import datetime
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

produtos_alimenticios = []
produtos_nao_alimenticios = []

with open("products.json", "r") as file:
    produtos = json.load(file)

    produtos_alimenticios = produtos["produtos_alimenticios"]
    produtos_nao_alimenticios = produtos["produtos_nao_alimenticios"]


@app.post("/api/gerar-compra/")
def gerar_compra():
    root = ET.Element("NFCeFicticia")

    aviso = ET.SubElement(root, "aviso")
    aviso.text = "DOCUMENTO FICTÍCIO – USO ACADÊMICO – NÃO É NOTA FISCAL VÁLIDA"

    numero = ET.SubElement(root, "numero")
    numero.text = str(random.randint(1000, 999999))

    data = ET.SubElement(root, "data")
    data.text = datetime.now().strftime("%Y-%m-%d")

    emitente = ET.SubElement(root, "emitente_ficticio")
    emitente.text = "Supermercado Modelo Fictício LTDA"

    itens_elem = ET.SubElement(root, "itens")

    qtd_itens = random.randint(2, 10)

    prod_alim = random.choice(produtos_alimenticios)
    prod_nao_alim = random.choice(produtos_nao_alimenticios)

    produtos_selecionados = [prod_alim, prod_nao_alim]

    if qtd_itens > 2:
        todos_produtos = produtos_alimenticios + produtos_nao_alimenticios
        restantes = [p for p in todos_produtos if p not in produtos_selecionados]
        produtos_selecionados.extend(random.sample(restantes, qtd_itens - 2))

    random.shuffle(produtos_selecionados)

    valor_total_nota = 0.0

    for prod in produtos_selecionados:
        item_elem = ET.SubElement(itens_elem, "item")

        qtd = random.randint(1, 5)
        v_unit = prod["preco"]
        v_total = round(v_unit * qtd, 2)
        valor_total_nota += v_total

        categoria = "alimenticio" if prod in produtos_alimenticios else "nao_alimenticio"

        p_nome = ET.SubElement(item_elem, "produto")
        p_nome.text = prod["nome"]

        p_cat = ET.SubElement(item_elem, "categoria")
        p_cat.text = categoria

        p_qtd = ET.SubElement(item_elem, "quantidade")
        p_qtd.text = str(qtd)

        p_vunit = ET.SubElement(item_elem, "valor_unitario")
        p_vunit.text = f"{v_unit:.2f}"

        p_vtot = ET.SubElement(item_elem, "valor_total")
        p_vtot.text = f"{v_total:.2f}"

    total_elem = ET.SubElement(root, "total")
    total_elem.text = f"{round(valor_total_nota, 2):.2f}"

    ET.indent(root, space="  ")
    xml_content = ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

    return Response(content=xml_content, media_type="application/xml")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)