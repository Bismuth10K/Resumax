import fitz

from autre import replacator


def find_authors(doc: fitz.Document, page_num: int, blknum: int):
	"""
	Fonction d'extraction des auteurs, de leurs affiliations et de leurs mails (en théorie)
	Args:
		doc: L'objet Document à analyser
		page_num: numéro de la page où commencer la recherche
		blknum: nuéro du bloc sur la page où commencer la recherche

	Returns: un tuple avec les noms, affiliations, mails dans des listes

	"""
	mails = []
	names = []
	blocks = doc[page_num].get_text("blocks")
	for i in range(blknum, len(blocks)):
		block = blocks[i]
		text = block[4]
		# les auteurs se trouvent pratiquement toujours juste au-dessus de l'abstract
		if "abstract" in text.lower():
			blknum = block[5]
			break
		else:
			# si un email est trouvé : on l'ajoute dans la liste et on l'enlève du texte du bloc
			tmp_auteur = replacator(text)
			if "@" in text:
				while email(tmp_auteur.split(" ")) is not None:
					m = email(tmp_auteur.split(" "))
					mails.append(m)
					tmp_auteur = tmp_auteur.replace(m, "")

			# pour les noms, on ajoute ce qui reste du texte du bloc
			names.append(replacator(tmp_auteur))
	return names, mails, page_num, blknum


def email(strings: list):
	"""
	Détecte s'il y a un mail.

	Args:
		strings: Liste de strings.

	Returns: Vrai s'il y en a un, faux sinon
	"""
	for string in strings:
		if "@" in string:
			return string
