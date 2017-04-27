import sys

from PySide.QtCore import *

from PySide.QtGui import *
from PySide.QtGui import QApplication, QMainWindow

from Gui.Radiator import Radiator

def testWidget(testedWidget):
    testLayout = QHBoxLayout()
    testLayout.addWidget(testedWidget)

    mainWidget = QWidget()
    mainWidget.setLayout(testLayout)

    testMainWindow = QMainWindow()
    testMainWindow.setCentralWidget(mainWidget)
    testMainWindow.show()
    return testMainWindow

def main():
    app = QApplication(sys.argv)

    # mpk = MpkUpdate_GUI()
    r = Radiator()

    app.exec_()
    sys.exit()

if __name__ == '__main__':
    main()
