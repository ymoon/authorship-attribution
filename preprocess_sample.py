from nltk.tokenize import sent_tokenize
import os, json

# Returns dictionary mapping authors to list of passages
def parse_text(compare):
    directory = os.listdir('AUTHORS')
    result = {}


    # Aristotle <-> Dickens 53.7%

    # Remove Burroughs, Jefferson, Shakespeare, Stevenson

    # Burroughs, Dickens, Jefferson, Stevenson
    # write similarly

    # Dickens   <-> Burroughs   52.5%
    # Dickens   <-> Jefferson   56.6%
    # Burroughs <-> Jefferson   54%

    # Dickens   <-> Stevenson   50.2%
    # Burroughs <-> Stevenson   52.8%
    # Jefferson <-> Stevenson   56.8%

    # Burroughs <-> Emerson     65%
    # Dickens   <-> Emerson     62.7%
    # Jefferson <-> Emerson     68.7%
    # Stevenson <-> Emerson     62.5%

    # Burroughs <-> Kant        52.3%
    # Dickens   <-> Kant        68.7%
    # Jefferson <-> Kant        56.4%
    # Stevenson <-> Kant        50.4%   

    # Shakespeare

    # compare = ['JEFFERSON', 'TWAIN']
    # print compare
    print compare
    for author in compare:
        result[author] = []
        files = os.listdir('AUTHORS/' + author)
        count = 0
        for textfile in files:
            if count >= 2:
                break
            try:
                with open('AUTHORS/' + author + '/' + textfile, 'r') as INPUTFILE:
                    text = INPUTFILE.read().encode('latin-1')
                    sentences = sent_tokenize(text)
                    sentences = [' '.join(sentence.split()) for sentence in sentences]
                    sentences = list(chunks(sentences, 50))
                    sentences = [' '.join(sentence) for sentence in sentences]
                    result[author] += sentences
                    count += 1
            except:
                pass

    file_name = '_'.join(compare)               
    with open('samples/' + file_name + '.json', 'w') as fp:
        json.dump(result, fp)

    return

def chunks(l, n):
    # Yield successive n-sized chunks from l
    for i in range(0, len(l), n):
        yield l[i:i + n]

if __name__ == '__main__':
    parse_text()
