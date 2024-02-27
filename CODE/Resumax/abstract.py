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
    abstract = abstract.replace("- \n", "")
    abstract = abstract.replace("\n", " ")  # retour à la ligne dans un paragraphe, donc on remplace par " ".
    return abstract