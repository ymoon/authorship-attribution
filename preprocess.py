from nltk.tokenize import sent_tokenize
import os, json

# Returns dictionary mapping authors to list of passages
def parse_text():
	directory = os.listdir('AUTHORS')
	result = {}
	for author in directory:
		result[author] = []
		files = os.listdir('AUTHORS/' + author)
		for file in files:
			conditional = True
			try:
				with open('AUTHORS/' + author + '/' + file, 'r') as INPUTFILE:
					text = INPUTFILE.read()
			except:
				conditional = False
				pass
			if conditional:
				sentences = sent_tokenize(text)
				sentences = [' '.join(sentence.split()) for sentence in sentences]
				sentences = list(chunks(sentences, 50))
				sentences = [' '.join(sentence) for sentence in sentences]
				result[author] += sentences

	with open('data.json', 'w') as fp:
		json.dump(result, fp)

	return

def chunks(l, n):
    # Yield successive n-sized chunks from l
    for i in range(0, len(l), n):
        yield l[i:i + n]

if __name__ == '__main__':
	parse_text()