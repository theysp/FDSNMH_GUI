from PyQt5 import uic

def CompileUI(uiname,pyname):
    uifile = open(uiname, 'r')
    pyfile = open(pyname, 'w')
    uic.compileUi(uifile, pyfile)
    pyfile.close()
    uifile.close()

if __name__ == '__main__':
    import sys
    CompileUI(sys.argv[1],sys.argv[2])
   # CompileUI('ShowResultDlg.ui','Ui_ShowResultDlg.py')
  #  CompileUI('WidgetParam.ui', 'Ui_WidgetParam.py')
   # CompileUI('WidgetPrimaryNuclides.ui', 'Ui_WidgetPrimaryNuclides.py')
   # CompileUI('WidgetTransGraph.ui', 'Ui_WidgetTransGraph.py')
