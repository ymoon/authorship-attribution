from preprocess_sample import parse_text
from main import main

authors = ['ARISTOTLE', 'DICKENS', 'DOYLE', 'EMERSON', 'HAWTHORNE', 'IRVING', 'KANT', 'KEATS', 'MILTON', 'PLATO', 'POE', 'TWAIN', 'WILDE']

for i in range(len(authors)):
	for j in range(i + 1, len(authors)):
		compare = [authors[i], authors[j]]
		# parse_text(compare)
		main(compare)