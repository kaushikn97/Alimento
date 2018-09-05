import csv
from bookClass import Book
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import pickle

filename = "data.csv"

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    rows = []
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
Books = []
for row in rows:
    Books.append(Book(row[0]))

pickle_in = open(os.getcwd() + "/book_index.pickle","rb")
index = pickle.load(pickle_in)
#index = 444
for oneBook in Books[index:]:
    print(index+1)
    address = 'https://www.goodreads.com'+ oneBook.link

    page = urlopen(address)

    print("Got page")

    soup = BeautifulSoup(page, 'html.parser')

    print("Parsed page")

    title_box = soup.find('h1', attrs={'id':'bookTitle'})
    title = title_box.text.strip()

    author_box = soup.find('span', attrs={'itemprop':'name'})
    author = author_box.text.strip()

    rating_box = soup.find('span', attrs={'class':'average'})
    rating = rating_box.text.strip()

    awards = []
    for award in soup.find_all('a',attrs={'class':'award'}):
        awards.append(award.text.strip())

    genre_box = soup.find('a', attrs={'class':'actionLinkLite bookPageGenreLink'})
    if genre_box is not None:
        genre = genre_box.text.strip()
    else:
        genre = ""
    desc_box = soup.find('div', attrs={'class':'readable stacked'})
    if desc_box is not None:
        descs = desc_box.findChildren("span" , recursive=False)
        if(len(descs)==2):
            desc = descs[1].text.strip()
        else:
            desc = descs[0].text.strip()
    else:
        desc = ""
    chars = []
    for box in soup.find_all('a',attrs={'class':'clearFloats'}):
        charBox = box.find('div',attrs={'class':'infoBoxRowTitle'})
        if(charBox.text.strip() == "Characters"):
            charItems = box.find('div',attrs={'class':'infoBoxRowItem'}).findChildren("a" , recursive=False)
            charDescs = []
            for item in charItems:
                charDescs.append(item.text.strip())
            chars.append(charDescs)

    oneBook.set_title(title)
    oneBook.set_author(author)
    oneBook.set_genre(genre)
    oneBook.set_description(desc)
    oneBook.set_rating(rating)
    oneBook.set_awards(awards)
    oneBook.set_chars(chars)

    all_text = oneBook.title + "\n" + oneBook.author + "\n" + oneBook.genre + "\n" + oneBook.desc + "\n" + oneBook.rating + "\n"

    for award in oneBook.awards:
        all_text = all_text + award + ", "

    all_text = all_text[:-2]
    all_text = all_text + "\n"

    for char in oneBook.characters:
        all_text = all_text + char + ", "

    all_text = all_text[:-1]
    oneBook.set_all_text(all_text)
    oneBook.set_index(index+1)
    oneBook.write_to_csv_detailed('details.csv')
    index = index+1

    pickle_index = open(os.getcwd() + "/book_index.pickle","wb")
    pickle.dump(index, pickle_index)
    pickle_index.close()

pickle_out = open(os.getcwd() + "/book_info.pickle","wb")
pickle.dump(Books, pickle_out)
pickle_out.close()
