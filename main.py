import sys, os, json
from preprocess import parse_text
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from stylometry_features import get_stylometry_features
from common_word_feature import feature_extract

def getFeatures(passages):
	features = []
	for p in passages:
		new_feat_vec = []

		# get stylo feats
		lex_feats, punct_feats, bigrams = get_stylometry_features(p)
		# get common/uncommon words lists
		common_list, stop_word_list = feature_extract(p)

		# Concatenate feats
		new_feat_vec.append(lex_feats)
		new_feat_vec.append(punct_feats)
		new_feat_vec.append(bigrams)
		new_feat_vec.append(common_list)
		new_feat_vec.append(stop_word_list)

		# append feature vector
		features.append(new_feat_vec)

def main():
	if not os.path.exists('data.json'):
		parse_text()
	with open('data.json', 'r') as fp:
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
	svc_clf = SVC()
	sgd_clf = SGDClassifier()

	# Init accuracy sums to get average accuracy across 5 folds
	svc_acc_sum = 0
	sgd_acc_sum = 0

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
		train_features = getFeatures(train_passages)
		test_features = getFeatures(test_passages)

		# Fit SVM classifier and test
		svc_clf.fit(train_features, train_labels)
		svc_acc = svc_clf.score(test_features, test_labels)
		svc_acc_sum += svc_acc
		print "SVC "+str(j)+" Fold:", svc_acc

		# Fit and test SGD classifier
		sgd_clf.fit(train_features, train_labels)
		sgd_acc = sgd_clf.score(test_features, test_labels)
		sgd_acc_sum += sgd_acc
		print "SGD "+str(j)+" Fold:", sgd_acc

	# Calculate and print total accuracies
	total_svc_acc = svc_acc_sum / 5.0
	total_sgd_acc = sgd_acc_sum / 5.0

	print "SVC accuracy: ", total_svc_acc
	print "SGD accuracy: ", total_sgd_acc

	return

if __name__ == '__main__':
	main()
