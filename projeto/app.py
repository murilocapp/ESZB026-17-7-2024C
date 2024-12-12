import sys
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import serial
import time


def inicia_coleta():
    conexaoSerial.write(b"i")
    print("Coleta Iniciada!")


def para_coleta():
    conexaoSerial.write(b"p")
    print("Coleta Encerrada!")


def liga_led():
    conexaoSerial.write(b"l")
    print("Alerta visual ativado!")


def desliga_led():
    conexaoSerial.write(b"d")
    print("Alerta visual desligado!")


def saindo():
    desliga_led()
    para_coleta()
    print("Encerrando Sistema")


win = pg.GraphicsWindow()
win.setWindowTitle("Monitor de Apneia")

npontos = 800
x_atual = 0
p1 = win.addPlot()
p1.setYRange(0, 5, padding=0)
data1 = np.zeros(200)
curve1 = p1.plot(data1)
ptr1 = 0
maxV = 5.0

previousTime = time.time() * 1000  # pega a hora atual, em milissegundos
texto = pg.TextItem(text="", color=(255, 255, 0), anchor=(0, 1))
p1.addItem(texto)
texto.setPos(0, 0)  # adiciona o texto na posição (0, 0) do gráfico

proxy1 = QtGui.QGraphicsProxyWidget()
botao1 = QtGui.QPushButton("Inicia")
proxy1.setWidget(botao1)
botao1.clicked.connect(inicia_coleta)

proxy2 = QtGui.QGraphicsProxyWidget()
botao2 = QtGui.QPushButton("Para")
proxy2.setWidget(botao2)
botao2.clicked.connect(para_coleta)

proxy3 = QtGui.QGraphicsProxyWidget()
botao3 = QtGui.QPushButton("Desativar Alarme")
proxy3.setWidget(botao3)
botao3.clicked.connect(desliga_led)

p2 = win.addLayout(row=1, col=0)
p2.addItem(proxy1, row=0, col=0)
p2.addItem(proxy2, row=1, col=0)
p2.addItem(proxy3, row=2, col=0)

conexaoSerial = serial.Serial("/dev/ttyACM0", 115200)
inicia_coleta()


def update():
    global data1, curve1, ptr1, conexaoSerial, x_atual, npontos, previousTime
    if conexaoSerial.inWaiting() > 1:
        dado1 = conexaoSerial.read()
        dado2 = conexaoSerial.read()
        novodado = float((ord(dado1) + ord(dado2) * 256.0) * maxV / 1023.0)

        data1[x_atual] = novodado
        data1[(x_atual + 1) % npontos] = np.nan
        x_atual = x_atual + 1
        if x_atual >= npontos:
            x_atual = 0

        curve1.setData(data1, connect="finite")
        actualTime = time.time() * 1000
        taxa = str(round(actualTime - previousTime))
        previousTime = actualTime
        texto.setText("taxa: " + taxa.zfill(3) + "ms")


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == "__main__":
    QtGui.QApplication.instance().exec_()
