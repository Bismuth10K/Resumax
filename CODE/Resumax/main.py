import fitz

doc = fitz.open("../ressources/Das_Martins.pdf")

for page in doc:
    texte = page.get_text("blocks")
    print(texte)

print("\n\n")

doc2 = fitz.open("../ressources/Gonzalez_2018_Wisebe.pdf")
for page in doc2:
    texte = page.get_text("blocks")
    print(texte)

print("\n\n")

doc3 = fitz.open("../ressources/Mikolov.pdf")
for page in doc3:
    texte = page.get_text("blocks")
    print(texte)

print("\n\n")

doc4 = fitz.open("../ressources/Nasr.pdf")
for page in doc4:
    texte = page.get_text("blocks")
    print(texte)