import re

import fitz

from autre import is_section


def find_abstract(doc: fitz.Document, page_num: int, blknum: int):
	"""
	Fonction d'extraction de la partie "Abstract" d'un document

	Args:
		doc: l'objet Document à analyser
		page_num: le numéro de la page où commencer la recherche
		blknum: le numéro du bloc sur la page où commencer la recherche

	Returns: Une chaine de caractères contenant l'abstract du document.
	"""
	newpage = page_num
	newblk = blknum

	found_abstract = False  # S'active quand l'abstract a été trouvé
	finished_abstract = False  # S'active quand la partie d'apre a été trouvée
	abstract = ""

	for page in range(page_num, len(doc)):
		for i in range(blknum, len(doc[page].get_text("blocks"))):
			block = doc[page].get_text("blocks")[i]
			text = block[4]

			if not found_abstract:
				if re.match(r"\A(?: |\n|)+abstract", text.lower()) or "a b s t r a c t" in text.lower():
					found_abstract = True
					abstract += text
				else:
					continue
			else:
				if not finished_abstract:
					if is_section("introduction", text.lower()) or is_section("", text.lower()):
						finished_abstract = True
					else:
						abstract += text
				else:
					break
			newblk = i
		if finished_abstract:
			break
		newpage = page

	if abstract == "":
		abstract = "N/A"
		return abstract, page_num, blknum
	return abstract, newpage, newblk
