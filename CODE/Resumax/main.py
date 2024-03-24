"""
Code source du Sprint 3 de resumax.
Il est recommandé de générer une venv avec les bibliothèques pyMuPDF et python-dateutil.
"""

import os  # Pour manipuler des dossiers.
import re  # Pour utiliser du regex.
import sys  # Commandes système

import fitz  # Pour lire les pdf, ---pip install PyMuPDF---
import titre
import author
import abstract
import references
import body

from autre import *
from writer import *
from menu import menu

def parser_old(pdf):
    """
    Parser du paramètre pdf. Il y récupère plusieurs informations.
    :param pdf: Un document pdf à parser.
    :return: Dictionnaire comportant différentes sections du PDF (auteurs, titre, abstract, biblio...)
    """
    doc = fitz.open(pdf)  # On ouvre le pdf avec pyMuPDF (fitz).
    auteur = []
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
        # print("current titre : " + titre)
        titre, pos_bloc_titre = find_title(content[0], content[1])
        # print("new titre : " + titre)
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

    if len(abstract) == 0:  # Si on ne trouve pas l'abstract, on le dit.
        print("Abstract not found")

    # Récuperation de la bibliographie
    bib = find_references(pdf)
    bibstr = ""
    for ref in bib:
        bibstr += ref + "\n"

    parsed_results = {"titre": titre, "auteur": auteur, "abstract": abstract.replace("\n", " "), "biblio": bibstr}

    return parsed_results


def parser_new(pdf):
    """

    :param pdf: le chemin du fichier pdf à parser
    :return: void
    """

    # Document opening
    doc = fitz.open(pdf)
    authors = []
    mails = []
    titleStr = ""
    abstractStr = ""

    # On most documents, the first page is where we find titles, authors and abstracts.
    page = doc[0]

    # finding title
    temp = titre.find_title(page, 0)
    titleStr = temp[0]
    blknum = temp[1]


    # finding authors
    temp = author.find_authors(page, blknum)
    authors = temp[0]
    mails = temp[1]
    blknum = temp[2]


    # finding abstract
    temp = abstract.find_abstract(page, blknum)
    abstractStr = temp[0]
    blknum = temp[1]


    #finding introduction and body
    intro, bodyText = body.find_body(pdf)


    #extracting discussions and conclusions
    discussion, bodyText = body.extract_discuss(bodyText)


    # finding references
    refs = references.find_references(pdf)


    # on met tout ca dans un dictionnaire pour pouvoir l'écrire dans les fichiers après
    print(titleStr)
    # print("---")
    # print(authors)
    # print("---")
    # print(mails)
    # print("---")
    # print(abstractStr)
    # print("---")
    # print(intro)
    # print("---")
    # print(bodyText)
    # print("---")
    # print(discussion)
    # print("---")
    # print(refs)
    print(type(refs))
    parsed_results = {"titre": titleStr, "auteur": authors, "mails":mails, "abstract": abstractStr.replace("\n", " "), "intro":intro, "body":bodyText, "discussion":discussion, "biblio": refs}
    return parsed_results


def parse_all_pdf(pdf_files: list, func_output, func_output_all=None):
    """
    Code du sprint 2, récupère : le nom du fichier, le titre de l'article, les auteurs, l'abstract.
    Le code devra être simplifié lors des futurs sprints.
    :return: Un txt pour chaque pdf contenant le nom du fichier, le titre de l'article, les auteurs, l'abstract.
    """
    if not os.path.exists("../output/"):
        os.makedirs("../output/")
    for file in pdf_files:
        with (open(file, 'rb') as pdf):
            dict_res = parser_new(pdf)
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
