import os
import pickle
from preproc import TrieNode,PostingsList,Node

count = 0

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
            find_all_words_util(root,prefix,word_list)
            for word in word_list:
                word = prefix
            if(count<10):
                return word_list
            else:
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

def find_all_words_util(root,curr_word,word_list):
    global count

    count = 0

    return find_all_words(root,curr_word,word_list)

def find_all_words(root,curr_word,word_list):
    global count
    node = root
    if node.word_finished == True :
        count = count + 1
        word_list.append(curr_word)

    if count > 10:
        return

    for child in node.children:
        if count > 100:
            return
        find_all_words(child,curr_word + child.char,word_list)
