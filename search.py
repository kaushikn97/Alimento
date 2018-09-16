from bookClass import Book
import csv
import os
import pickle
from typing import Tuple
import math
import sys

if __name__ == '__main__':

    text = input('Enter search query: ')
    # split into words
    from nltk.tokenize import word_tokenize
    tokens = word_tokenize(text)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word

    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words

    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    words_unfil = [w for w in words if not w in stop_words]
    # remove all tokens that are not alphabetic
    words = [word for word in words_unfil if word.isalpha()]

    whole_words_added = []
    for word in words:
        if word not in whole_words_added:
            insert(whole_root,oneBook.index,-1,word)
            whole_words_added.append(word)

    from nltk.stem.porter import PorterStemmer
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in words]

    #create vector

    #find top 10 closest using cosine distance

    #return a list of objects
