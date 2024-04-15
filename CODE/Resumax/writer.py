from xml.etree.ElementTree import Element, SubElement, ElementTree, indent  # Pour générer des xml
import string


def output_txt(pdf, dict_results: dict):
	"""
	Récupère les outputs et les inscrit dans un txt.
	:param pdf: Le document traité, il nous sert pour récupérer le nom dans la mémoire.
	:param dict_results: Le dictionnaire des informations parsées.
	"""
	with open("../output/" + pdf.split("/")[-1][:-4] + '.txt',
				'w') as f:  # On les sauvegarde dans le dossier output.
		f.write("Nom fichier : " + pdf + "\n\n")

		f.write("Titre : " + dict_results.get("titre") + "\n\n")

		f.write("Auteurs : ")
		for i in dict_results.get("auteur"):
			f.write(i + "\n")

		f.write("\nAbstract : \n" + dict_results.get("abstract") + "\n\n")

		f.write("Intro : \n" + dict_results.get("intro") + "\n\n")

		f.write("Corps : \n" + dict_results.get("body") + "\n\n")

		f.write("Discussion et Conclusion : \n" + dict_results.get("discussion") + "\n\n")

		f.write("Bibliographie : \n")
		for element in dict_results.get("biblio"):
			f.write(element + "\n")


def output_xml(pdf, dict_results: dict):
	"""
	Récupère les outputs et les inscrit dans un xml.
	:param pdf: Le document traité, il nous sert pour récupérer le nom dans la mémoire.
	:param dict_results: Le dictionnaire des informations parsées.
	"""
	article = Element('article')
	preamble = SubElement(article, 'preamble')
	preamble.text = pdf

	titre = SubElement(article, 'titre')
	titre.text = "".join(x for x in dict_results.get("titre") if x in string.printable)

	auteurs = SubElement(article, 'auteurs')
	list_auteurs = dict_results.get("auteur")
	list_mails = dict_results.get("mail")

	i = 0
	while i < len(list_auteurs):
		auteur = SubElement(auteurs, 'auteur')

		name = SubElement(auteur, 'name')
		name.text = "".join(x for x in list_auteurs[i] if x in string.printable)

		affi = SubElement(auteur, 'affiliation')
		affi.text = "".join(x for x in list_auteurs[i] if x in string.printable)

		mail = SubElement(auteur, 'mail')
		try:
			mail.text = "".join(x for x in list_mails[i] if x in string.printable)
		except:
			mail.text = "N/A"

		i += 1

	abstract = SubElement(article, 'abstract')
	abstract.text = "".join(x for x in dict_results.get("abstract") if x in string.printable)

	intro = SubElement(article, 'introduction')
	intro.text = "".join(x for x in dict_results.get("intro") if x in string.printable)

	body = SubElement(article, 'corps')
	body.text = "".join(x for x in dict_results.get("body") if x in string.printable)

	discu = SubElement(article, 'discussion')
	discu.text = "".join(x for x in dict_results.get("discussion") if x in string.printable)

	conc = SubElement(article, 'conclusion')
	conc.text = "N/A"

	biblio = SubElement(article, 'biblio')
	biblio.text = "\n".join(str(elem) for elem in dict_results.get("biblio"))

	tree = ElementTree(article)

	indent(tree, space="\t")

#	with open("../output/Sprint2_" + pdf.split("/")[-1] + '.xml', 'w') as f:
#		tree.write(f, encoding="UTF-8")
	tree.write("../output/" + pdf.split("/")[-1][:-4] + '.xml', encoding="utf8", xml_declaration=True)

