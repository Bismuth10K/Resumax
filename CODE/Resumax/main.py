"""
Code source du Sprint 3 de resumax.
Il est recommandé de générer une venv avec les bibliothèques pyMuPDF et python-dateutil.
"""

import sys  # Commandes système

import abstract
import author
import body
import references
import titre
from autre import *
from menu import menu
from writer import *


def parser(pdf):
	"""
	Fonction principale qui parse les pdfs.
	Args:
		pdf: le document à parser

	Returns: un dictionnaire contenant chaque partie parsée.

	"""
	# Document opening
	doc = fitz.open(pdf)

	# On most documents, the first page is where we find titles, authors and abstracts.
	page = doc[0]

	pagenum = 0
	for block in page.get_text("blocks"):
		if "elsevier" in block[4].lower():
			pagenum = 1
			break

	# finding title
	temp = titre.find_title(doc, pagenum, 0)
	titleStr = temp[0]
	page_num = temp[1]
	blknum = temp[2]

	# finding authors
	temp = author.find_authors(doc, 0, blknum)
	authors = temp[0]
	mails = temp[1]
	page_num = temp[2]
	blknum = temp[3]

	# finding abstract
	temp = abstract.find_abstract(doc, 0, blknum)
	abstractStr = temp[0]
	page_num = temp[1]
	blknum = temp[2]

	# finding introduction and body
	temp = body.extract_body(doc, page_num, blknum)
	intro = temp[0]
	bodyText = temp[1]
	discussion = temp[2]
	conclu = temp[3]

	# finding references
	refs = references.find_references(pdf)

	parsed_results = {"titre": replacator(titleStr), "auteur": authors, "mails": mails,
					  "abstract": replacator(abstractStr), "intro": replacator(intro), "body": replacator(bodyText),
					  "discussion": replacator(discussion), "conclusion": replacator(conclu), "biblio": refs}
	return parsed_results


def parse_all_pdf(pdf_files: list, func_output, func_output_all=None):
	"""
	Automatise le parsind des pdfs pour plusieurs pdfs.

	Args:
		pdf_files: la liste des chemins relatifs des fichiers à analyser
		func_output: la fonction déterminant la sortie du programme (txt, xml, ou les deux)
		func_output_all: la deuxieme fonction, si nécéssaire

	"""
	if not os.path.exists("../output/"):
		os.makedirs("../output/")
	for file in pdf_files:
		with (open(file, 'rb') as pdf):
			dict_res = parser(pdf)
			func_output(file, dict_res)
			if func_output_all is not None:
				func_output_all(file, dict_res)
			print(pdf, "parsé et traité !")


if __name__ == '__main__':
	if len(sys.argv) >= 3:
		output_par = sys.argv[1]
		files = menu(sys.argv[2])

		if '-t' in output_par:  # Paramètre pour générer des txt.
			parse_all_pdf(files, output_txt)
		elif '-x' in output_par:  # Paramètre pour générer des xml.
			parse_all_pdf(files, output_xml)
		elif '-a' in output_par:  # Paramètre pour générer des txt et des xml.
			parse_all_pdf(files, output_txt, output_xml)
		elif '-r':  # Paramètre pour générer les fichiers de reconnaissance des patterns.
			txt_reco_patterns()
	else:  # Parce qu'il n'y a jamais assez de tests !
		txt_reco_patterns()
