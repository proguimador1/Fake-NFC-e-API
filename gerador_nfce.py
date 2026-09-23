import random
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

produtos_alimenticios = [
    {"nome": "Arroz Agulhinha 5kg", "preco": 22.50},
    {"nome": "Feijão Preto 1kg", "preco": 7.80},
    {"nome": "Açúcar Refinado 1kg", "preco": 4.20},
    {"nome": "Café Torrado e Moído 500g", "preco": 16.90},
    {"nome": "Óleo de Soja 900ml", "preco": 6.50},
    {"nome": "Leite Integral 1L", "preco": 4.99},
    {"nome": "Macarrão Espaguete 500g", "preco": 3.80},
    {"nome": "Sal Refinado 1kg", "preco": 2.10},
    {"nome": "Farinha de Trigo 1kg", "preco": 4.50},
    {"nome": "Manteiga com Sal 200g", "preco": 9.90},
    {"nome": "Biscoito Recheado 135g", "preco": 3.20},
    {"nome": "Chocolate ao Leite 80g", "preco": 5.50},
    {"nome": "Suco de Laranja 1L", "preco": 7.50},
    {"nome": "Refrigerante de Guaraná 2L", "preco": 8.90},
    {"nome": "Água Mineral sem Gás 500ml", "preco": 2.00},
    {"nome": "Pão de Forma 450g", "preco": 7.20},
    {"nome": "Queijo Mussarela 100g", "preco": 5.40},
    {"nome": "Presunto Cozido 100g", "preco": 4.10},
    {"nome": "Iogurte Natural 170g", "preco": 3.10},
    {"nome": "Maçã Fuji 1kg", "preco": 8.90},
    {"nome": "Banana Prata 1kg", "preco": 6.50},
    {"nome": "Tomate Longa Vida 1kg", "preco": 7.80},
    {"nome": "Cebola Nacional 1kg", "preco": 5.20},
    {"nome": "Batata Monalisa 1kg", "preco": 6.00},
    {"nome": "Peito de Frango 1kg", "preco": 18.90},
]

produtos_nao_alimenticios = [
    {"nome": "Sabão em Pó 1kg", "preco": 12.50},
    {"nome": "Detergente Líquido 500ml", "preco": 2.40},
    {"nome": "Desinfetante Pinho 1L", "preco": 6.80},
    {"nome": "Amaciante de Roupas 2L", "preco": 14.90},
    {"nome": "Papel Higiênico Folha Dupla (8 un)", "preco": 15.90},
    {"nome": "Sabonete em Barra 90g", "preco": 2.50},
    {"nome": "Shampoo 350ml", "preco": 14.50},
    {"nome": "Condicionador 350ml", "preco": 15.80},
    {"nome": "Creme Dental 90g", "preco": 4.20},
    {"nome": "Escova de Dentes", "preco": 6.90},
    {"nome": "Esponja de Aço (cx c/ 8)", "preco": 4.80},
    {"nome": "Esponja Multiuso", "preco": 3.50},
    {"nome": "Sacos para Lixo 50L (10 un)", "preco": 9.90},
    {"nome": "Água Sanitária 1L", "preco": 3.80},
    {"nome": "Limpador Multiuso 500ml", "preco": 5.90},
    {"nome": "Toalha de Papel (2 rolos)", "preco": 6.50},
    {"nome": "Fio Dental 50m", "preco": 8.90},
    {"nome": "Lâmina de Barbear", "preco": 12.00},
    {"nome": "Desodorante Aerossol 150ml", "preco": 13.90},
    {"nome": "Álcool em Gel 70% 500ml", "preco": 8.50},
    {"nome": "Guardanapo de Papel", "preco": 3.20},
    {"nome": "Fita Adesiva Transparente", "preco": 4.50},
    {"nome": "Pilha AA (pct c/ 4)", "preco": 16.00},
    {"nome": "Lâmpada LED 9W", "preco": 9.90},
    {"nome": "Fósforo (pct c/ 10)", "preco": 5.50},
]


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