import numpy as np
import nltk
import glob
import os
from nltk.tokenize import sent_tokenize, word_tokenize

def getLexPuncFeatures(passage):
    lex_fv = np.zeros(4)
    punct_fv = np.zeros(4)

    # note: the nltk.word_tokenize includes punctuation
    tokens = nltk.word_tokenize(passage.lower())
    words = word_tokenize(passage.lower())
    sentences = sent_tokenize(passage)
    vocab = set(words)
    words_per_sentence = np.array([len(word_tokenize(s))
                                   for s in sentences])
   
    avg_tags = 0
    tags = set()
    for i in sent_tokenize(passage):
        for word, tag in word_tokenize(i):
            tags.add(tag)
        avg_tags += len(tags)
        tags.clear()

    # average number of words per sentence
    lex_fv[0] = words_per_sentence.mean()
    # sentence length variation
    lex_fv[1] = words_per_sentence.std()
    # Lexical diversity
    lex_fv[2] = len(vocab) / float(len(words))
    # Average unique POS tags per sentence
    lex_fv[3] = float(avg_tags) / float(len(sent_tokenize(passage)))
 
    # Commas per sentence
    punct_fv[0] = tokens.count(",") / float(len(sentences))
    # Semicolons per sentence
    punct_fv[1] = tokens.count(";") / float(len(sentences))
    # Colons per sentence
    punct_fv[2] = tokens.count(":") / float(len(sentences))
    # Apostrophes per sentence
    punct_fv[3] = tokens.count("!") / float(len(sentences))

    return lex_fv, punct_fv
