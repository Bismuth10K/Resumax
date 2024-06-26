import re

import fitz


def find_references(pdf: str) -> list:
	"""
	Récupère les références de la bibliographie du document.

	Args:
		pdf: Le chemin pour le document

	Returns: Une liste contenant le texte de chaque bloc de la bibliographie
	"""

	doc = fitz.open(pdf)
	res = []
	found = False
	for i in range(len(doc)):
		for block in doc[i].get_text("blocks"):
			if re.match(r"\A(?: |\n|[a-z0-9.]|)+references(?: |)*", block[4].lower()):
				found = True
			elif found:
				if not re.match(r"\A[0-9]+(?:\n|)$", block[4]):
					tmp_ref = block[4].replace("- \n", "")
					tmp_ref = tmp_ref.replace("-\n", "")
					tmp_ref = tmp_ref.replace("\n", " ")
					res.append(tmp_ref)
	return res
