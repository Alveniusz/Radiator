import sys

from PySide.QtGui import QApplication
from Gui.Radiator import Radiator
from Gui.MpkListener import MpkListener
from Libs.mpkUpdate import MpkUpdate_GUI

def main():
    app = QApplication(sys.argv)

    mpk = MpkUpdate_GUI()

    # widget = MpkListener()
    # widget.setGeometry(700,50,600,900)
    # widget.show()

    r = Radiator()

    app.exec_()
    sys.exit()

if __name__ == '__main__':
    main()