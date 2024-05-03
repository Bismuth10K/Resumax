import fitz

from autre import replacator


def find_authors(doc: fitz.Document, page_num: int, blknum: int):
	mails = []
	names = []
	for block in range(blknum, len(doc[page_num].get_text("blocks"))):
		# les auteurs se trouvent pratiquement toujours juste au-dessus de l'abstract
		if "abstract" in block[4].lower():
			blknum = block[5]
			break
		else:
			# si un email est trouvé : on l'ajoute dans la liste et on l'enlève du texte du bloc
			tmp_auteur = replacator(block[4])
			if "@" in block[4]:
				while email(tmp_auteur.split(" ")) is not None:
					m = email(tmp_auteur.split(" "))
					mails.append(m)
					tmp_auteur = tmp_auteur.replace(m, "")

			# pour les noms, on ajoute ce qui reste du texte du bloc
			names.append(replacator(tmp_auteur))
	return names, mails, page_num, blknum


def email(strings: list):
	for string in strings:
		if "@" in string:
			return string


if __name__ == "__main__":
	d = fitz.open("../ressources/Torres.pdf")
	tab = find_authors(d[0], 1)
