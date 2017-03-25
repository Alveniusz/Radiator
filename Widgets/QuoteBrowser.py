from PySide.QtGui import *
from PySide.QtCore import *

import json

QUOTES_LIST_FILE = "Config/quoteList.cfg"


class AddQuote(QDialog):
    def __init__(self, parent=None, oldQuote ="", oldAuthor = "", oldDate = ""):
        super().__init__(parent)
        self.setWindowTitle("Add new quote")
        self.setFocus()

        self.setMinimumWidth(400)

        self.quote = oldQuote
        self.author = oldAuthor
        self.date = oldDate

        self.quoteInput = QLineEdit()
        self.quoteInput.setText(self.quote)
        self.quoteInput.setPlaceholderText("New quote")
        self.authorInput = QLineEdit()
        self.authorInput.setText(self.author)
        self.authorInput.setPlaceholderText("Author")

        self.okButton = QPushButton("Ok")
        self.okButton.setDefault(True)
        self.cancelButton = QPushButton("Cancel")

        verLayout = QVBoxLayout()
        horLayout = QHBoxLayout()

        horLayout.addWidget(self.okButton)
        horLayout.addWidget(self.cancelButton)

        verLayout.addWidget(self.quoteInput)
        verLayout.addWidget(self.authorInput)
        verLayout.addLayout(horLayout)

        self.setLayout(verLayout)

        self.connect(self.cancelButton, SIGNAL('clicked()'), self.reject)
        self.connect(self.okButton, SIGNAL('clicked()'), self.accept)


    def accept(self):
        self.quote = self.quoteInput.text()
        self.author = self.authorInput.text()
        if self.author == "":
            self.author = "NN"
        if self.date == "":
            self.date = QDate.currentDate().toString("dd-MM-yyyy")

        if self.quote:
            super().accept()


class QuoteBrowser(QDialog):
    def __init__(self, parent=None, const = False):
        super().__init__(parent)
        self.setWindowTitle("Select quote")
        self.setMinimumWidth(1000)

        self.constQuote = const

        self.initWidgets()
        self.connectSignals()

        self.loadList()
        self.updateList()

        self.quoteRes = ""
        self.authorRes = ""

    def initWidgets(self):
        self.okButton = QPushButton("Ok")
        self.okButton.setDefault(True)
        self.applyButton = QPushButton("Apply")
        self.cancelButton = QPushButton("Cancel")

        self.addButton = QPushButton("Add quote")
        self.editButton = QPushButton("Edit quote")
        self.deleteButton = QPushButton("Delete quote")

        self.setConstantBox = QCheckBox("Set constant quote")
        self.setConstantBox.setChecked(self.constQuote)

        self.listWidget = QListWidget()
        self.listWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        verLayout = QVBoxLayout()
        horLayout = QHBoxLayout()
        sidLayout = QVBoxLayout()
        lowLayout = QHBoxLayout()

        sidLayout.addWidget(self.addButton)
        sidLayout.addWidget(self.editButton)
        sidLayout.addWidget(self.deleteButton)
        sidLayout.addStretch()

        horLayout.addWidget(self.listWidget, 8)
        horLayout.addLayout(sidLayout, 2)

        lowLayout.addWidget(self.okButton)
        lowLayout.addWidget(self.applyButton)
        lowLayout.addWidget(self.cancelButton)

        verLayout.addLayout(horLayout)
        verLayout.addWidget(self.setConstantBox)
        verLayout.addLayout(lowLayout)

        self.setLayout(verLayout)

    def connectSignals(self):
        self.connect(self.cancelButton, SIGNAL('clicked()'), self.reject)
        self.connect(self.applyButton, SIGNAL('clicked()'), self.apply)
        self.connect(self.okButton, SIGNAL('clicked()'), self.accept)
        self.connect(self.addButton, SIGNAL('clicked()'), self.addQuote)
        self.connect(self.editButton, SIGNAL('clicked()'), self.editQuote)
        self.connect(self.deleteButton, SIGNAL('clicked()'), self.deleteQuote)
        self.connect(self.listWidget,SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.accept)

    def accept(self):
        selected = self.listWidget.currentRow()
        if selected >= 0 :
            self.quoteRes = self.quoteList[selected]["quote"]
            self.authorRes = self.quoteList[selected]["author"]
        self.constQuote = self.setConstantBox.isChecked()
        self.saveList()
        super().accept()

    def apply(self):
        self.saveList()
        self.reject()

    def addQuote(self):
        aq = AddQuote(self)
        res = aq.exec_()
        if res:
            quote = {"quote":aq.quote, "author":aq.author, "date":aq.date}
            self.quoteList.append(quote)
            self.updateList()

    def editQuote(self):
        selected = self.listWidget.currentRow()
        if selected >= 0 :
            quote = self.quoteList[selected]
            aq = AddQuote(self, quote["quote"], quote["author"], quote["date"])
            res = aq.exec_()
            if res:
                quote = {"quote":aq.quote, "author":aq.author, "date":aq.date}
                self.quoteList[selected] = quote
                self.updateList()

    def deleteQuote(self):
        selected = self.listWidget.currentRow()
        if selected >= 0 :
            self.quoteList.pop(selected)
            self.updateList()

    def loadList(self):
        try:
            with open(QUOTES_LIST_FILE, 'r') as infile:
                self.quoteList = json.load(infile)
        except ValueError:
            self.quoteList = []

    def saveList(self):
        with open(QUOTES_LIST_FILE, 'w') as outfile:
            json.dump(self.quoteList, outfile, ensure_ascii=False)

    def updateList(self):
        self.listWidget.clear()

        for q in self.quoteList:
            line = self.truncateString(q["quote"], 55 ) + " | "
            line += self.truncateString(q["author"], 25 ) + " | "
            line += q["date"]
            self.listWidget.addItem(line)

        for i in range( self.listWidget.count() ):
            self.listWidget.item(i).setFont(QFont("Courier",10,QFont.Monospace))

    def truncateString(self, s, m):
        if m < 2:
            raise ValueError()
        if len(s) < m:
            return s + " "*(m-len(s))
        else :
            return s[:m-2] + ".."