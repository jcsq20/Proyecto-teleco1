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
    
    #Metodo que identifa la tarjeta de red de mi pc
    def detectar(self):
        var=subprocess.getoutput('iwconfig')
        interfaz=var.splitlines()
        tarjetaRed=""
        for i in range(len(interfaz)):
                if interfaz[i].find("w", 0, 1)==0:
                        y=interfaz[i].split()
                        tarjetaRed=y[0]
        return tarjetaRed

    #Metodo de Escaner de las redes wifi
    def buscar(self, event):
        tarjetaRed = self.detectar()
        bandera =True
        canal.clear()
        señal.clear()
        while bandera:
            print(bandera)
            if not (canal):
                ssid = subprocess.getoutput("sudo iwlist "+tarjetaRed+" scan |egrep 'ESSID|Frequency|Channel|Signal'")
                row=ssid.splitlines()
                aux=[]
                auxFreq=[]
                for j in range(len(row)):
                        if j*4+3<len(row):
                                aux=row[j*4].split(":")
                                canal.append(int(aux[1]))

                                aux=row[j*4+1].split()
                                auxFreq=aux[0].split(":")
                                frecuencia.append(auxFreq[1])

                                aux=row[j*4+2].split("level=")
                                auxFreq=aux[1].split()
                                señal.append(int(auxFreq[0]))

                                aux=row[j*4+3].split(":")
                                essid.append(aux[1])
                f = open ('escanWifi.txt','w')
                for c in range(len(canal)):
                        f.write("ESSID: "+str(essid[c])+', Frecuencia: '+str(frecuencia[c])+', Signal frecuecy: '+str(señal[c])+' dbm, Canal: '+str(canal[c])+'\n')
                f.close()
            else:
                bandera = False
        print("Fin de deteccion")

        self.señal.axes.cla()
        self.graficar()
        self.señal.draw_idle()

    def graficar(self):
            #print(canal)
        for i, x in enumerate(canal):
            #print(i)
            limplot = lim+x
            sinplot = ((señal[i]+100)*si)-100
            self.señal.axes.plot(limplot, sinplot)
            #self.señal.axes.legend(str(señal[i]))
            self.señal.axes.legend(essid, loc="upper right",fancybox=True, framealpha=0.5)
        print("Fin pintada")