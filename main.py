import sys, os, json
from preprocess import parse_text
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from stylometry_features import get_stylometry_features
from stylometry_features import get_n_gram_features
from common_word_feature import feature_extract

def getFeatures(passages):
	stylo_features = []
	# bigram_features = []
	# word_features = []
	for p in passages:
		# get stylo feats
		stylo_feats = get_stylometry_features(p)

		# get bigram frequencies
		# bigrams = get_n_gram_features(p)

		# get word frequencies
		# word_freq_list = feature_extract(p)

		# append to feature matrices
		stylo_features.append(stylo_feats)
		# bigram_features.append(bigrams)
		# word_features.append(word_freq_list)

	# return stylo_features, bigram_features, word_features
	return stylo_features


def main():
	# if not os.path.exists('data.json'):
	# 	parse_text()
	# with open('data.json', 'r') as fp:
	# 	data = json.load(fp)

	if not os.path.exists('sample.json'):
		parse_text()
	with open('sample.json', 'r') as fp:
		data = json.load(fp)

	# Initialize dictionaries that contain folds
	feature_folds = {}
	label_folds = {}
	for i in range(5):
		feature_folds[i] = []
		label_folds[i] = []

	# Make folds
	for author in data:
		for ind,passage in enumerate(data[author]):
			feature_folds[ind%5].append(passage)
			label_folds[ind%5].append(author)

	# Initialize classifiers
	stylo_clf = SVC()
	bigram_clf = SVC()
	wordfreq_clf = SVC()

	# Init accuracy sums to get average accuracy across 5 folds
	stylo_acc_sum = 0
	bigram_acc_sum = 0
	wordfreq_acc_sum = 0

	### Run 5 fold cross validation on SVC and SGD classifiers
	for j in range(5):

		train_passages = []
		test_passages = []
		train_labels = []
		test_labels = []

		# Divide passages and labels by folds
		for k in range(5):
			if j != k:
				train_passages += feature_folds[k]
				train_labels += label_folds[k]
			else:
				test_passages += feature_folds[k]
				test_labels += label_folds[k]

		# Get features
		# stylo_train, bigram_train, wordfreq_train = getFeatures(train_passages)
		stylo_train = getFeatures(train_passages)
		# stylo_test, bigram_test, wordfreq_test = getFeatures(test_passages)
		stylo_test = getFeatures(test_passages)

		# Fit SVM stylometry classifier and test
		stylo_clf.fit(stylo_train, train_labels)
		stylo_acc = stylo_clf.score(stylo_test, test_labels)
		stylo_acc_sum += stylo_acc

		'''
		# Fit SVM character bigram classifier and test
		bigram_clf.fit(bigram_train, train_labels)
		bigram_acc = bigram_clf.score(bigram_test, test_labels)
		bigram_acc_sum += bigram_acc

		# Fit SVM stylometry classifier and test
		wordfreq_clf.fit(wordfreq_train, train_labels)
		wordfreq_acc = wordfreq_clf.score(wordfreq_test, test_labels)
		wordfreq_acc_sum += wordfreq_acc
		'''
		'''
		# Fit and test SGD classifier
		sgd_clf.fit(train_features, train_labels)
		sgd_acc = sgd_clf.score(test_features, test_labels)
		sgd_acc_sum += sgd_acc
		print "SGD "+str(j)+" Fold:", sgd_acc
		'''

	# Calculate and print total accuracies
	total_stylo_acc = stylo_acc_sum / 5.0
	# total_bigram_acc = bigram_acc_sum / 5.0
	# total_wordfreq_acc = wordfreq_acc_sum / 5.0

	print "Stylometry accuracy: ", total_stylo_acc
	# print "Bigram freq accuracy: ", total_bigram_acc
	# print "Word freq accuracy: ", total_wordfreq_acc

	return

if __name__ == '__main__':
	main()
