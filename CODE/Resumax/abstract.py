import re

import fitz

from autre import replacator


def check_if_abstract(bloc: str):
	"""
	Détermine si un texte contient le terme "abstract" (et donc en est un) ou pas.
	:param bloc: Un texte.
	:return: Int → 	+1 : "abstract" + texte abstract dans le même bloc.
					+0 : "abstract" seul.
					-1 : pas de "abstract".
	"""
	if "abstract" in bloc.lower():
		if len(bloc) > len("abstract") * 2:
			return 1  # Texte abstract dans le bloc actuel.
		else:
			return 0  # Texte abstract dans le bloc suivant.
	else:
		return -1  # Pas un abstract.


def find_abstract(doc: fitz.Document, page_num: int, blknum: int, toc=None):
	"""
	Détermine si un texte un est un abstract ou pas.
	:param page: Une page du document.
	:param blknum : Le numéro du bloc courant.
	:param toc: Une liste, sommaire du document s'il existe.
	:return: abstract (str) le texte de l'abstract.
	"""

	abstract = ""
	for page in doc:
		for i in range(blknum, len(page.get_text("blocks"))):
			block = page.get_text("blocks")[i]
			if re.search(r"\A( )*(?:[0-9]|i|)(?:.|-|)(?: |)(?:\n)[Ii]ntroduction(?: |)(?:\n|)", block[4].lower()):
				abstract = replacator(abstract)
				blknum = block[5]
				page_num = page.number
				break
			else:
				abstract += block[4] + " "

	return abstract, page_num, blknum
