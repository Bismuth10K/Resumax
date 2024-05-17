import re

import fitz

import autre


def find_intro(doc: fitz.Document, page_num: int, blknum: int):
	"""
	Fonction d'extraction de la partie "Introduction"

	Args:
		doc: Le document à analyser
		page_num: Le numéro de la page où commencer la recherche
		blknum: Le numéro de bloc sur la page où commencer

	Returns: Une chaine contenant l'introduction du document
	"""
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

			if found_intro == False:  # on a pas encore trouvé l'intro
				if autre.is_section("introduction", text.lower()):
					found_intro = True
					page_pos = page
					pos = block[1]
					posx = block[2]
			else:  # on a trouvé le début de l'intro
				if finish_intro == False:
					if not autre.is_section("[a-z]", text.lower()) and text.lower() not in bold_texts_page:
						if page == page_pos:
							if block[1] > pos:
								if block[0] < posx:
									intro += text
							else:
								intro += text
						else:
							intro += text
					elif re.match(r"\A(1\.[0-9](?: |\n|)+)", text.lower()):

						intro += text
					else:
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
	"""
	Fonction d'extraction de la partie "Discussion"

	Args:
		doc: Le document à analyser
		page_num: Le numéro de la page où commencer la recherche
		blknum: Le numéro de bloc sur la page où commencer

	Returns: Une chaine contenant les discussions du document
	"""
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
					pos = block[1]
					posx = block[2]
					page_pos = page
			else:  # on a trouvé le début de la discussion
				if finished_discuss == False:
					if not autre.is_section("conclusion", text.lower()):
						if page == page_pos:
							if block[1] > pos:
								if block[0] < posx:
									discussed += text
							else:
								discussed += text
						else:
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
	"""
	Fonction d'extraction de la partie "Conclusion"

	Args:
		doc: Le document à analyser
		page_num: Le numéro de la page où commencer la recherche
		blknum: Le numéro de bloc sur la page où commencer

	Returns: Une chaine contenant la conclusion du document
	"""
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
					pos = block[1]
					posx = block[2]
					page_pos = page
					found_conclu = True
			else:  # on a trouvé le début de la conclusion
				if finished_conclu == False:

					if not re.match(r"\A(?: |\n|[a-z0-9.]|)+reference(?:[a-z]| |)*", text.lower()) and not re.match(
							r"\A(?: |\n|[a-z0-9.]|)+acknowledg(?:e|)ment(?:[a-z]| |)*", text.lower()):
						if page == page_pos:
							if block[1] > pos:
								if block[0] < posx:
									conclu += text
							else:
								conclu += text
						else:
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

		return conclu, page_num, blknum
	return conclu, newpage, newblk


def extract_body(doc: fitz.Document, page_num: int, blknum: int):
	"""
	Fonction d'extraction du corps du document, sans les parties traitées auparavant.

	Args:
		doc: Le document à analyser
		page_num: Le numéro de la page où commencer la recherche
		blknum: Le numéro de bloc sur la page où commencer

	Returns: Une chaine contenant le corps du document
	"""
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
	"""
	Retrouve tous les textes en gras dans une page.

	Args:
		page: Un objet page de PyMuPDF

	Returns: Une liste des textes en gras dana la page, tous les textes sont en minuscule.
	"""
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
						if flags & 2 ** 4:
							bold_texts.append(text.lower())
	return bold_texts
