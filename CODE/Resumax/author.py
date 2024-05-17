import fitz

from autre import replacator


def find_authors(doc: fitz.Document, page_num: int, blknum: int):
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
	for string in strings:
		if "@" in string:
			return string


if __name__ == "__main__":
	d = fitz.open("../ressources/Torres.pdf")
	tab = find_authors(d[0], 1)
