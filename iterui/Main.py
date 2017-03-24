# -*- coding: utf-8 -*-

from showresultdlg import ShowResultDlg
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    resultDlg = ShowResultDlg()
    resultDlg.show()
    sys.exit(app.exec_())