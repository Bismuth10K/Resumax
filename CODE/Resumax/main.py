"""
Code source du Sprint 3 de resumax.
Il est recommandé de générer une venv avec les bibliothèques pyMuPDF et python-dateutil.
"""

import os  # Pour manipuler des dossiers.
import re  # Pour utiliser du regex.
import sys  # Commandes système
from xml.etree.ElementTree import Element, SubElement, ElementTree  # Pour générer des xml

import fitz  # Pour lire les pdf, ---pip install PyMuPDF---
from dateutil.parser import parse  # Pour détecter une date, ---pip install python-dateutil---

# Le dossier contenant les corpus de textes et le texte sous forme de bloc.
directory = '../ressources/'


def txt_reco_patterns():
    """
    Cette fonction génère des txt pour chaque pdf.
    Elle existe pour stocker et comparer les patterns dans les pdf.
    Elle n'apporte aucune idée directement dans le résultat du parsing.
    :return: txt avec le contenu de la première page sous forme de blocks de pyMuPDF.
    """
    for file in os.listdir(directory):
        if not file.endswith(".pdf"):
            continue
        with open(os.path.join(directory, file), 'rb') as pdfFileObj:
            doc = fitz.open(pdfFileObj)
            # test récupération taille de police
            # page = doc[0]
            # for b in page.get_text("dict", flags=11)["blocks"]:
            # 	for l in b["lines"]:
            # 		for s in l["spans"]:
            # 			print(s["size"])

            content = doc[0].get_text("blocks", sort=True)

            with open(doc.name + '.txt', 'w') as f:
                for i in content:
                    f.write(str(i) + "\n")


def check_if_toc(bloc: str, toc: list):
    """
    Détermine si bloc est un titre appartenant à la TOC (Table Of Contents, ou Sommaire).
    :param bloc: Un texte.
    :param toc: Une liste.
    :return: True si bloc est dans toc, False sinon.
    """
    for i in toc:
        if bloc in i[1]:
            return True
    return False


def find_title(cur_bloc: list, next_bloc: list):
    """
    Trouve le titre parmi deux blocs, l'un des deux pouvant être un footer, on le détermine donc grâce à la position.
    :param cur_bloc: Un bloc de pyMuPDF.
    :param next_bloc: Un bloc de pyMuPDF.
    :return: titre (str) le vrai titre d'après la position, bloc (int) le numéro du bloc du titre.
    """
    if cur_bloc[1] > next_bloc[1]:  # si la position de cur_bloc sur l'axe y (descendant) est supérieur next_block,
        # c'est probablement un footer. PyMuPDF affiche les footers en premier.
        titre = next_bloc[4]
        bloc = next_bloc[5]
    else:
        titre = cur_bloc[4]
        bloc = cur_bloc[5]
    titre = titre.replace("\n", " ")  # Remplace "\n" par un espace dans le titre.
    return titre, bloc


def check_if_abstract(bloc: str):
    """
    Détermine si un texte contient le terme "abstract" (et donc en est un) ou pas.
    :param bloc: Un texte.
    :return: Int → 	+1 : "abstract" + texte abstract dans le même bloc.
                    +0 : "abstract" seul.
                    -1 : pas de "abstract".
    """
    if "abstract" in bloc.lower():
        if len(bloc) > len("abstract") * 2:
            return 1  # Texte abstract dans le bloc actuel.
        else:
            return 0  # Texte abstract dans le bloc suivant.
    else:
        return -1  # Pas un abstract.


def find_abstract(cur_bloc: str, next_bloc: str, toc=None):
    """
    Détermine si un texte un est un abstract ou pas.
    :param cur_bloc: Un texte où on souhaite déterminer si c'est un abstract ou pas.
    :param next_bloc: Le texte après cur_bloc.
    :param toc: Une liste, sommaire du document s'il existe.
    :return: abstract (str) le texte de l'abstract.
    """
    if toc is None:
        toc = []
    abstract = ""
    checker = check_if_abstract(cur_bloc)

    if checker == 1:  # Si abstract + texte -> renvoie cur_bloc.
        abstract = cur_bloc
        print("Abstract found by checker 1")
    elif checker == 0:  # Si abstract seul -> renvoie next_bloc.
        abstract = next_bloc
        print("Abstract found by checker 0")
    elif next_bloc is not None and re.search(r"\A(?:[0-9]|I|)(?:.|-|)(?: |)[Ii]ntroduction(?: |)(?:\n|)", next_bloc):
        # Si next_bloc est l'introduction, alors cur_bloc est l'abstract. L'abstract se trouve avant l'introduction.
        abstract = cur_bloc
        print("Abstract found by regex")
    elif next_bloc is not None and check_if_toc(next_bloc, toc):
        # si next_bloc fait partie du sommaire, cur_bloc est l'abstract.
        abstract = cur_bloc
        print("Abstract found by TOC")
    abstract = abstract.replace("-\n", "")  # mot coupé en deux dans un paragraphe, donc on remplace par "".
    abstract = abstract.replace("\n", " ")  # retour à la ligne dans un paragraphe, donc on remplace par " ".
    return abstract


def is_date(string: str):
    """
    Détermine si un texte est (ou contient) une date.
    :param string: Un texte où il y aurait potentiellement une date.
    :return: True si contient une date, sinon False.
    """
    try:
        parse(string, fuzzy=True)  # fuzzy permet de trouver une date en plein texte.
        return True
    except ValueError:
        return False


def find_references(pdf: str) -> list:
    """
    Récupère les références de la bibliographie du document.
    :param pdf: le document
    :return: une liste contenant le texte de chaque bloc de la bibliographie
    """
    doc = fitz.open(pdf)
    res = []
    found = False
    for i in range(len(doc)):
        for block in doc[i].get_text("blocks"):
            if ("References" in block[4] or "REFERENCES" in block[4]):
                found = True
            elif found:
                if not block[4].isdigit():
                    print("Found page ", i)
                    print(block[4])
                    res.append(block[4])
    return res


