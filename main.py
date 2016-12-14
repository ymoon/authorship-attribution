import sys
import json
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from stylometry_features import get_stylometry_features
from stylometry_features import get_n_gram_features
from common_word_feature import feature_extract


# Get features from the 50 sentence passage
def getFeatures(passages):
    stylo_features = []
    bigram_features = []
    word_features = []
    for p in passages:
        # get stylo feats
        stylo_feats = get_stylometry_features(p)

        # get bigram frequencies
        bigrams = get_n_gram_features(p)

        # get word frequencies
        word_freq_list = feature_extract(p)

        # append to feature matrices
        stylo_features.append(stylo_feats)
        bigram_features.append(bigrams)
        word_features.append(word_freq_list)

    return stylo_features, bigram_features, word_features


def main():
    # Load file names from argv
    if len(sys.argv) == 3:
        file_name = sys.argv[1]
        classifier = sys.argv[2]
        print(file_name)
        with open('samples/' + file_name, 'r') as fp:
            data = json.load(fp)
    else:
        classifier = sys.argv[1]
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
        for ind, passage in enumerate(data[author]):
            feature_folds[ind % 5].append(passage)
            label_folds[ind % 5].append(author)

    # Initialize classifiers
    if classifier == 'svm':
        stylo_clf = SVC()
        bigram_clf = SVC()
        wordfreq_clf = SVC()
    elif classifier == 'knn':
        stylo_clf = KNeighborsClassifier(n_neighbors=5)
        bigram_clf = KNeighborsClassifier(n_neighbors=5)
        wordfreq_clf = KNeighborsClassifier(n_neighbors=5)
    elif classifier == 'sgd':
        stylo_clf = SGDClassifier()
        bigram_clf = SGDClassifier()
        wordfreq_clf = SGDClassifier()
    else:
        print("Incorrect classification type")
        sys.exit()

    # Init accuracy sums to get average accuracy across 5 folds
    stylo_acc_sum = 0
    bigram_acc_sum = 0
    wordfreq_acc_sum = 0

    # Run 5 fold cross validation on SVC and SGD classifiers
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
        stylo_train, bigram_train, wordfreq_train = getFeatures(train_passages)
        stylo_test, bigram_test, wordfreq_test = getFeatures(test_passages)

        # Fit SVM stylometry classifier and test
        stylo_clf.fit(stylo_train, train_labels)
        stylo_acc = stylo_clf.score(stylo_test, test_labels)
        stylo_acc_sum += stylo_acc

        # Fit SVM character bigram classifier and test
        bigram_clf.fit(bigram_train, train_labels)
        bigram_acc = bigram_clf.score(bigram_test, test_labels)
        bigram_acc_sum += bigram_acc

        # Fit SVM stylometry classifier and test
        wordfreq_clf.fit(wordfreq_train, train_labels)
        wordfreq_acc = wordfreq_clf.score(wordfreq_test, test_labels)
        wordfreq_acc_sum += wordfreq_acc

    # Calculate and print total accuracies
    total_stylo_acc = stylo_acc_sum / 5.0
    total_bigram_acc = bigram_acc_sum / 5.0
    total_wordfreq_acc = wordfreq_acc_sum / 5.0

    # print "Stylometry accuracy: ", total_stylo_acc
    print("Stylometry feature accuracy: {}".format(total_stylo_acc))
    print("Bigram freq accuracy: {}".forma(total_bigram_acc))
    print("Word freq accuracy: {}{}".forma(total_wordfreq_acc, '\n'))

    return

if __name__ == '__main__':
    main()
