from bookClass import Book
import preproc
import csv
import os
import pickle
from typing import Tuple
import math
import sys

def get_newidf(word,Books):

    count = 0
    total = len(Books)

    for book in Books:
        if word in book.norm_text :
            count = count + 1

    return 1+math.log(total+1/count+1)


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
    query_vector=[]
    pickle_in = open(os.getcwd() + "/dictionary.pickle","rb")
    dictionary = pickle.load(pickle_in)
    
    pickle_in = open(os.getcwd() + "/doc_vectors.pickle","rb")
    vectors = pickle.load(pickle_in)

    words_added=[]

    magnitude=0
    for word in dictionary:
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
        cosine_dis=[]
        index=0    
        for temp_vec in vectors:
            temp_dis=0
            for i in range(len[temp_vec]):
                temp_dis = temp_dis + temp_vec[i]*query_vector[i]
            cosine_dis[index]=(index,temp_dis)
            index=index + 1    

            cosine_dist=cosine_dist[0:1]+sorted(cosine_dist[1:],key= lambda x:x[1])

        i=1
        while i<11 :
            print (cosine_dist[i][0])
            i=i+1
    else:
        print ("No results found")

    #return a list of objects
