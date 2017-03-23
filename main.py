import sys

from PySide.QtGui import QApplication

from Libs.mpkUpdate import MpkUpdate_GUI


def main():
    app = QApplication(sys.argv)

    mpk = MpkUpdate_GUI()

    # r = Radiator()

    app.exec_()
    sys.exit()

if __name__ == '__main__':
    main()