import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#import SearchWindow
import autocomplete
import os
import pickle
from preproc import TrieNode,PostingsList,Node
import search

class Main_Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Libro'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 640
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.currenttext=""
        #self.window= QtWidget();
        #create search_box
        self.searchbox=QComboBox(self)
        self.searchbox.move(150,90)
        self.searchbox.resize(280,40)
        self.searchbox.setEditable(True)
        self.searchbox.lineEdit().textEdited.connect(self. auto_complete_functionality)
        self.searchbox.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.searchbox.activated.connect(self.setting_index)

        #create a button
        self.searchbutton=QPushButton('Search',self)
        self.searchbutton.move(450,95)
        #connect button to on_click
        self.searchbutton.clicked.connect(self.on_click)
        #adding searchbox and search button in a horizontal layout
        search_layout=QHBoxLayout();
        search_layout.addWidget(self.searchbox)
        search_layout.addWidget(self.searchbutton)
        #adding search_layout to a vertical layout
        total_result_layout=QVBoxLayout()
        #defining the label to display the book names
        self.rlabel1=QLabel(self)
        self.rlabel2=QLabel(self)
        self.rlabel3=QLabel(self)
        self.rlabel4=QLabel(self)
        self.rlabel5=QLabel(self)
        self.rlabel6=QLabel(self)
        self.rlabel7=QLabel(self)
        self.rlabel8=QLabel(self)
        self.rlabel9=QLabel(self)
        self.rlabel10=QLabel(self)
        #a label if the query entered is not correct
        self.incorrect_query=QLabel(self)
        self.incorrect_query.setText('No Results Found. Try again.')
        self.incorrect_query.move(80,150)
        self.incorrect_query.resize(250,30)
        #aligning the text to left for all the labels
        self.rlabel1.setAlignment(Qt.AlignLeft)
        self.rlabel2.setAlignment(Qt.AlignLeft)
        self.rlabel3.setAlignment(Qt.AlignLeft)
        self.rlabel4.setAlignment(Qt.AlignLeft)
        self.rlabel5.setAlignment(Qt.AlignLeft)
        self.rlabel6.setAlignment(Qt.AlignLeft)
        self.rlabel7.setAlignment(Qt.AlignLeft)
        self.rlabel8.setAlignment(Qt.AlignLeft)
        self.rlabel9.setAlignment(Qt.AlignLeft)
        self.rlabel10.setAlignment(Qt.AlignLeft)
        #positioning the labels
        self.rlabel1.move(80,180)
        self.rlabel2.move(80,220)
        self.rlabel3.move(80,260)
        self.rlabel4.move(80,300)
        self.rlabel5.move(80,340)
        self.rlabel6.move(80,380)
        self.rlabel7.move(80,420)
        self.rlabel8.move(80,460)
        self.rlabel9.move(80,500)
        self.rlabel10.move(80,540)
        #resizing the label
        self.rlabel1.resize(380,30)
        self.rlabel2.resize(380,30)
        self.rlabel3.resize(380,30)
        self.rlabel4.resize(380,30)
        self.rlabel5.resize(380,30)
        self.rlabel6.resize(380,30)
        self.rlabel7.resize(380,30)
        self.rlabel8.resize(380,30)
        self.rlabel9.resize(380,30)
        self.rlabel10.resize(380,30)
        #setting some initial text for the labels
        self.rlabel1.setText('1')
        self.rlabel2.setText('2')
        self.rlabel3.setText('3')
        self.rlabel4.setText('4')
        self.rlabel5.setText('5')
        self.rlabel6.setText('6')
        self.rlabel7.setText('7')
        self.rlabel8.setText('8')
        self.rlabel9.setText('9')
        self.rlabel10.setText('10')
        #defining all the view buttons for the 10 search results
        self.rbutton1=QPushButton('View',self)
        self.rbutton2=QPushButton('View',self)
        self.rbutton3=QPushButton('View',self)
        self.rbutton4=QPushButton('View',self)
        self.rbutton5=QPushButton('View',self)
        self.rbutton6=QPushButton('View',self)
        self.rbutton7=QPushButton('View',self)
        self.rbutton8=QPushButton('View',self)
        self.rbutton9=QPushButton('View',self)
        self.rbutton10=QPushButton('View',self)
        #setting the buttons position
        self.rbutton1.move(450,170)
        self.rbutton2.move(450,210)
        self.rbutton3.move(450,250)
        self.rbutton4.move(450,290)
        self.rbutton5.move(450,330)
        self.rbutton6.move(450,370)
        self.rbutton7.move(450,410)
        self.rbutton8.move(450,450)
        self.rbutton9.move(450,490)
        self.rbutton10.move(450,530)
        #setting the size of the buttons
        self.rbutton1.resize(100,30)
        self.rbutton2.resize(100,30)
        self.rbutton3.resize(100,30)
        self.rbutton4.resize(100,30)
        self.rbutton5.resize(100,30)
        self.rbutton6.resize(100,30)
        self.rbutton7.resize(100,30)
        self.rbutton8.resize(100,30)
        self.rbutton9.resize(100,30)
        self.rbutton10.resize(100,30)
        #layout for incorrect query
        incorrect_query_layout=QHBoxLayout()
        incorrect_query_layout.addWidget(self.incorrect_query)
        #defining 10 horizontal layouts
        result_layout1=QHBoxLayout()
        result_layout2=QHBoxLayout()
        result_layout3=QHBoxLayout()
        result_layout4=QHBoxLayout()
        result_layout5=QHBoxLayout()
        result_layout6=QHBoxLayout()
        result_layout7=QHBoxLayout()
        result_layout8=QHBoxLayout()
        result_layout9=QHBoxLayout()
        result_layout10=QHBoxLayout()
        #adding the labels  to the layout
        result_layout1.addWidget(self.rlabel1)
        result_layout2.addWidget(self.rlabel2)
        result_layout3.addWidget(self.rlabel3)
        result_layout4.addWidget(self.rlabel4)
        result_layout5.addWidget(self.rlabel5)
        result_layout6.addWidget(self.rlabel6)
        result_layout7.addWidget(self.rlabel7)
        result_layout8.addWidget(self.rlabel8)
        result_layout9.addWidget(self.rlabel9)
        result_layout10.addWidget(self.rlabel10)
        #adding the buttons to the layout
        result_layout1.addWidget(self.rbutton1)
        result_layout2.addWidget(self.rbutton2)
        result_layout3.addWidget(self.rbutton3)
        result_layout4.addWidget(self.rbutton4)
        result_layout5.addWidget(self.rbutton5)
        result_layout6.addWidget(self.rbutton6)
        result_layout7.addWidget(self.rbutton7)
        result_layout8.addWidget(self.rbutton8)
        result_layout9.addWidget(self.rbutton9)
        result_layout10.addWidget(self.rbutton10)
        #adding all the horizontal layout to a vertical layout
        total_result_layout.addLayout(incorrect_query_layout)
        total_result_layout.addLayout(result_layout1)
        total_result_layout.addLayout(result_layout2)
        total_result_layout.addLayout(result_layout3)
        total_result_layout.addLayout(result_layout4)
        total_result_layout.addLayout(result_layout5)
        total_result_layout.addLayout(result_layout6)
        total_result_layout.addLayout(result_layout7)
        total_result_layout.addLayout(result_layout8)
        total_result_layout.addLayout(result_layout9)
        total_result_layout.addLayout(result_layout10)
        #initially hide all the buttons
        self.rbutton1.hide()
        self.rbutton2.hide()
        self.rbutton3.hide()
        self.rbutton4.hide()
        self.rbutton5.hide()
        self.rbutton6.hide()
        self.rbutton7.hide()
        self.rbutton8.hide()
        self.rbutton9.hide()
        self.rbutton10.hide()
        #hide all the labels initially
        self.incorrect_query.hide()
        self.rlabel1.hide()
        self.rlabel2.hide()
        self.rlabel3.hide()
        self.rlabel4.hide()
        self.rlabel5.hide()
        self.rlabel6.hide()
        self.rlabel7.hide()
        self.rlabel8.hide()
        self.rlabel9.hide()
        self.rlabel10.hide()
        #total layout for the box
        total_layout=QVBoxLayout()
        total_layout.addLayout(search_layout)
        total_layout.addLayout(total_result_layout)

        self.setLayout(total_layout)
        self.show()

    @pyqtSlot()
    def setting_index(self):
        selected_text=self.searchbox.currentText()
        #print(selected_text)
        #index=self.searchbox.findText(selected_text,PyQt5.QtCore.Qt.MatchFixedString)
        #print(index)
        self.searchbox.lineEdit().setText(selected_text)

        print(self.searchbox.currentText())
        print('askdfalkdsjhfajdshfljakfhlkajhfljadhslfjkahaldsjkfhaldjfhlad')
        #if index>0:
        #    self.searchbox.setCurrentIndex(index)
    @pyqtSlot()
    def on_click(self):

        self.statusBar().showMessage('Getting data...')

        searchboxValue = self.searchbox.currentText()
        #send this search query to kaushik and get back top 10 results in the form of a list or something
        books_result = search.search_query(searchboxValue)
        if not books_result:
            self.incorrect_query.show()
        else:
            self.rlabel1.show()
            self.rlabel2.show()
            self.rlabel3.show()
            self.rlabel4.show()
            self.rlabel5.show()
            self.rlabel6.show()
            self.rlabel7.show()
            self.rlabel8.show()
            self.rlabel9.show()
            self.rlabel10.show()
            self.rbutton1.show()
            self.rbutton2.show()
            self.rbutton3.show()
            self.rbutton4.show()
            self.rbutton5.show()
            self.rbutton6.show()
            self.rbutton7.show()
            self.rbutton8.show()
            self.rbutton9.show()
            self.rbutton10.show()

        self.statusBar().showMessage('Search Complete')

    @pyqtSlot()
    def auto_complete_functionality(self):
        print('im running')

        n=self.searchbox.count()
        #setting the combobox as null
        for i in range(n):
            self.searchbox.removeItem(1)

        words=[]
        #the query entered so far is stored here
        searchboxValue=self.searchbox.currentText()
        print(searchboxValue)
        words=searchboxValue.split(' ')
        #will pass words[-1] to kaushik and he will return a list of words "listed"
        listed = autocomplete.search_prefix(words[-1])
        listed.insert(0," ")
        print(listed)
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
