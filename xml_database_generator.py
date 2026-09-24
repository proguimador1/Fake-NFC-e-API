import os
import json
import random
import xml.etree.ElementTree as ET

random.seed(42)

produtos = []

with open("products.json", "r") as file:
    produtos = json.load(file)

    produtos = produtos["produtos_alimenticios"] + produtos["produtos_nao_alimenticios"]

pasta_destino = "notas_fiscais_ficticias"
os.makedirs(pasta_destino, exist_ok=True)

total_arquivos = 2000

for i in range(1, total_arquivos + 1):
    root = ET.Element("NFCeFicticia")

    aviso = ET.SubElement(root, "aviso")
    aviso.text = (
        "DOCUMENTO FICTÍCIO – USO ACADÊMICO – NÃO É NOTA FISCAL VÁLIDA"
    )

    numero = ET.SubElement(root, "numero")
    numero.text = str(i)

    data = ET.SubElement(root, "data")
    data.text = "2026-03-23"

    emitente = ET.SubElement(root, "emitente_ficticio")
    emitente.text = "Supermercado Modelo Fictício LTDA"

    itens_elem = ET.SubElement(root, "itens")

    qtd_itens = random.randint(2, 10)
    produtos_selecionados = random.sample(produtos, qtd_itens)

    valor_total_nota = 0.0

    for prod in produtos_selecionados:
        item_elem = ET.SubElement(itens_elem, "item")

        qtd = random.randint(1, 5)
        v_unit = prod["preco"]
        v_total = round(v_unit * qtd, 2)
        valor_total_nota += v_total

        p_nome = ET.SubElement(item_elem, "produto")
        p_nome.text = prod["nome"]

        p_qtd = ET.SubElement(item_elem, "quantidade")
        p_qtd.text = str(qtd)

        p_vunit = ET.SubElement(item_elem, "valor_unitario")
        p_vunit.text = f"{v_unit:.2f}"

        p_vtot = ET.SubElement(item_elem, "valor_total")
        p_vtot.text = f"{v_total:.2f}"

    total_elem = ET.SubElement(root, "total")
    total_elem.text = f"{round(valor_total_nota, 2):.2f}"

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")

    nome_arquivo = f"nota_{i:04d}.xml"
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

    tree.write(caminho_arquivo, encoding="utf-8", xml_declaration=True)

caminho_absoluto = os.path.abspath(pasta_destino)
print(
    f"Foram gerados {total_arquivos} arquivos XML na pasta: {caminho_absoluto}"
)