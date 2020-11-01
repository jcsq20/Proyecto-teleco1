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

#creacion vector (inicio, fin, paso)
lim = np.arange(-0.5,0.5,0.001)
#Devuelve números espaciados uniformemente durante un intervalo especificado.
#primer-numero,ultimon-numero,numero de muestras
l = np.linspace(0,np.pi,len(lim))
#funcion seno
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
                ssid = subprocess.getoutput("iwlist "+tarjetaRed+" scan |egrep 'ESSID|Frequency|Channel|Signal'")
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
                f = open ('RedesDetectadas.txt','w')
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

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Creamos la organización de la ventana
        self.layout = QGridLayout()
        # Gráfica de los datos scan
        self.lseñal = QLabel()
        self.lseñal.setText("Scan")
        self.layout.addWidget(self.lseñal, 0, 0, 1, 2)
        self.señal = MplCanvas(self, width=14, height=7)
        self.layout.setRowStretch(1,6)
        self.layout.addWidget(self.señal, 1, 0, 1, 2)

        #Creamos el boton scan
        self.bexit = QPushButton()
        self.bexit.setText('Scan')
        self.bexit.setFixedSize(70, 35)
        self.bexit.clicked.connect(self.buscar)
        self.layout.addWidget(self.bexit, 2, 0, 1, 1)

        #Creamos el boton salir
        self.brecord = QPushButton()
        self.brecord.setText('Salir')
        self.brecord.setFixedSize(70, 35)
        self.brecord.clicked.connect(self.salir)
        self.layout.addWidget(self.brecord, 2, 1, 1, 1)

        #texto
        tar = self.detectar()
        self.lvar = QLabel()
        self.lvar.setText("Nombre de la tarjeta Wifi: "+str(tar))
        self.layout.addWidget(self.lvar, 3, 0, 1, 2)

        #pintar
        self.widget = QWidget()
        self.setFixedSize(1270, 850)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setColumnMinimumWidth(0,1100)
        self.layout.setColumnMinimumWidth(1,100)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        

        self.show()

app = QApplication([])
w = MainWindow()
app.exec_()