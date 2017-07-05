# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from InputDlg import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    resultDlg = InputDlg()
    resultDlg.show()
    sys.exit(app.exec_())