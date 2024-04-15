import re
from autre import replacator
import fitz


def find_body(pdf: str):
	doc = fitz.open(pdf)
	found_intro = False
	do_body = False

	intro = ""
	corps = ""
	for page in doc:
		for block in page.get_text("blocks"):
			# Si le bloc est un texte, on fait le truc, sinon (c'est une image), on ne fait rien
			if block[6] == 0:
				# deuxieme partie : stocker l'intro jusqu'a la partie suivante
				if found_intro:

					if not re.fullmatch(r"\A( )*(2|ii|)(?:.|-|)(?: |)(?:\n|)([a-z](?: |))+(?:\n|)",
										block[4].lower()):  # Regex pour deuxième partie
						intro += block[4]
					else:
						# print("do_body")
						do_body = True
						found_intro = False

				# troisième partie : stocker le reste du corps jusqu'aux références
				elif do_body:
					if not re.match(r"references(?: |\n|)+", block[4].lower()):  # Regex pour references
						corps += block[4]
					else:
						return intro, corps

				# premiere partie : trouver l'intro
				else:
					if re.match(r"\A( )*(?:[0-9]|i|)(?:.|-|)(?: |)(?:\n|)introduction(?: |)(?:\n|)",
								block[4].lower()):  # Regex pour Intro
						# print("found_intro")
						found_intro = True
						intro += block[4]
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


def extract_conclusion(discussion: str, body: str):
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
