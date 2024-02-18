import os
import re
import fitz

directory = '../ressources/'


def test_txt_reco_patterns():
	for file in os.listdir(directory):
		if not file.endswith(".pdf"):
			continue
		with open(os.path.join(directory, file), 'rb') as pdfFileObj:
			doc = fitz.open(pdfFileObj)

			# page = doc[0]
			# for b in page.get_text("dict", flags=11)["blocks"]:
			# 	for l in b["lines"]:
			# 		for s in l["spans"]:
			# 			print(s["size"])

			if doc.metadata.get('author'):
				print(doc.metadata.get('author'))
			else:
				print("HAHA no")

			print(doc.metadata)
			print(doc.name.split('/')[-1])
			content = doc[0].get_text("blocks")

			with open(doc.name + '.txt', 'w') as f:
				for i in content:
					f.write(str(i) + "\n")


def check_if_abstract(bloc: str):
	if "abstract" in bloc.lower():
		if len(bloc) > len("abstract") * 2:
			return 1  # Texte abstract dans le bloc actuel
		else:
			return 0  # Texte abstract dans le bloc suivant
	else:
		return -1  # Pas un abstract


def check_if_toc(bloc: str, toc: list):
	for i in toc:
		if bloc in i[1]:
			return True
	return False


def find_title(cur_bloc: list, next_bloc: list):
	if cur_bloc[1] > next_bloc[1]:
		titre = next_bloc[4]
	else:
		titre = cur_bloc[4]
	titre = titre.replace("\n", " ")
	return titre


def find_abstract(cur_bloc: str, next_bloc: str, toc=None):
	if toc is None:
		toc = []
	abstract = ""
	checker = check_if_abstract(cur_bloc)
	if checker == 1:
		abstract = cur_bloc
		print("Abstract found by checker 1")
	elif checker == 0:
		abstract = next_bloc
		print("Abstract found by checker 0")
	elif next_bloc is not None and re.search(r"\A(?:[0-9]||I)(?:.|-|)(?: |)[Ii]ntroduction(?: |)(?:\n|)", next_bloc):
		abstract = cur_bloc
		print("Abstract found by regex")
	elif next_bloc is not None and check_if_toc(next_bloc, toc):
		abstract = cur_bloc
		print("Abstract found by TOC")
	abstract = abstract.replace("-\n", "")
	abstract = abstract.replace("\n", " ")
	return abstract


def sprint_2():
	for file in os.listdir(directory):
		if file.endswith(".pdf"):
			with (open(os.path.join(directory, file), 'rb') as pdfFileObj):
				doc = fitz.open(pdfFileObj)

				content = doc[0].get_text("blocks", sort=True)

				print(file)
				print(doc.get_toc())

				# récupération titre
				if doc.metadata.get('title'):
					titre = doc.metadata.get('title')
				if len(titre) == 0 or re.match(r'/', titre) is not None:
					print("current titre : " + titre)
					titre = find_title(content[0], content[1])
					print("new titre : " + titre)
				print(titre)

				# récupération auteurs
				if doc.metadata.get('author'):
					auteur = doc.metadata.get('author')
				else:
					pass  # TODO parse author

				# récupération abstract
				for i in range(len(content)):
					tmp_txt = content[i][4]
					try:
						tmp_next_txt = content[i + 1][4]
					except IndexError:
						tmp_next_txt = None
					abstract = find_abstract(tmp_txt, tmp_next_txt, doc.get_toc())
					if len(abstract) > 0:
						break
				if len(abstract) == 0:
					print("Abstract not found")
				else:
					print(abstract)
				print()

				# output
				with open("../output/Sprint2_" + file + '.txt', 'w') as f:
					f.write(file + "\n")
					f.write(titre + "\n")
					f.write(auteur + "\n")
					f.write(abstract.replace("\n", " "))
				titre = ""
				auteur = ""
				abstract = ""


# test_txt_reco_patterns()
sprint_2()
