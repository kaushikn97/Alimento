import os
import pickle
from preproc import TrieNode,PostingsList,Node

def search_prefix(prefix):
    pickle_in = open(os.getcwd() + "/trie_whole_words.pickle","rb")
    root = pickle.load(pickle_in)
    empty_list = []
    not_done = True
    index = 0
    while(not_done):
        if index == len(prefix):
            not_done = False
            word_list = []
            find_all_words(root,prefix,word_list)
            for word in word_list:
                word = prefix
            if(len(word_list)<10)
                return word_list
            else
                return empty_list
        found = 0

        for child in root.children:
            if child.char == prefix[index]:
                root = child
                index += 1
                found = 1
                break

        if found == 0:
            return empty_list

def find_all_words(root,curr_word,word_list):
    node = root
    if node.word_finished == True :
        word_list.append(curr_word)

    for child in node.children:
        find_all_words(child,curr_word + child.char,word_list)
