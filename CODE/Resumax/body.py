import re
from autre import replacator
import fitz


def find_intro(doc:fitz.Document, page_num:int, blknum:int):
	found_intro = False
	do_body = False

	intro = ""
	corps = ""
	for page in range(page_num, len(doc)):
		for i in range(blknum, len(doc[page].get_text("blocks"))):
			block = page.get_text("blocks")[i]
			text = block[4]
			if found_intro == False:
				if re.match(r"\A( )*(?:[0-9]|i|)(?:.|-|)(?: |)(?:\n|)introduction(?: |)(?:\n|)", text.lower()):
					found_intro = True
					intro += text

	return intro, corps


def extract_discuss(body: str):
	decompo = body.split("\n")
	recompo = ""
	discussed = ""

	found_discuss = False
	for line in decompo:
		if found_discuss:
			decompo.remove(line)
			discussed += line + "\n"
		else:
			if re.match(r"[0-9]*(?: *|)(?:- |)discussion(?:s|)", line.lower()):  # Regex pour Discussion
				# print("Discussion found")
				found_discuss = True
			else:
				recompo += line + "\n"
	return discussed, recompo



def find_conclusion(discussion: str, body: str):
	found_conclu = False
	conclu = ""
	discu = ""
	autre = ""
	# si la discussion est vide, la conclusion se trouve dans le body
	if discussion == "":
		for element in body.split("\n"):
			if found_conclu:
				conclu += element + "\n"
			else:
				if re.fullmatch(r"[0-9]*[ .\-)/]*conclusion(?:s|)", element.lower()):
					found_conclu = True
				else:
					discu += element + "\n"
		return (discussion != ""), autre, conclu
	# sinon la conclusion est dans la discussion
	else:
		for element in discussion.split("\n"):
			if found_conclu:
				conclu += element + "\n"
			else:
				if re.fullmatch(r"[0-9]*[ .\-)/]*conclusion(?:s|)", element.lower()):
					found_conclu = True
				else:
					discu += element + "\n"
		return (discussion != ""), discu, conclu


if __name__ == "__main__":
	intro, body = find_body("..\\ressources\\acl2012.pdf")
	discussion, body = extract_discuss(body)
	print(intro)
	print("-------------------------")
	print(body)
	print("-------------------------")
	print(discussion)
