from PyQt5.QtWidgets import *
import random
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())
        horizontal_layout = QVBoxLayout()
        horizontal_layout.addWidget(self.canvas)
        self.plot_visual_defn(horizontal_layout)

    def plot_visual_defn(self, horizontal_layout):
        self.canvas.ax1 = self.canvas.figure.add_subplot(451)
        self.canvas.ax1.set_facecolor("none")
        self.canvas.ax1.set_alpha(0.5)
        self.canvas.ax1.tick_params(axis='x', colors='white')
        self.canvas.ax1.tick_params(axis='y', colors='white')

        self.canvas.ax2 = self.canvas.figure.add_subplot(452)
        self.canvas.ax2.set_facecolor('none')
        self.canvas.ax2.grid(color='w', linestyle='-', linewidth=0.1)
        self.canvas.ax2.tick_params(axis='x', colors='white')
        self.canvas.ax2.tick_params(axis='y', colors='white')

        self.canvas.ax3 = self.canvas.figure.add_subplot(453)
        self.canvas.ax3.set_facecolor('none')
        self.canvas.ax3.grid(color='w', linestyle='-', linewidth=0.1)
        self.canvas.ax3.tick_params(axis='x', colors='white')
        self.canvas.ax3.tick_params(axis='y', colors='white')

        self.canvas.ax4 = self.canvas.figure.add_subplot(454)
        self.canvas.ax4.set_facecolor('none')
        self.canvas.ax4.grid(color='w', linestyle='-', linewidth=0.1)
        self.canvas.ax4.tick_params(axis='x', colors='white')
        self.canvas.ax4.tick_params(axis='y', colors='white')

        # self.canvas.ax6 = self.canvas.figure.add_subplot(456)
        # self.canvas.ax6.set_facecolor('none')
        # self.canvas.ax6.grid(color='w', linestyle='-', linewidth=0.1)
        # self.canvas.ax6.tick_params(axis='x', colors='white')
        # self.canvas.ax6.tick_params(axis='y', colors='white')

        self.canvas.ax5 = self.canvas.figure.add_subplot(455)
        self.canvas.ax5.set_facecolor('none')
        self.canvas.ax5.grid(color='w', linestyle='-', linewidth=0.1)
        self.canvas.ax5.tick_params(axis='x', colors='white')
        self.canvas.ax5.tick_params(axis='y', colors='white')

        self.canvas.ax7 = self.canvas.figure.add_subplot(4, 5, 10)
        self.canvas.ax7.set_facecolor((0.06, 0.06, 0.06))
        self.canvas.ax7.grid(color='w', linestyle='-', linewidth=0.1)
        self.canvas.ax7.tick_params(axis='x', colors='white')
        self.canvas.ax7.tick_params(axis='y', colors='white')

        self.canvas.ax_3d = self.canvas.figure.add_subplot(3, 5, 11, projection="3d")
        self.canvas.ax_3d.set_facecolor('none')
        self.canvas.ax_3d.tick_params(axis='x', colors='white')
        self.canvas.ax_3d.tick_params(axis='y', colors='white')
        self.canvas.ax_3d.tick_params(axis='z', colors='white')
        self.canvas.figure.set_facecolor('none')
        # plot colour should be orange blue and green
        self.setLayout(horizontal_layout)


