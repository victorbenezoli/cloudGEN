# encoding: utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal, pyqtSlot)
import sys
import os

sys.path.append('src/')
from claudio_createCloud import main as createCloud


class work(QObject):
    def __init__(self, infile, outfile):
        super(work, self).__init__()

        self.infile = infile
        self.outfile = outfile
        self.start.connect(self.run)

    start = pyqtSignal(str)

    @pyqtSlot()
    def run(self):
        createCloud(self.infile,self.outfile)


class window(QWidget):
    def __init__(self, parent = None):
        super(window, self).__init__(parent)
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

    def set_layout(self):

        self.grid = QGridLayout()
        self.groupbox = QGroupBox("Selecione os dados de entrada:")
        self.groupboxLayout = QFormLayout()
        self.groupboxLayout.addRow("Selecione a pasta com os dados de radiação: ", self.button1)
        self.groupboxLayout.addRow("Selecione a pasta de saída: ", self.button2)
        self.groupbox.setLayout(self.groupboxLayout)

        self.layout_button3 = QHBoxLayout()
        self.layout_button3.addWidget(self.button3)

        self.layoutLog = QVBoxLayout()
        self.layoutLog.addWidget(self.logtitle)
        self.layoutLog.addWidget(self.logbox)

        self.layout_master = QVBoxLayout()
        self.layout_master.addWidget(self.groupbox)
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
        self.path2 = '/'+QFileDialog.getExistingDirectory(self, "Selecionar pasta")
        self.path2 = self.path2+"/"
        self.button2.setText(self.path2)

    def run(self):
        self.logbox.clear()
        self.logbox.appendPlainText("Aguarde...")
        self.thread = QThread(self)
        self.thread.start()
        self.worker = work(self.path1, self.path2)
        self.worker.moveToThread(self.thread)
        self.worker.start.emit("start")
        self.layoutLog.appendPlainText("Concluído!")


root = QApplication(sys.argv)
app = window()
app.show()

sys.exit(root.exec_())
