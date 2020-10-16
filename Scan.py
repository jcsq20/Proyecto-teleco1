import subprocess
import matplotlib
import sys
matplotlib.use('Qt5Agg')
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as fc
from matplotlib.figure import Figure 

canal=[]
frecuencia =[]
señal=[]
essid=[]
lim = np.arange(-0.5,0.5,0.001)
l = np.linspace(0,np.pi,len(lim))
si = np.sin(l)

class MplCanvas(fc):
    def __init__(self, parent=None, width=8, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    #Metodo de salir entorno grafico
    def salir(self):
        sys.exit()