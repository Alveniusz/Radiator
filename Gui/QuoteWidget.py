from PySide.QtGui import *
from PySide.QtCore import *

import json
import random

from Widgets.QuoteBrowser import QuoteBrowser, QUOTES_LIST_FILE

MAX_QUOTE_TEXT_HEIGHT = 50
MAX_QUOTE_TEXT_WIDTH = 1750

class QuoteWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initWidgets()

        self.setQuote("Have a nice day!", "NN")
        self.constantQuote = False
        self.currentQuote = self.quoteLabel.text()
        self.currentAuthor = self.authorLabel.text()

        self.initTimer()


    def initWidgets(self):
        layout = QHBoxLayout(self)

        self.titleLabel = QLabel("Quote of the week", self)

        self.titleLabel.setFont(QFont("Arial", 10, -1, QFont.Cursive))
        self.titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.darkRed)
        self.titleLabel.setPalette(palette)
        layout.addWidget(self.titleLabel, 1)

        self.quoteLabel = QLabel("...")
        self.quoteLabel.setFont(QFont("Arial", 20, -1, QFont.Cursive))
        self.quoteLabel.setAlignment(Qt.AlignCenter)
        palette = QPalette()
        palette.setColor(QPalette.Foreground, QColor(40,40,40))
        self.quoteLabel.setPalette(palette)
        layout.addWidget(self.quoteLabel, 17)


        self.authorLabel = QLabel("< NN >")
        self.authorLabel.setFont(QFont("Arial", 15, -1, QFont.Cursive))
        self.authorLabel.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.darkRed)
        self.authorLabel.setPalette(palette)
        layout.addWidget(self.authorLabel,2)

        self.setLayout(layout)

    def setQuote(self, quote, autor = "NN"):

        self.quoteLabel.setText(quote)
        lines = quote.split("\n")
        maxLine = max( len(l) for l in lines )
        if len(lines) != 0 and maxLine != 0:
            fontSize = min(MAX_QUOTE_TEXT_HEIGHT / len(lines), MAX_QUOTE_TEXT_WIDTH / maxLine )
            self.quoteLabel.setFont(QFont("Arial", fontSize, -1, QFont.Cursive))

        self.authorLabel.setText("< {0} >".format(autor))

    def initTimer(self):
        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'), self.updateTime)
        timer.start(60*60*1000)

    def updateTime(self):
        qtime = QDateTime.currentDateTime()
        qtime = QDateTime()

        if qtime.date().dayOfWeek() > 5 or qtime.date().dayOfWeek() == 5 and qtime.time().hour() > 13:
            self.setWeekendQuote()
        elif not self.constantQuote:
            self.setQuoteFromList()
        else:
            self.setCurrentQuote()


    def setWeekendQuote(self):
        self.currentQuote = self.quoteLabel.text()
        self.currentAuthor = self.authorLabel.text()
        self.setQuote("Piątek, piąteczek, piątunio!", "Kamil W.")

    def setCurrentQuote(self):
        self.setQuote(self.currentQuote, self.currentAuthor)

    def setQuoteFromList(self):
        quoteList = []
        try:
            with open(QUOTES_LIST_FILE, 'r') as infile:
                quoteList = json.load(infile)
        except ValueError:
            return

        if len(quoteList):
            qu = random.choice(quoteList)
            self.currentQuote = qu["quote"].replace("\\n","\n")
            self.currentAuthor = qu["author"]
            self.setCurrentQuote()


    def mouseReleaseEvent(self, ev):
        qb = QuoteBrowser()
        res = qb.exec_()
        if res:
            self.constantQuote = qb.constQuote
            if qb.quoteRes :
                self.currentQuote = qb.quoteRes.replace("\\n","\n")
                self.currentAuthor = qb.authorRes
                print(self.currentQuote)
                self.setCurrentQuote()
