import sys

from PySide.QtGui import QApplication
from Gui.Radiator import Radiator
from Gui.MpkListener import MpkListener
from Gui.QuoteWidget import QuoteWidget
from Libs.mpkUpdate import MpkUpdate_GUI

def main():
    app = QApplication(sys.argv)

    # mpk = MpkUpdate_GUI()

    # widget = QuoteWidget()
    # widget.setGeometry(50,50,1200,100)
    # widget.show()

    r = Radiator()

    app.exec_()
    sys.exit()

if __name__ == '__main__':
    main()