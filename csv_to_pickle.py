from bookClass import Book
import csv
import os
import pickle

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
for row in rows:
    print(index)
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
    Books.append(oneBook)
    index = index + 1
pickle_out = open(os.getcwd() + "/book_info.pickle","wb")
pickle.dump(Books, pickle_out)
pickle_out.close()
