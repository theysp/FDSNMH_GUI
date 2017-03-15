
from PyQt5.QtCore import pyqtSlot,pyqtSignal
from PyQt5.QtWidgets import QDialog,QApplication, QHBoxLayout
from ui_plotdialog import Ui_PlotDialog

import matplotlib
matplotlib.use("Qt5Agg")
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotDialog(QDialog, Ui_PlotDialog):
    def __init__(self, parent=None):
        super(PlotDialog, self).__init__(parent)
        self.setupUi(self)
        self._createFigures()
        self._createLayouts()

    def _createFigures(self):
        self._fig = Figure(figsize=(8,6), dpi=100, tight_layout=True)
        self._fig.set_facecolor('#F5F5F5')
        self._fig.subplots_adjust(left=0.08,top=0.92,bottom=0.1)
        self._canvas = FigureCanvas(self._fig)
        self._ax = self._fig.add_subplot(111)
        self._ax.hold(True)
        self._initializeFigure()

    def _createLayouts(self):
        layout = QHBoxLayout(self.frame)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self._canvas)

    def _initializeFigure(self):
        Font = {'family':'Tahoma',
                'weight': 'bold','size': 10}
        # Abscissa
        self._ax.set_xlim([380, 780])
        self._ax.set_xticks([380, 460, 540, 620, 700, 780])
        self._ax.set_xticklabels([380, 460, 540, 620, 700, 780], fontdict=Font)
        self._ax.set_xlabel("Wavelength (nm)", fontdict=Font)
        # Ordinate
        self._ax.set_ylim([0.0, 1.0])
        self._ax.set_yticks(np.arange(0.0, 1.1, 0.2))
        self._ax.set_yticklabels(np.arange(0.0, 1.1, 0.2), fontdict=Font)
        self._ax.set_ylabel("Spectral Radiance (W/(m$^2$*sr*nm))", fontdict=Font)
        self._ax.grid(True)  # Grid On

    def _updateFigures(self):
        Font = {'family': 'Tahoma',
                'weight': 'bold',
                'size': 10}
        self._ax.clear()
        maxY = 0.0
        x = np.arange(380, 781)
        y = np.random.rand(401)
        self._ax.plot(x, y, 'r', label="Data")
        maxY = max(y)
        if maxY <= 0:
            self._initializeFigure()
        else:
            self._fig.subplots_adjust(left=0.11, top=0.92, right=0.95, bottom=0.1)
            # Abscissa
            self._ax.set_xlim([380, 780])
            self._ax.set_xticks([380, 460, 540, 620, 700, 780])
            self._ax.set_xticklabels([380, 460, 540, 620, 700, 780], fontdict=Font)
            self._ax.set_xlabel("Wavelength (nm)", fontdict=Font)
            # Ordinate
            self._ax.set_ylim([0.0, maxY])
            self._ax.set_yticks([0.0, maxY / 4.0, maxY / 2.0, maxY * 3 / 4.0, maxY])
            self._ax.set_yticklabels(
                ["%.1e" % 0.0, "%.1e" % (maxY / 4.0), "%.1e" % (maxY / 2.0), "%.1e" % (maxY * 3.0 / 4.0),
                 "%.1e" % maxY], fontdict=Font)
            self._ax.set_ylabel("Spectral Radiance (W/(m$^2$*sr*nm))", fontdict=Font)

        self._ax.grid(True)
        self._ax.legend(loc="best", fontsize="small").draggable(state=True)  # Legend
        self._canvas.draw()

    @pyqtSlot()
    def on_buttonPlot_clicked(self):
        self._updateFigures()


if __name__ == '__main__':
    import sys
    a = QApplication(sys.argv)
    b = PlotDialog()
    b.show()
    sys.exit(a.exec_())

