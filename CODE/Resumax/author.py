import fitz
import re
import titre

def find_authors(page:fitz.Page, blknum:int):
    mails = []
    names = ""
    for block in page.get_text("blocks"):
        if block[5] < blknum :
            continue
        # les auteurs se trouvent pratiquement toujours juste au-dessus de l'abstract
        if "abstract" in block[4].lower():
            blknum = block[5]
            break
        else :
            # si un email est trouvé : on l'ajoute dans la liste et on l'enlève du texte du bloc
            if "@" in block[4]:
                while email(block[4].split(" ")) is not None:
                    m = email(block[4].split(" "))
                    mails.append(m)
                    block[4] = block[4] - m

            # pour les noms, on ajoute ce qui reste du texte du bloc
            names += block[4]
    return names, str(mails), blknum







def email(strings:list):
    for str in strings:
        if "@" in str:
            return str


if __name__ == "__main__":
    d = fitz.open("../ressources/Torres.pdf")
    find_authors(d[0], 1)