from PyQt5 import uic
if __name__ == '__MAIN__'
    uifile = open('plotdialog.ui','r')
    pyfile = open('ui_plotdialog.py','w')
    uic.compileUi(uifile,pyfile)