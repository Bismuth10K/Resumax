import fitz

from autre import replacator


def find_title(doc: fitz.Document, blknum: int):
	"""
	Trouve le titre parmi deux blocs, l'un des deux pouvant être un footer, on le détermine donc grâce à la position.
	:param page: Une page du document.
	:param blknum: Un bloc de pyMuPDF.
	:return: titre (str) le vrai titre d'après la position, bloc (int) le numéro du bloc du titre.
	"""


	cur_block = doc[0].get_text("blocks")[blknum]
	next_block = doc[0].get_text("blocks")[blknum + 1]

	if cur_block[1] > next_block[1]:  # si la position de cur_bloc sur l'axe y (descendant) est supérieur next_block,
		# c'est probablement un footer. PyMuPDF affiche les footers en premier.
		titre = next_block[4]
		bloc = next_block[5]
	else:
		titre = cur_block[4]
		bloc = cur_block[5]
	titre = replacator(titre)
	return titre, bloc
