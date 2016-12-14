import nltk
from collections import OrderedDict
from nltk import FreqDist


# Pull features out of a 100 sentence long string
def feature_extract(paragraph):
    tokens = nltk.word_tokenize(paragraph.lower())
    f_dist = FreqDist(tokens)
    f_dist = f_dist.most_common()

    # Load word file
    words = set()
    with open('words.txt', 'r') as INPUTFILE:
        for line in INPUTFILE.readlines():
            words.add(line)

    # Find frequency of common words
    word_frequency = OrderedDict()
    for i in words:
        word_frequency[i] = 0
    for token in tokens:
        if token in words:
            word_frequency[token] += 1

    word_list = []
    for key, value in word_frequency.items():
        word_list.append(value)

    return word_list
