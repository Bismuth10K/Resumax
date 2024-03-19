from xml.etree.ElementTree import Element, SubElement, ElementTree, indent  # Pour générer des xml


def output_txt(pdf, dict_results: dict):
    """
    Récupère les outputs et les inscrit dans un txt.
    :param pdf: Le document traité, il nous sert pour récupérer le nom dans la mémoire.
    :param dict_results: Le dictionnaire des informations parsées.
    """
    with open("../output/Sprint2_" + pdf.split("/")[-1] + '.txt', 'w') as f:  # On les sauvegarde dans le dossier output.
        f.write("Nom fichier : " + pdf + "\n\n")
        f.write("Titre : " + dict_results.get("titre") + "\n\n")
        f.write("Auteurs : ")
        for i in dict_results.get("auteur"):
            f.write(i + "\n")
        f.write("\nAbstract : \n" + dict_results.get("abstract") + "\n\n")
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
    list_auteurs = dict_results.get("auteur")

    i = 0
    while i < len(list_auteurs):
        auteur = SubElement(auteurs, 'auteur')
        if '@' not in list_auteurs[i]:
            name = SubElement(auteur, 'name')
            name.text = list_auteurs[i]
        if i + 1 < len(auteurs) and '@' in auteurs[i + 1] and '@' not in auteurs[i]:
            mail = SubElement(auteur, 'mail')
            mail.text = auteurs[i + 1]
        if len(auteur) == 0:
            auteurs.remove(auteur)
        i += 1

    abstract = SubElement(article, 'abstract')
    abstract.text = dict_results.get("abstract")

    biblio = SubElement(article, 'biblio')
    biblio.text = dict_results.get("biblio")

    tree = ElementTree(article)

    indent(tree, space="\t")

    with open("../output/Sprint2_" + pdf.split("/")[-1] + '.xml', 'w') as f:
        tree.write(f, encoding='unicode')
