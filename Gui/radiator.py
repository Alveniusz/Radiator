from PySide.QtGui import *

class Radiator(QMainWindow):
    def __init__(self):
        super(Radiator, self).__init__()

        self.setMainWindowsParameters()

        self.initWidgets()
        self.setWidgetsLayout()
        self.showMaximized()

    def setMainWindowsParameters(self):
        palette	= QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("Pictures/Background.jpg")))
        self.setPalette(palette)


        self.setGeometry(300, 300, 300, 150)

    def initWidgets(self):
        # Replace frames with correct widgets when ready
        self.topWidget = QFrame()
        self.topWidget.setFrameStyle(QFrame.Box)

        self.bottomWidget = QFrame()
        self.bottomWidget.setFrameStyle(QFrame.Box)

        self.leftWidget = QFrame()
        self.leftWidget.setFrameStyle(QFrame.Box)

        self.rightWidget = QFrame()
        self.rightWidget.setFrameStyle(QFrame.Box)

    def setWidgetsLayout(self):
        mainVerticalLayout = QVBoxLayout()
        mainHorizontalLayout = QHBoxLayout()

        midFrame = QFrame(self)
        mainHorizontalLayout.addWidget(self.leftWidget,7)
        mainHorizontalLayout.addWidget(self.rightWidget,3)
        midFrame.setLayout(mainHorizontalLayout)

        mainVerticalLayout.addWidget(self.topWidget,2)
        mainVerticalLayout.addWidget(midFrame,17)
        mainVerticalLayout.addWidget(self.bottomWidget,1)

        widget = QWidget()
        widget.setLayout(mainVerticalLayout)
        self.setCentralWidget(widget)






    # def initTimer(self):
    #     timer = QTimer(self)
    #     self.connect(timer, SIGNAL('timeout()'), self.updateTime)
    #     timer.start(1000)
    #
    # def updateTime(self):
    #     qtime = QTime.currentTime()

