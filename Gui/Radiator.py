from PySide.QtGui import *
from PySide.QtCore import *

from Gui.MpkListener import MpkListener
from Gui.QuoteWidget import QuoteWidget
from Gui.NotificationLine import NotificationLine

class Radiator(QMainWindow):
    def __init__(self):
        super(Radiator, self).__init__()

        self.setMainWindowsParameters()

        self.initWidgets()
        self.setWidgetsLayout()
        self.showMaximized()

        # self.adjustWidgets()

    def setMainWindowsParameters(self):
        self.setWindowTitle('Radiator')
        palette	= QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("Pictures/Background.jpg")))
        self.setPalette(palette)

    def initWidgets(self):
        # Replace frames with correct widgets when ready

        self.topWidget = QuoteWidget()

        self.topRightWidget = QLabel("Alarm")
        self.topRightWidget.setAlignment(Qt.AlignCenter)
        self.topRightWidget.setFont(QFont("Arial", 27, QFont.Bold))
        self.topRightWidget.setFrameStyle(QFrame.Box)

        self.bottomWidget = NotificationLine()

        self.leftWidget = QLabel("Weather")
        self.leftWidget.setAlignment(Qt.AlignCenter)
        self.leftWidget.setFont(QFont("Arial", 27, QFont.Bold))
        self.leftWidget.setFrameStyle(QFrame.Box)

        self.rightWidget = MpkListener()

    def setWidgetsLayout(self):
        mainVerticalLayout = QVBoxLayout()
        mainHorizontalLayout = QHBoxLayout()
        mainTopHorizontalLayout = QHBoxLayout()

        topFrame = QFrame(self)
        mainTopHorizontalLayout.addWidget(self.topWidget,17)
        mainTopHorizontalLayout.addWidget(self.topRightWidget,3)
        topFrame.setLayout(mainTopHorizontalLayout)

        midFrame = QFrame(self)
        mainHorizontalLayout.addWidget(self.leftWidget,7)
        mainHorizontalLayout.addWidget(self.rightWidget,3)
        midFrame.setLayout(mainHorizontalLayout)

        mainVerticalLayout.addWidget(topFrame)
        mainVerticalLayout.addWidget(midFrame,16)
        mainVerticalLayout.addWidget(self.bottomWidget,2)

        widget = QWidget()
        widget.setLayout(mainVerticalLayout)
        self.setCentralWidget(widget)

    # def adjustWidgets(self):
    #     self.bottomWidget.setLabelsStart()







