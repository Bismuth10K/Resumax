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
