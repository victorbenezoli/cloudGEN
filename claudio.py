# encoding: utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal, pyqtSlot, Qt)
import sys
import os

sys.path.append('src/')
from claudio_createCloud import main as createCloud


class work(QObject):
    def __init__(self, infile, outfile, vname):
        super(work, self).__init__()

        self.infile = infile
        self.outfile = outfile
        self.vname = vname
        self.start.connect(self.run)

    start = pyqtSignal(str)

    @pyqtSlot()
    def run(self):
        createCloud(self.infile,self.outfile,self.vname)
#        print(self.err)


class window(QWidget):
    def __init__(self, parent = None):
        super(window, self).__init__(parent)

        self.path1 = None
        self.path2 = None

        self.set_window()
        self.create_window()
        self.set_layout()


    def set_window(self):

        self.resize(600,400)
        self.setWindowTitle("Claudio v2.0")


    def create_window(self):

#       -- Create buttons --
        self.button1 = QPushButton("Escolha a pasta", self)
        self.button2 = QPushButton("Escolha a pasta", self)
        self.button3 = QPushButton("Executar!", self)

#       -- Create labels --
        self.logbox = QPlainTextEdit()
        self.logbox.setReadOnly(True)
        self.logtitle = QLabel("LOG:")

#       -- Create links --
        self.button1.clicked.connect(self.choose_directory1)
        self.button2.clicked.connect(self.choose_directory2)
        self.button3.clicked.connect(self.run)

#       -- Create text option fields --
        self.optfield1 = QLineEdit("0.251")
        self.optfield2 = QLineEdit("0.509")
        self.optfield3 = QLineEdit("dswrf")
        self.optfield1.setAlignment(Qt.AlignRight)
        self.optfield2.setAlignment(Qt.AlignRight)
        self.optfield3.setAlignment(Qt.AlignRight)


    def set_layout(self):

        self.grid = QGridLayout()
        self.groupbox1 = QGroupBox("Selecione os dados de entrada:")
        self.groupbox1Layout = QFormLayout()
        self.groupbox1Layout.addRow("Selecione a pasta com os dados de radiação: ", self.button1)
        self.groupbox1Layout.addRow("Selecione a pasta de saída: ", self.button2)
        self.groupbox1.setLayout(self.groupbox1Layout)

        self.groupbox2 = QGroupBox("Opções:")
        self.groupbox2Layout = QFormLayout()
        self.groupbox2Layout.addRow("Digite o valor do coeficiente a do modelo de Angströn-Prescott:", self.optfield1)
        self.groupbox2Layout.addRow("Digite o valor do coeficiente b do modelo de Angströn-Prescott:", self.optfield2)
        self.groupbox2Layout.addRow("Digite o nome da variável de radiação de onda curta:", self.optfield3)
        self.groupbox2.setLayout(self.groupbox2Layout)

        self.layout_button3 = QHBoxLayout()
        self.layout_button3.addWidget(self.button3)

        self.layoutLog = QVBoxLayout()
        self.layoutLog.addWidget(self.logtitle)
        self.layoutLog.addWidget(self.logbox)

        self.layout_master = QVBoxLayout()
        self.layout_master.addWidget(self.groupbox1)
        self.layout_master.addWidget(self.groupbox2)
        self.layout_master.addLayout(self.layoutLog)
        self.layout_master.addLayout(self.layout_button3)
        self.setLayout(self.layout_master)


# -- Set choose_directitory buttons --
    def choose_directory1(self):
        self.path1 = QFileDialog.getExistingDirectory(self, "Selecionar pasta")
        self.path1 = self.path1+"/"
        self.button1.setText(self.path1)
        self.fnames = os.listdir(self.path1)
        nspc = len(self.fnames)
        for i in range(0, nspc):
            self.logbox.appendPlainText(self.fnames[i])

    def choose_directory2(self):
        self.path2 = QFileDialog.getExistingDirectory(self, "Selecionar pasta")
        self.path2 = self.path2+"/"
        self.button2.setText(self.path2)

    def run(self):
        try:
            coefa = float(self.optfield1.text())
            coefb = float(self.optfield2.text())
        except:
            self.messsage_box = QMessageBox.critical(self, "Erro!", "Os coeficientes a e b do modelo de Angströn-Prescott devem ser numéricos")
            return

        if (self.path1 is None or self.path2 is None):
            self.messsage_box = QMessageBox.critical(self, "Erro!", "As pastas de entrada e saída devem ser selecionadas antes do botão Executar ser acionado!")
            return

        self.vname = str(self.optfield3.text())
        self.logbox.clear()
        self.logbox.appendPlainText("Aguarde...")
        self.thread = QThread(self)
        self.thread.start()
        self.worker = work(self.path1, self.path2, self.vname)
        self.worker.moveToThread(self.thread)
        self.worker.start.emit("start")
        self.layoutLog.appendPlainText("Concluído!")


root = QApplication(sys.argv)
app = window()
app.show()

sys.exit(root.exec_())
