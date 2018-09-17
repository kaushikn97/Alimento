from bookClass import Book
import preproc
import csv
import os
import pickle
from typing import Tuple
import math
import sys
from preproc import PostingsList,Node

def get_newidf(word,Books):

    count = 0
    total = len(Books)

    for book in Books:
        if word in book.norm_text :
            count = count + 1

    return 1+math.log(total+1/count+1)

def get_tf(word,terms):

    count = 0
    total = len(terms)

    for term in terms:
        if word == term :
            count = count + 1

    return count/total

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

    from nltk.stem.porter import PorterStemmer
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in words]

    #create vector
    query_vector=[]
    pickle_in = open(os.getcwd() + "/dictionary.pickle","rb")
    dictionary = pickle.load(pickle_in)

    pickle_in = open(os.getcwd() + "/doc_vectors.pickle","rb")
    vectors = pickle.load(pickle_in)
    pickle_in = open(os.getcwd() + "/book_with_norm.pickle","rb")
    Books = pickle.load(pickle_in)

    words_added=[]
    result = []
    magnitude = 0
    for (word,postings_list) in dictionary:
        if word in stemmed:
            if word not in words_added:
                score=get_tf(word,stemmed)*get_newidf(word,Books)
                query_vector.append(score)
                words_added.append(word)
                magnitude = magnitude + score*score

        else:
            query_vector.append(0)

    magnitude=math.sqrt(magnitude)

    if magnitude!=0:
        for value in query_vector:
            value=value/magnitude

    #find top 10 closest using cosine distance
        cosine_dist=[]
        index=0
        for vector in vectors[1:]:
            temp_dis=1
            for i in range(len(vector)):
                temp_dis = temp_dis + vector[i]*query_vector[i]

            cosine_dist.append((index,temp_dis))
            index=index + 1

            cosine_dist=sorted(cosine_dist,key = lambda x:(-x[1]))

        for i in range(0,11):
            result.append(Books[cosine_dist[i][0]])
            print(Books[cosine_dist[i][0]].title)
    else:
        print ("No results found")
