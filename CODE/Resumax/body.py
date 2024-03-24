import fitz
import re



def find_body(pdf:str):
    doc = fitz.open(pdf)
    found_intro = False
    do_body = False

    intro = " "
    corps = " "
    for page in doc:
        for block in page.get_text("blocks"):

            # deuxieme partie : stocker l'intro jusqu'a la partie suivante
            if found_intro:

                if not re.fullmatch(r"\A( )*(2|ii|)(?:.|-|)(?: |)(?:\n|)([a-z](?: |))+(?:\n|)", block[4].lower()):
                    intro += block[4]
                else :
                    do_body = True

            # troisième partie : stocker le reste du corps jusqu'aux références
            elif do_body:
                if not re.match(r"references(?: |\n|)+",block[4].lower()):
                    corps += block[4]
                else :
                    return [intro, corps]


            # premiere partie : trouver l'intro
            else :
                if re.match(r"\A( )*(?:[0-9]|i|)(?:.|-|)(?: |)(?:\n|)introduction(?: |)(?:\n|)", block[4].lower()):
                    found_intro = True
                    intro += block[4]





if __name__ == "__main__":
    print("Intro : ")
    print(find_body("../ressources/Gonzalez_2018_Wisebe.pdf"))
    #print("Corps : ")
    #print(find_body("../ressources/Gonzalez_2018_Wisebe.pdf")[1])