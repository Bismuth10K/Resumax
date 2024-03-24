import os

import fitz
from dateutil.parser import parse  # Pour détecter une date, ---pip install python-dateutil---


def txt_reco_patterns():
	"""
	Cette fonction génère des txt pour chaque pdf.
	Elle existe pour stocker et comparer les patterns dans les pdf.
	Elle n'apporte aucune idée directement dans le résultat du parsing.
	:return: txt avec le contenu de la première page sous forme de blocks de pyMuPDF.
	"""
	directory = "../ressources/"
	for file in os.listdir(directory):
		if not file.endswith(".pdf"):
			continue
		with open(os.path.join(directory, file), 'rb') as pdfFileObj:
			doc = fitz.open(pdfFileObj)
			# test récupération taille de police
			# page = doc[0]
			# for b in page.get_text("dict", flags=11)["blocks"]:
			#     for l in b["lines"]:
			#         for s in l["spans"]:
			#             print(s["size"])
			content = []
			for pages in doc:
				content += pages.get_text("blocks") + ["\npage suivante"]
			with open(doc.name + '.txt', 'w') as f:
				for i in content:
					f.write(str(i) + "\n")


def check_if_toc(bloc: str, toc: list):
	"""
	Détermine si bloc est un titre appartenant à la TOC (Table Of Contents, ou Sommaire).
	:param bloc: Un texte.
	:param toc: Une liste.
	:return: True si bloc est dans toc, False sinon.
	"""
	for i in toc:
		if bloc in i[1]:
			return True
	return False


def is_date(string: str):
	"""
	Détermine si un texte est (ou contient) une date.
	:param string: Un texte où il y aurait potentiellement une date.
	:return: True si contient une date, sinon False.
	"""
	try:
		parse(string, fuzzy=True)  # fuzzy permet de trouver une date en plein texte.
		return True
	except ValueError:
		return False


def replacator(text_to_clean: str):
	return text_to_clean.replace("-\n", "").replace("- \n", "").replace("\n", " ")


if __name__ == '__main__':
	txt_reco_patterns()
