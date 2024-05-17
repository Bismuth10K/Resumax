import fitz

from autre import replacator


def find_title(doc: fitz.Document, page_num: int, blknum: int):
	"""
	Trouve le titre parmi deux blocs, l'un des deux pouvant être un footer, on le détermine donc grâce à la position.

	Args:
		doc: Le document à analyser
		page_num: le numéro de la page où commencer
		blknum: le numéro de bloc sur la page où commencer

	Returns: un string contenant le titre
	"""

	cur_block = doc[page_num].get_text("blocks")[blknum]
	next_block = doc[page_num].get_text("blocks")[blknum + 1]

	if cur_block[1] > next_block[1]:  # si la position de cur_bloc sur l'axe y (descendant) est supérieur next_block,
		# c'est probablement un footer. PyMuPDF affiche les footers en premier.
		titre = next_block[4]
		bloc = next_block[5]
	else:
		titre = cur_block[4]
		bloc = cur_block[5]
	titre = replacator(titre)
	return titre, page_num, blknum
