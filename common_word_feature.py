import nltk
import numpy as np
import glob
import os
from nltk.corpus import stopwords
from nltk import FreqDist

def feature_extract(paragraph):
    TOP_N_WORDS = 10
    stop_word_list = stopwords.words('english')
    tokens = nltk.word_tokenize(paragraph.lower())
    f_dist = FreqDist(tokens)
    f_dist = f_dist.most_common()
    
    punctuation_list = ['.', ';', '!', ',', '?']
    
    word_found = 0
    #vocab = f_dist.keys()
    
    iter = 0
    word_list = []
    stop_list = []
    while (word_found < TOP_N_WORDS and iter < len(f_dist)):
        #print(f_dist[iter][0])
        if (f_dist[iter][0] not in punctuation_list):
            if (f_dist[iter][0] in stop_word_list):
                if(len(stop_list) < 10):
                    stop_list.append(f_dist[iter][0])
            else:
                if (len(word_list) < 10):
                    word_list.append(f_dist[iter][0])
        iter += 1
    '''
    for word in word_list:
        print(word)
    for word in stop_list:
        print(word)
    '''
    return word_list, stop_list

#if __name__ == "__main__":
#    print(feature_extract("""The cow went into the barn and sat down.
#The cow that sat down in the barn was then milked and went to sleep.
#In the morning the cow did not wake up in the barn, but rather in the field.
#It was a weird day."""))
