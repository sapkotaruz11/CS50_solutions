import nltk
import sys
import os
import string
import math



FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_map = {}
    for files in os.listdir(directory):
        with open(os.path.join(directory, files), encoding='utf8') as f:
            file_map[files] = f.read()
    return file_map


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    stop_words = nltk.corpus.stopwords.words("english")
    string_punctuation = string.punctuation
    sentence = nltk.word_tokenize(document)
    sentence = [word.lower() for word in sentence if word.isalnum()]
    sentence = [word for word in sentence if word not in stop_words and word not in string_punctuation]
    return sorted(sentence)


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set()
    for files in documents:
        for word in documents[files]:
            if word not in words:
                words.add(word)

    idfs = dict()
    for word in words:
        f = sum(word in documents[files] for files in documents)
        idf = math.log(len(documents) / f)
        idfs[word] = idf
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf = {}
    for txt_file in files:
        tfidf[txt_file] = 0
        for word in query:
            tf = files[txt_file].count(word)
            tfidf[txt_file] += tf * idfs[word]
    return sorted(tfidf, key=tfidf.get, reverse=True)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    mwm = []
    for sentence in sentences:
        sentence_mwm_qtd = [sentence, 0, 0]
        for word in query:
            if word in sentences[sentence]:
                sentence_mwm_qtd[1] += idfs[word]
                sentence_mwm_qtd[2] += sentences[sentence].count(word) / len(sentence)
        mwm.append(sentence_mwm_qtd)
    return [sentence for sentence, _, _ in sorted(mwm, key=lambda item: (item[1], item[2]), reverse=True)][:n]


if __name__ == "__main__":
    main()
