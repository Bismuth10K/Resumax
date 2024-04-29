import re
from autre import replacator
import fitz


def find_intro(doc:fitz.Document, page_num:int, blknum:int):
	found_intro = False
	finish_intro = False


	newblk = blknum
	newpage = page_num
	intro = ""

	for page in range(page_num, len(doc)):
		for i in range(blknum, len(doc[page].get_text("blocks"))):
			block = doc[page].get_text("blocks")[i]
			text = block[4]
			if found_intro == False: # on a pas encore trouvé l'intro
				if re.match(r"\A( )*(?:[0-9]|i|)(?:\.|-|)(?: |)(?:\n|)introduction(?: |)(?:\n|)", text.lower()):
					found_intro = True
					intro += text
			else : # on a trouvé le début de l'intro
				if finish_intro == False :
					#print("ALED\n" + text.lower())
					if not re.match(r"\A( *)(?:([0-9]|\.)|i+)( *)(\n|-|\.)", text.lower()):
						intro += text
					else:
						finish_intro = True
						break
		if finish_intro:
			break
		newblk += 1
	newpage += 1

	if intro == "" :
		intro = "N/A"
		return intro, page_num, blknum

	return intro, newpage, newblk


def find_discuss(doc : fitz.Document, page_num:int, blknum:int):
	found_discuss = False
	finished_discuss = False

	discussed = ""
	newpage = page_num
	newblk = blknum

	for page in range(page_num, len(doc)-1):
		for i in range(blknum, len(doc[page].get_text("blocks"))-1):
			block = doc[page].get_text("blocks")[i]
			text = block[4]
			if not found_discuss:
				if re.match(r"(?:[0-9]|\.)+(?: *|)(?:- |)discussion(?:s|)", text.lower()):  # Regex pour Discussion
					found_discuss = True
					discussed += text
			else: #on a trouvé le début de la discussion
				if finished_discuss == False :
					if re.fullmatch(r"[0-9]*[ .\-)/]*conclusion(?:s|)", text.lower()): #On s'arrete quand on tombe sur la conclusion
						finished_discuss = True
						break
					discussed += "###########BLOCK DELIMITER###########" + text
						# print("Discussion found")
		if not finished_discuss :
			break
		newblk += 1
	newpage += 1

	if discussed == "":
		discussed = "N/A"
		return discussed, page_num, blknum
	return discussed, newpage, newblk



def find_conclusion(doc:fitz.Document, page_num:int, blknum:int):
	found_conclu = False
	finished_conclu = False
	conclu = ""
	newpage = page_num
	newblk = blknum

	for page in range(page_num, len(doc)-1):
		for i in range(blknum, len(doc[page].get_text("blocks"))-1):
			block = doc[page].get_text("blocks")[i]
			text = block[4]
			if not found_conclu:
				if re.match(r"(?:[0-9]|\.)+(?: *|)(?:- |)conclusion(?:s|)", text.lower()):  # Regex pour Discussion
					found_conclu = True
					conclu += text
			else: #on a trouvé le début de la discussion
				if finished_conclu == False :
					if re.fullmatch(r"\Areferences(?: |\n|)+", text.lower()): #On s'arrete quand on tombe sur la conclusion
						finished_conclu = True
						break
					conclu += "###########BLOCK DELIMITER###########" + text

		if not finished_conclu :
			break
		newblk += 1
	newpage += 1

	if conclu == "":
		conclu = "N/A"
		return conclu, page_num, blknum
	return conclu, newpage, newblk




if __name__ == "__main__":
	intro = find_conclusion(fitz.open("../ressources/surveyTermExtraction.pdf"), 0,0)[0]
	print("-----------INTRO-------------")
	print(intro)
	print("-----------BODY--------------")

