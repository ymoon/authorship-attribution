import numpy as np
from collections import OrderedDict
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag


# Get style features based on sentence structure
def get_stylometry_features(passage):
    stylo_fv = np.zeros(8)

    # note: the nltk.word_tokenize includes punctuation
    tokens = word_tokenize(passage.lower())
    sentences = sent_tokenize(passage.lower())
    vocab = set(tokens)
    words_per_sentence = np.array([len(word_tokenize(s))
                                   for s in sentences])

    avg_tags = 0
    tags = set()
    for i in sentences:
        for word, tag in pos_tag(word_tokenize(i)):
            tags.add(tag)
        avg_tags += len(tags)
        tags.clear()

    # average number of words per sentence
    stylo_fv[0] = words_per_sentence.mean()
    # sentence length variation
    stylo_fv[1] = words_per_sentence.std()
    # Lexical diversity
    stylo_fv[2] = len(vocab) / float(len(tokens))
    # Average unique POS tags per sentence
    stylo_fv[3] = float(avg_tags) / float(len(sent_tokenize(passage)))

    # Commas per sentence
    stylo_fv[4] = tokens.count(",") / float(len(sentences))
    # Semicolons per sentence
    stylo_fv[5] = tokens.count(";") / float(len(sentences))
    # Colons per sentence
    stylo_fv[6] = tokens.count(":") / float(len(sentences))
    # Apostrophes per sentence
    stylo_fv[7] = tokens.count("!") / float(len(sentences))

    return stylo_fv


# Get features based on character n-grams
def get_n_gram_features(passage):
    # Load bigrams file
    bigrams = set()
    with open('bigrams.txt', 'r') as INPUTFILE:
        for line in INPUTFILE.readlines():
            bigrams.add(line)

    bigram_frequency = OrderedDict()
    for i in bigrams:
        bigram_frequency[i] = 0
    for first, second, third in zip(passage, passage[1:], passage[2:]):
        bigram = first + second + third
        if bigram in bigrams:
            bigram_frequency[bigram] += 1

    bigrams_list = []
    for key, value in bigram_frequency.items():
        bigrams_list.append(value)
    return bigrams_list
