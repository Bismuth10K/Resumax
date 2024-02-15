import os

import fitz

directory = '../ressources/'


def test_txt_reco_patterns():
	for file in os.listdir(directory):
		if not file.endswith(".pdf"):
			continue
		with open(os.path.join(directory, file), 'rb') as pdfFileObj:
			doc = fitz.open(pdfFileObj)

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
			return 1
		else:
			return 0
	else:
		return -1


def sprint_2():
	for file in os.listdir(directory):
		if file.endswith(".pdf"):
			with open(os.path.join(directory, file), 'rb') as pdfFileObj:
				doc = fitz.open(pdfFileObj)
				# récupération nom fichier
				nom_fichier = doc.name.split('/')[-1]

				# récupération titre
				if doc.metadata.get('title'):
					titre = doc.metadata.get('title')
				else:
					pass  # TODO parse titre

				# récupération auteurs
				if doc.metadata.get('author'):
					auteur = doc.metadata.get('author')
				else:
					pass  # TODO todo parse author

				# récupération abstract
				content = doc[0].get_text("blocks")
				for i in range(len(content)):
					tmp_txt = content[i][4]
					checker = check_if_abstract(tmp_txt)
					if checker == 1:
						abstract = tmp_txt
						break
					elif checker == 0:
						abstract = content[i+1][4]
						break

				# output
				with open("../output/Sprint2_" + doc.name.split("/")[-1] + '.txt', 'w') as f:
					f.write(nom_fichier + "\n")
					f.write(titre + "\n")
					f.write(auteur + "\n")
					f.write(abstract.replace("\n", " "))
				nom_fichier = ""
				titre = ""
				auteur = ""
				abstract = ""

# test_txt_reco_patterns()
sprint_2()
