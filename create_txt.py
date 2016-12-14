import os

# Returns dictionary mapping authors to list of passages
def create_resources():
    directory = os.listdir('AUTHORS')
    bigrams = {}
    words = {}
    for author in directory:
        files = os.listdir('AUTHORS/' + author)
        for textfile in files:
            try:
                # Load initial data
                with open('AUTHORS/' + author + '/' + textfile, 'r') \
                        as INPUTFILE:
                    text = INPUTFILE.read().encode('latin-1')
                    retrieve_counts(bigrams, words, text.lower().split())
            except:
                pass

    with open('bigrams.txt', 'w') as fp:
        count = 0
        for val in sorted(bigrams, key=bigrams.get, reverse=True):
            if count >= 100:
                break
            fp.write(val + '\n')
            count += 1

    with open('words.txt', 'w') as fp:
        count = 0
        for val in sorted(words, key=words.get, reverse=True):
            if count >= 100:
                break
            fp.write(val + '\n')
            count += 1

    return


def retrieve_counts(bigrams, words, text):
    for token in text:
        words[token] = words.get(token, 0) + 1
        for b in [token[i:i+3] for i in range(len(token)-2)]:
            bigrams[b] = bigrams.get(b, 0) + 1

if __name__ == '__main__':
    create_resources()
