import sys, os, json
from preprocess import parse_text

def main():
	if not os.path.exists('data.json'):
		parse_text()
	with open('data.json', 'r') as fp:
		data = json.load(fp)

	count_passages = 0
	authors = list(data.keys())
	for author in data:
		count_passages += len(data[author])
	print count_passages
	return

if __name__ == '__main__':
	main()