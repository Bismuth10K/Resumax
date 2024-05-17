import os


def menu(path_res: str):
	"""
	Créé le menu interactif et propose à l'utilisateur de choisir le ou les pdfs à traiter.

	Args:
		path_res: Chemin vers le dossier contenant les pdfs.

	Returns: Renvoie une liste des chemins vers les pdfs à traiter.
	"""
	pdf_files = []
	i = 0
	print("Voici tous les pdf dans le dossier " + path_res)
	for file in os.listdir(path_res):
		if file.endswith(".pdf"):
			pdf_files.append(file)
			print(i, file)
			i += 1
	print("\nSélectionnez les fichiers à traiter et à parser.")
	choix = input(
		"Tapez les numéros des fichiers (séparés par des espaces) ou 'all' si vous voulez tous les traiter : ")
	if "all" not in choix:
		choix = list(map(int, choix.split()))

		output_files = [os.path.join(path_res, pdf_files[nb]) for nb in choix if len(pdf_files) > nb >= 0]
		return output_files
	else:
		return [os.path.join(path_res, pdf_file) for pdf_file in pdf_files]
