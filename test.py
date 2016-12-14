from main import main

authors = ['ARISTOTLE', 'DICKENS', 'DOYLE', 'EMERSON', 'HAWTHORNE', 'IRVING',
           'KANT', 'KEATS', 'MILTON', 'PLATO', 'POE', 'TWAIN', 'WILDE']

# This script runs the main() function on each of the different authors
# to generate accuracies.
for i in range(len(authors)):
    for j in range(i + 1, len(authors)):
        compare = [authors[i], authors[j]]
        main(compare)
