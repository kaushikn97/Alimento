from bookClass import Book
import csv
import os
import pickle
from typing import Tuple
import math
import sys

def get_tf(word,terms):

    count = 0
    total = len(terms)

    for term in terms:
        if word == term :
            count = count + 1

    return count/total

def get_idf(word,Books):

    count = 0
    total = len(Books)

    for book in Books:
        if word in book.norm_text :
            count = count + 1

    return 1+math.log(total/count)

class Node:

   def __init__(self,book_id,score,nextNode=None):
       self.book_id = book_id
       self.score = score
       self.nextNode = nextNode

   def get_book_id(self):
       return self.book_id

   def get_score(self):
       return self.score

   def setData(self,val):
       self.data = val

   def getNextNode(self):
       return self.nextNode

class PostingsList:

   def __init__(self,head = None):
       self.head = head
       self.size = 0

   def getSize(self):
       return self.size

   def addNode(self,book_id,score):
       newNode = Node(book_id,score,self.head)
       self.head = newNode
       self.size+=1
       return True

   def find_book_score(self,index):
       curr = self.head
       while curr and curr.get_book_id() != index:
           #print(curr.data)
           curr = curr.getNextNode()

       if curr != None :
           return curr.get_score()
       else :
           return 0


   def printNode(self):
       curr = self.head
       while curr:
           #print(curr.data)
           curr = curr.getNextNode()


class TrieNode(object):

    """
    Our trie node implementation. Very basic. but does the job
    """

    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the word.`
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1
        #Link to inverted index
        self.postings_list = PostingsList()

def insert(root, book_id, score, word: str):
    """
    Adding a word in the trie structure
    """
    node = root
    for char in word:
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found it, increase the counter by 1 to keep track that another
                # word has it as well
                child.counter += 1
                # And point the node to the child that contains this char
                node = child
                found_in_child = True

                break
        # We did not find it so add a new chlid
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    if (score!=-1):
        node.postings_list.addNode(book_id,score)

    node.word_finished = True

def traverse(root,dictionary):

    node = root
    if node.word_finished == True :
        dictionary.append(node.postings_list)

    for child in node.children:
        traverse(child,dictionary)

def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if char_not_found:
            return False, 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter

if __name__ == "__main__":
    filename = "details.csv"

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        rows = []
        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
    Books = []
    index = 0

    normal_root = TrieNode('*')
    whole_root = TrieNode('*')

    for row in rows:
        oneBook = Book()
        oneBook.set_index(row[0])
        oneBook.set_title(row[1])
        oneBook.set_author(row[2])
        oneBook.set_description(row[3])
        oneBook.set_rating(row[4])
        oneBook.set_genre(row[5])
        oneBook.set_chars(row[6])
        oneBook.set_awards(row[7])
        oneBook.set_all_text(row[8])
        index = index + 1

        text = oneBook.all_text;
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

        oneBook.set_norm_text(stemmed)
        Books.append(oneBook)

    dictionary = []

    for book in Books:
        stemmed = book.norm_text
        words_added = []
        #print('**************************************')
        print(book.index)
        for word in stemmed:
            #print(word)
            if word not in words_added:
                insert(normal_root,book.index,get_tf(word,stemmed)*get_idf(word,Books),word)
                words_added.append(word)

    traverse(normal_root,dictionary)
    sys.setrecursionlimit(10000)

    pickle_out = open(os.getcwd() + "/trie_with_vectors.pickle","wb")
    pickle.dump(normal_root, pickle_out)
    pickle_out.close()

    pickle_out = open(os.getcwd() + "/trie_whole_words.pickle","wb")
    pickle.dump(whole_root, pickle_out)
    pickle_out.close()

    pickle_out = open(os.getcwd() + "/dictionary.pickle","wb")
    pickle.dump(dictionary, pickle_out)
    pickle_out.close()
