import fitz
import re


def find_references(pdf: str) -> list:
    """
    Récupère les références de la bibliographie du document.
    :param pdf: Le document
    :return: Une liste contenant le texte de chaque bloc de la bibliographie
    """
    doc = fitz.open(pdf)
    res = []
    found = False
    for i in range(len(doc)):
        for block in doc[i].get_text("blocks"):
            if re.match(r"\Areferences(?: |\n|)+", block[4].lower()):
                found = True
            elif found:
                if not re.match(r"\A[0-9]+(?:\n|)$", block[4]):
                    tmp_ref = block[4].replace("- \n", "")
                    tmp_ref = tmp_ref.replace("-\n", "")
                    tmp_ref = tmp_ref.replace("\n", " ")
                    res.append(tmp_ref)
    return res