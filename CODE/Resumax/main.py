import os

import fitz

directory = '../ressources/'
for file in os.listdir(directory):
	if not file.endswith(".pdf"):
		continue
	with open(os.path.join(directory, file), 'rb') as pdfFileObj:  # Changes here
		doc = fitz.open(pdfFileObj)
		content = doc[0].get_text("blocks")
		with open(doc.name + '.txt', 'w') as f:
			for i in content:
				f.write(str(i) + "\n")
