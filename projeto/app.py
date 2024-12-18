import os
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import serial
import time
import csv


def inicia_coleta():
    conexaoSerial.write(b"i")
    print("Coleta Iniciada!")


def para_coleta():
    conexaoSerial.write(b"p")
    print("Coleta Encerrada!")


def liga_alarme():
    conexaoSerial.write(b"l")
    atualiza_status("Alarme Ativado")
    print("Alerta ativado!")


def desliga_alarme():
    conexaoSerial.write(b"d")
    atualiza_status()
    print("Alerta desligado!")


def saindo():
    desliga_alarme()
    para_coleta()
    print("Encerrando Sistema")


def salvar_dados(dados: np.array, nome_arquivo: str = "dado.csv"):
    file_path = f"{os.getcwd()}/data/{nome_arquivo}"

    # Certifica-se de que o diretório "data" existe
    os.makedirs("data", exist_ok=True)

    # Verifica se o arquivo já existe
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="") as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            escritor.writerow(["valor"])  # Cabeçalho com tempo e valor

    # Adiciona os novos dados ao arquivo existente
    with open(file_path, mode="a", newline="") as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerows(zip(dados))  # Escreve tempo e valor


def atualiza_status(
    status: str = "Desativado", arquivo: str = "data/status_alarme.txt"
):
    # Cria o diretório caso não exista
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)

    # Abre o arquivo para escrita (substitui o conteúdo se já existir)
    with open(arquivo, "w") as file:
        file.write(status)  # Escreve o status no arquivo
        print(f"Status do alarme atualizado para: {status}")


def detecta_apneia(batch_dados: np.array):
    if batch_dados.sum() < 100:
        print(f"PACIENTE EM APNEIA! valor={batch_dados.sum()}")
        liga_alarme()


win = pg.GraphicsWindow()
win.setWindowTitle("Monitor de Apneia")

freqAquisicao = 100  # Hz
tempoBatch = 10  # s
npontos = freqAquisicao * tempoBatch
x_atual = 0
p1 = win.addPlot()
p1.setYRange(0, 5, padding=0)
data1 = np.zeros(npontos)
eventos = np.zeros(npontos)
curve1 = p1.plot(data1)
maxV = 5.0

limRuido = 100.0 * maxV / 1023.0

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
botao3.clicked.connect(desliga_alarme)

p2 = win.addLayout(row=1, col=0)
p2.addItem(proxy1, row=0, col=0)
p2.addItem(proxy2, row=1, col=0)
p2.addItem(proxy3, row=2, col=0)

conexaoSerial = serial.Serial("/dev/ttyACM0", 115200)
inicia_coleta()

def update():
    global data1, eventos, curve1, conexaoSerial, x_atual, npontos, previousTime

    if conexaoSerial.inWaiting() > 1:
        dado1 = conexaoSerial.read()
        dado2 = conexaoSerial.read()
        novodado = float((ord(dado1) + ord(dado2) * 256.0) * maxV / 1023.0)

        # Atualiza o gráfico
        data1[x_atual] = novodado
        data1[(x_atual + 1) % npontos] = np.nan
        if novodado >= limRuido: 
            eventos[x_atual] = 1
            eventos[(x_atual + 1) % npontos] = np.nan
        x_atual = x_atual + 1
        if x_atual == npontos-1:
            detecta_apneia()
            x_atual = 0
        salvar_dados(eventos, "eventos.csv")
        salvar_dados(dado1, "dado.csv")

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
