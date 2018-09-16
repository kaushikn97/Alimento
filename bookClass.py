import csv

class Book:
    def __init__(self,link=""):
        self.link = link

    def set_description(self, desc):
        self.desc = desc

    def set_title(self,title):
        self.title  = title

    def set_author(self,author):
        self.author = author

    def set_rating(self,rating):
        self.rating  = rating

    def set_genre(self, genre):
        self.genre = genre

    def set_chars(self,chars):
        self.characters = chars

    def set_awards(self,awards):
        self.awards = awards

    def set_all_text(self,all_text):
        self.all_text = all_text

    def set_index(self,index):
        self.index = index

    def get_index(self):
        return self.index

    def set_norm_text(self,norm_text):
        self.norm_text = norm_text

    def write_to_csv_link(self,csv_name):
        with open(csv_name, 'a') as csvFile:
            writer = csv.writer(csvFile)
            row = []
            row.append(self.link)
            writer.writerow(row)

    def write_to_csv_detailed(self,csv_name):
        with open(csv_name, 'a') as csvFile:
            writer = csv.writer(csvFile)
            row = []
            row.append(self.index)
            row.append(self.title)
            row.append(self.author)
            row.append(self.desc)
            row.append(self.rating)
            row.append(self.genre)
            row.append(self.characters)
            row.append(self.awards)
            row.append(self.all_text)
            writer.writerow(row)
    def write_to_csv_norm(self,csv_name):
        with open(csv_name, 'a') as csvFile:
            writer = csv.writer(csvFile)
            row = []
            row.append(self.index)
            row.append(self.title)
            row.append(self.author)
            row.append(self.desc)
            row.append(self.rating)
            row.append(self.genre)
            row.append(self.characters)
            row.append(self.awards)
            row.append(self.all_text)
            row.append(self.norm_text)
            writer.writerow(row)
