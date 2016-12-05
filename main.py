import sys, os, json
from preprocess import parse_text

def main():
	if not os.path.exists('data.json'):
		parse_text()
	with open('data.json', 'r') as fp:
		data = json.load(fp)

	feature_folds = [[]]*5
	label_folds = [[]]*5
	
	# Make folds
	for author in data:
		for ind,passage in enumerate(data[author]):
			feature_folds[ind%5].append(passage)
			label_folds[ind%5].append(author)


	return

if __name__ == '__main__':
	main()