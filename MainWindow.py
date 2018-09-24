import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import autocomplete
import os
import pickle
from preproc import TrieNode,PostingsList,Node
import search

class Main_Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Libro - The ultimate book search'
        self.left = 10
        self.top = 10
        self.width = 1360
        self.height = 640
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.currenttext=""

        #create search_box
        self.searchbox=QComboBox(self)
        self.searchbox.move(500,90)
        self.searchbox.resize(280,40)
        self.searchbox.setEditable(True)
        self.searchbox.lineEdit().textEdited.connect(self. auto_complete_functionality)
        self.searchbox.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.searchbox.activated.connect(self.setting_index)

        #create a button
        self.searchbutton=QPushButton('Search',self)
        self.searchbutton.move(800,95)

        #connect button to on_click
        self.searchbutton.clicked.connect(self.on_click)

        #adding searchbox and search button in a horizontal layout
        search_layout=QHBoxLayout();
        search_layout.addWidget(self.searchbox)
        search_layout.addWidget(self.searchbutton)

        #adding search_layout to a vertical layout
        total_result_layout=QVBoxLayout()

        #defining the label to display the book names
        self.rlabel=[]
        for i in range(1,11):
            self.rlabel.append(QLabel(self))

        #label if the query entered is not correct
        self.incorrect_query=QLabel(self)
        self.incorrect_query.setText('No Results Found. Try again.')
        self.incorrect_query.move(80,150)
        self.incorrect_query.resize(250,30)

        #aligning the text to left for all the labels
        for i in range(0,10):
            self.rlabel[i].setAlignment(Qt.AlignLeft)
        #definig the titles
        self.titles=[]
        for i in range(1,7):
            self.titles.append(QLabel(self))
        #moving the titles to appropriate positions
        self.titles[0].move(40,150)
        self.titles[1].move(80,150)
        self.titles[2].move(550,150)
        self.titles[3].move(750,150)
        self.titles[4].move(950,150)
        self.titles[5].move(1150,145)

        #resize all the titles
        for i in range(0,5):
            self.titles[i].resize(200,30)
        #set the text value for the values
        self.titles[0].setText("S.No.")
        self.titles[1].setText("Title")
        self.titles[2].setText("Author")
        self.titles[3].setText("Rating")
        self.titles[4].setText("Genre")
        self.titles[5].setText("Similar results")
        #positioning the labels
        for i in range(0,10):
            self.rlabel[i].move(80,190+ 40*i)

        #resizing the label
        for i in range(0,10):
            self.rlabel[i].resize(400,30)

        #setting some initial text for the labels
        for i in range(0,10):
            self.rlabel[i].setText('0')

        #defining the serial number labels
        self.serial_no=[]
        for i in range(0,10):
            self.serial_no.append(QLabel(self))
        #setting the values of the serial labels
        for i in range(0,10):
            self.serial_no[i].setText(str(i+1)+".")
        #moving the serial labels
        for i in range(0,10):
            self.serial_no[i].move(40,182 + 40*i)
        #resizing the serial labels
        for i in range(0,10):
            self.serial_no[i].resize(50,30)
        #defining all the view buttons for the 10 search results
        self.rbutton=[]
        for i in range(1,11):
            self.rbutton.append(QPushButton('View',self))

        #setting the buttons position
        for i in range(0,10):
            self.rbutton[i].move(1150, 175 +40*i)

        #setting the size of the buttons
        for i in range(0,10):
            self.rbutton[i].resize(100,30)

        #defining author label
        self.author_label=[]
        for i in range(0,10):
            self.author_label.append(QLabel(self))

        #setting the position of the author label
        for i in range(0,10):
            self.author_label[i].move(550,180 +40*i)

        #resize the author label
        for i in range(0,10):
            self.author_label[i].resize(200,30)

        #defining rating label
        self.rating_label=[]
        for i in range(0,10):
            self.rating_label.append(QLabel(self))

        #setting the position of the rating label
        for i in range(0,10):
            self.rating_label[i].move(750,180 +40*i)

        #resize the rating label
        for i in range(0,10):
            self.rating_label[i].resize(200,30)

        #defining genre label
        self.genre_label=[]
        for i in range(0,10):
            self.genre_label.append(QLabel(self))

        #setting the position of the author label
        for i in range(0,10):
            self.genre_label[i].move(950,180 +40*i)

        #resize the author label
        for i in range(0,10):
            self.genre_label[i].resize(200,30)

        #layout for incorrect query
        incorrect_query_layout=QHBoxLayout()
        incorrect_query_layout.addWidget(self.incorrect_query)

        #defining 10 horizontal layouts
        result_layout=[]
        for i in range(1,11):
            result_layout.append(QHBoxLayout())
        #defining a layout for all the titles
        title_layout=QHBoxLayout()
        for i in range(0,6):
            title_layout.addWidget(self.titles[i])
        #adding the labels  to the layout
        for i in range(0,10):
            result_layout[i].addWidget(self.serial_no[i])
        for i in range(0,10):
            result_layout[i].addWidget(self.rlabel[i])
        for i in range(0,10):
            result_layout[i].addWidget(self.author_label[i])
        for i in range(0,10):
            result_layout[i].addWidget(self.rating_label[i])
        for i in range(0,10):
            result_layout[i].addWidget(self.genre_label[i])
        #adding the buttons to the layout
        for i in range(0,10):
            result_layout[i].addWidget(self.rbutton[i])

        #adding all the horizontal layout to a vertical layout
        total_result_layout.addLayout(incorrect_query_layout)
        total_result_layout.addLayout(title_layout)
        for i in range(0,10):
            total_result_layout.addLayout(result_layout[i])

        #initially hide all the buttons
        for i in range(0,10):
            self.rbutton[i].hide()

        #hide all the labels initially
        self.incorrect_query.hide()
        for i in range(0,6):
            self.titles[i].hide()
        for i in range(0,10):
            self.serial_no[i].hide()
        for i in range(0,10):
            self.rlabel[i].hide()
        for i in range(0,10):
            self.author_label[i].hide()
        for i in range(0,10):
            self.genre_label[i].hide()
        for i in range(0,10):
            self.rating_label[i].hide()
        #total layout for the box
        total_layout=QVBoxLayout()
        total_layout.addLayout(search_layout)
        total_layout.addLayout(total_result_layout)

        self.setLayout(total_layout)
        self.show()

    @pyqtSlot()
    def setting_index(self):
        selected_text=self.searchbox.currentText()
        self.searchbox.lineEdit().setText(selected_text)
        self.currenttext=selected_text


    @pyqtSlot()
    def on_click(self):

        self.statusBar().showMessage('Getting data...')

        searchboxValue = self.searchbox.currentText()
        #send this search query to kaushik and get back top 10 results in the form of a list or something
        books_result = search.search_query(searchboxValue)
        if not books_result:
            self.incorrect_query.show()
            for i in range(0,6):
                self.titles[i].hide()
            for i in range(0,10):
                self.serial_no[i].hide()
            for i in range(0,10):
                self.rlabel[i].hide()
            for i in range(0,10):
                self.author_label[i].hide()
            for i in range(0,10):
                self.genre_label[i].hide()
            for i in range(0,10):
                self.rating_label[i].hide()
            for i in range(0,10):
                self.rbutton[i].hide()
        else:
            self.incorrect_query.hide()
            for i in range(0,10):
                self.rlabel[i].setText(books_result[i].title)
                self.author_label[i].setText(books_result[i].author)
                self.genre_label[i].setText(books_result[i].genre)
                self.rating_label[i].setText(books_result[i].rating)

            for i in range(0,6):
                self.titles[i].show()

            for i in range(0,10):
                self.serial_no[i].show()

            for i in range(0,10):
                self.rlabel[i].show()

            for i in range(0,10):
                self.rbutton[i].show()

            for i in range(0,10):
                self.author_label[i].show()

            for i in range(0,10):
                self.genre_label[i].show()

            for i in range(0,10):
                self.rating_label[i].show()
        self.statusBar().showMessage('Search Complete')

    @pyqtSlot()
    def auto_complete_functionality(self):
        #if self.currenttext!="":
        print(self.searchbox.lineEdit().text())
        self.currenttext=self.searchbox.lineEdit().text()
        n=self.searchbox.count()
        #setting the combobox as null
        for i in range(n-1):
            self.searchbox.removeItem(1)
        self.searchbox.lineEdit().setText(self.currenttext)
        words=[]
        #the query entered so far is stored here
        searchboxValue=self.searchbox.lineEdit().text()
        print(searchboxValue)
        words=searchboxValue.split(' ')
        #will pass words[-1] to kaushik and he will return a list of words "listed"
        listed = autocomplete.search_prefix(words[-1])
        listed.insert(0," ")
        if words!="":
            words.pop()
        sentence=""
        #for showying the whole quwry along with the autocomplete
        for val in words:
            sentence=sentence+val+' '

        list_enter=[]
        #0 index will have the query you have written so far
        self.searchbox.setItemText(0,searchboxValue)
        #appending the autocomplete word to the sentence
        for value in listed:
            value=sentence+value
            list_enter.append(value)
        #sending the list to the combobox
        self.searchbox.addItems(list_enter)
        self.searchbox.removeItem(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_Window()
    sys.exit(app.exec_())
