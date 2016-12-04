# from nltk.tokenize import sent_tokenize, word_tokenize
import os

def parse_text():
	directory = os.listdir('AUTHORS')
	result = {}
	for author in directory:
		result[author] = []
		files = os.listdir('AUTHORS/' + author)
		for file in files:
			with open('AUTHORS/' + author + '/' + file, 'r') as INPUTFILE:
				text = INPUTFILE.read()
			paragraphs = text.split('\n\n'):
			for paragraph in paragraphs:
				if len(paragraph.split()) > 10:
					result[author].append(paragraph)
		print '\n'
	return

if __name__ == '__main__':
	parse_text()