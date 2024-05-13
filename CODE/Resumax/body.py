import re

from CODE.Resumax import autre
from autre import replacator
import fitz


def find_intro(doc: fitz.Document, page_num: int, blknum: int):
	found_intro = False
	finish_intro = False

	newblk = blknum
	newpage = page_num
	intro = ""

	for page in range(page_num, len(doc)):
		bold_texts_page = findAllBold(doc[page])
		for i in range(0, len(doc[page].get_text("blocks"))):
			block = doc[page].get_text("blocks")[i]
			if block[-1] == 1:
				continue
			text = block[4]
			print("###########BLOCK DELIMITER##############\n", text.lower())
			print(re.match(r"\A(?:[xvi]|[0-9]|\.|\n| )+(?:- |)introduction(?:s|)", text.lower()))
			if found_intro == False:  # on a pas encore trouvé l'intro
				if autre.is_section("introduction", text.lower()):

					found_intro = True

			else:  # on a trouvé le début de l'intro
				if finish_intro == False:
					if not autre.is_section("[a-z]", text.lower()) and text.lower() not in bold_texts_page:
						print("AAAAAAAAAAAA")
						intro += text
					elif re.match(r"\A([0-9]\.){2,}", text.lower()):
						print("Subsection")
						intro += text
					else:
						print("FIN", text.lower())
						finish_intro = True
						break
		if finish_intro:
			break
		newblk += 1
	newpage += 1

	if intro == "":
		intro = "N/A"
		return intro, page_num, blknum

	return intro, newpage, newblk


def find_discuss(doc: fitz.Document, page_num: int, blknum: int):
	found_discuss = False
	finished_discuss = False

	discussed = ""
	newpage = page_num
	newblk = blknum

	for page in range(page_num, len(doc)):
		for i in range(0, len(doc[page].get_text("blocks"))):
			block = doc[page].get_text("blocks")[i]
			if block[-1] == 1:
				continue
			text = block[4]
			if not found_discuss:
				if autre.is_section("discussion", text.lower()):  # Regex pour Discussion
					found_discuss = True

			else:  # on a trouvé le début de la discussion
				if finished_discuss == False:
					if not autre.is_section("conclusion", text.lower()):
						discussed += text
					else:
						finished_discuss = True
						break
		if not finished_discuss:
			break
		newblk += 1
	newpage += 1

	if discussed == "":
		discussed = "N/A"
		return discussed, page_num, blknum
	return discussed, newpage, newblk


def find_conclusion(doc: fitz.Document, page_num: int, blknum: int):
	found_conclu = False
	finished_conclu = False
	conclu = ""
	newpage = page_num
	newblk = blknum

	for page in range(page_num, len(doc)):
		for i in range(0, len(doc[page].get_text("blocks"))):
			block = doc[page].get_text("blocks")[i]
			if block[-1] == 1:
				continue
			text = block[4]
			if found_conclu == False:
				if autre.is_section("conclusion", text.lower()):
					found_conclu = True
			else:  # on a trouvé le début de la conclusion
				if finished_conclu == False:
					if not autre.is_section("reference", text.lower()):
						conclu += text
					else:
						finished_conclu = True
						break

		if finished_conclu:
			break
		newblk += 1
	newpage += 1

	if conclu == "":
		conclu = "N/A"
		print("HAHA non")
		return conclu, page_num, blknum
	return conclu, newpage, newblk


def extract_body(doc: fitz.Document, page_num: int, blknum: int):
	newpage = 0
	newblk = 0

	# on fit un premier tour du document pour choper les parties spécifiques
	intro, newpage, newblk = find_intro(doc, page_num, blknum)
	discuss, newpage, newblk = find_discuss(doc, newpage, newblk)
	conclusion, newpage, newblk = find_conclusion(doc, newpage, newblk)
	body = ""

	# On repart du début pour extraire le corps parmi le reste du texte déja traité
	for page in range(page_num, len(doc)):
		for i in range(blknum, len(doc[page].get_text("blocks"))):
			block = doc[page].get_text("blocks")[i]
			if block[-1] == 1:
				continue
			text = block[4]
			if not (text in intro or text in discuss or text in conclusion):
				body += text
	return intro, body, discuss, conclusion


def findAllBold(page):
	block_dict = {}
	bold_texts = []
	page_num = 1

	file_dict = page.get_text('dict')  # Get the page dictionary
	block = file_dict['blocks']  # Get the block information
	block_dict[page_num] = block  # Store in block dictionary

	for page_num, blocks in block_dict.items():
		for block in blocks:
			if block['type'] == 0:
				for line in block['lines']:
					for span in line['spans']:
						text = span['text']
						flags = int(span['flags'])
						if flags & 2**4:
							bold_texts.append(text.lower())
	return bold_texts


if __name__ == "__main__":
	intro, body, discuss, conclusion = extract_body(fitz.open("../ressources/infoEmbeddings.pdf"), 0, 0)
	print("-----------INTRO-------------")
	# print(intro)

# TODO ckecker la position des blocs: si c'est au dessus du titre, ca dégage