def parser(pdf):
    """
    Parser du paramètre pdf. Il y récupère plusieurs informations.
    :param pdf: Un document pdf à parser.
    :return: Dictionnaire comportant différentes sections du PDF (auteurs, titre, abstract, biblio...)
    """
    doc = fitz.open(pdf)  # On ouvre le pdf avec pyMuPDF (fitz).
    auteur = ""
    titre = ""

    content = doc[0].get_text("blocks")  # Récupération des texts sous forme de blocs.
    # Un block = (x0, y0, x1, y1, "texte", block_no, block_type).
    # (x0, y0) position du bloc en haut à gauche, (x1, y1) position du bloc en bas à droite.
    # block_no le numéro de block lors de la lecture, block_type = 0 si texte, 1 si image.

    # Récupération titre.
    if doc.metadata.get('title'):
        titre = doc.metadata.get('title')
        pos_bloc_titre = 0
    # Si le titre contient un / ou si on l'a pas trouvé dans les metadata,
    # on cherche un nouveau titre dans le document.
    if len(titre) == 0 or re.match(r'/', titre) is not None:
        print("current titre : " + titre)
        titre, pos_bloc_titre = find_title(content[0], content[1])
        print("new titre : " + titre)
    print(titre)

    # Récupération auteurs.
    # if doc.metadata.get('author'):
    #	auteur = doc.metadata.get('author') + "\n"

    # Récupération abstract et auteurs si absents des metadata.
    for i in range(len(content)):
        tmp_txt = content[i][4]  # On stocke le texte du bloc actuel.
        try:
            tmp_next_txt = content[i + 1][4]  # On stocke le texte du bloc suivant s'il existe.
        except IndexError:
            tmp_next_txt = None

        abstract = find_abstract(tmp_txt, tmp_next_txt, doc.get_toc())  # Récupération abstract.

        # Récupération auteurs sur plusieurs lignes tant que ce n'est pas un abstract.
        if i > pos_bloc_titre and abstract == "" and tmp_txt.split() != titre.split():  # and not doc.metadata.get('author')
            if not is_date(tmp_txt):  # Permet de filtrer les dates.
                auteur += tmp_txt.replace("\n", " ") + "\n"
        if len(abstract) > 0:  # Sachant que l'abstract se trouve après les auteurs,
            break  # si on le trouve, on sort de la boucle.
    if len(abstract) == 0:  # Si on ne trouve pas l'abstract, on le dit.
        print("Abstract not found")
    print()
    print(auteur)
    print()

    # Récuperation de la bibliographie
    bib = find_references(pdf)
    bibstr = ""
    for ref in bib:
        bibstr += ref + "\n\n"

    parsed_results = {"titre": titre, "auteur": auteur, "abstract": abstract.replace("\n", " "), "biblio": bibstr}

    return parsed_results


def output_txt(pdf, dict_results: dict):
    """
    Récupère les outputs et les inscrit dans un txt.
    :param pdf: Le document traité, il nous sert pour récupérer le nom dans la mémoire.
    :param dict_results: Le dictionnaire des informations parsées.
    """
    with open("../output/Sprint2_" + pdf + '.txt', 'w') as f:  # On les sauvegarde dans le dossier output.
        f.write("Nom fichier : " + pdf + "\n\n")
        f.write("Titre : " + dict_results.get("titre") + "\n\n")
        f.write("Auteurs : " + dict_results.get("auteur") + "\n")
        f.write("Abstract : \n" + dict_results.get("abstract") + "\n\n")
        f.write("Bibliographie : \n" + dict_results.get("biblio") + "\n")


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
    titre.text = dict_results.get("titre")

    auteurs = SubElement(article, 'auteurs')
    auteur = SubElement(auteurs, 'auteur')
    auteur.text = dict_results.get("auteur")  # rajouter enfants name et mail

    abstract = SubElement(article, 'abstract')
    abstract.text = dict_results.get("abstract")

    biblio = SubElement(article, 'biblio')
    biblio.text = dict_results.get("biblio")

    tree = ElementTree(article)

    with open("../output/Sprint2_" + pdf + '.xml', 'w') as f:
        tree.write(f, encoding='unicode')


def parse_all_pdf(func_output, func_output_all=None):
    """
    Code du sprint 2, récupère : le nom du fichier, le titre de l'article, les auteurs, l'abstract.
    Le code devra être simplifié lors des futurs sprints.
    :return: Un txt pour chaque pdf contenant le nom du fichier, le titre de l'article, les auteurs, l'abstract.
    """
    if not os.path.exists("../output/"):
        os.makedirs("../output/")
    for file in os.listdir(directory):
        if file.endswith(".pdf"):  # On parse tous les pdf dans directory.
            with (open(os.path.join(directory, file), 'rb') as pdf):
                dict_res = parser(pdf)
                func_output(file, dict_res)
                if func_output_all is not None:
                    func_output_all(file, dict_res)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        param = sys.argv[1]
        if '-t' in param:  # Paramètre pour générer des txt.
            parse_all_pdf(output_txt)
        elif '-x' in param:  # Paramètre pour générer des xml.
            parse_all_pdf(output_xml)
        elif '-a' in param:  # Paramètre pour générer des txt et des xml.
            parse_all_pdf(output_txt, output_xml)
        elif '-r':  # Paramètre pour générer les fichiers de reconnaissance des patterns.
            txt_reco_patterns()
    else:  # Parce qu'il n'y a jamais assez de tests !
        txt_reco_patterns()
