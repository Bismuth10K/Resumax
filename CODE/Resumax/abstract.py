import re

import fitz

from autre import replacator,is_section


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
	newpage = page_num
	newblk = blknum

	found_abstract = False
	finished_abstract = False
	abstract = ""

	for page in range(page_num, len(doc)):
		for i in range(blknum, len(doc[page].get_text("blocks"))):
			block = doc[page].get_text("blocks")[i]
			text = block[4]

			if not found_abstract:
				if re.match(r"\A(?: |\n|)+abstract", text.lower()):
					found_abstract = True
					abstract += text
				else :
					continue
			else:
				if not finished_abstract:
					if is_section("introduction", text.lower()) or is_section("", text.lower()):
						finished_abstract = True
					else :
						abstract += text
				else :
					break
			newblk = i
		if finished_abstract :
			break
		newpage = page

	if abstract == "":
		abstract = "N/A"
		return abstract, page_num, blknum
	return abstract, newpage, newblk


if __name__ == "__main__":
	doc = fitz.open("../ressources/BLESS.pdf")
	abst = find_abstract(doc, 0, 0)[0]
	print("-------ABSTRACT-------")
	print(abst)