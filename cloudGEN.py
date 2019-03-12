# encoding: utf-8

from PyQt5.QtWidgets import (QWidget, QPushButton, QPlainTextEdit, QLabel,
                            QLineEdit, QGridLayout, QGroupBox, QFormLayout,
                            QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox,
                            QApplication)

from PyQt5.QtCore import (QCoreApplication, QObject, QThread, pyqtSignal, pyqtSlot, Qt)
                          
from PyQt5.QtGui import QIcon
import sys
import os
import numpy as np

sys.path.append('src/')
sys.path.append('icon/')
from cloudGEN_createCloud import main as createCloud
from cloudGEN_getinfo import main as getinfo

class work(QThread):

    done = pyqtSignal(int)
    erro = pyqtSignal(int)

    def __init__(self, infile, outfile, outpattern, invname, outvname, coefa, coefb):
        super(work, self).__init__()

        self.infile = infile
        self.outfile = outfile
        self.outpattern = outpattern
        self.invname = invname
        self.outvname = outvname
        self.coefa = coefa
        self.coefb = coefb

    def run(self):
        try:
            self.err = createCloud(self.infile,self.outfile,self.outpattern,self.invname,self.outvname,self.coefa, self.coefb)
            if (self.err == 1000):
                self.erro.emit(1000)
            elif (self.err == 2000):
                self.erro.emit(2000)
            elif (self.err == 0):
                self.done.emit(0)
                print("Concluído!", "A operação foi concluída com sucesso!")

        except:
            self.erro.emit(9999)
            return()


class window(QWidget):
    def __init__(self, parent = None):
        super(window, self).__init__(parent)

        self.path1 = None
        self.path2 = None

        self.set_window()
        self.create_window()
        self.set_layout()


    def set_window(self):

        self.resize(600,500)
        self.setWindowTitle("cloudGEN v1.0")
        self.setWindowIcon(QIcon(".icon/icon.ico"))


    def create_window(self):

#       -- Create buttons --
        self.button1 = QPushButton("Choose the folder", self)
        self.button2 = QPushButton("Choose the folder", self)
        self.button3 = QPushButton("Run!", self)

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
        self.optfield4 = QLineEdit("cld")
        self.optfield5 = QLineEdit("cld.daily.")
        self.optfield1.setAlignment(Qt.AlignRight)
        self.optfield2.setAlignment(Qt.AlignRight)
        self.optfield3.setAlignment(Qt.AlignRight)
        self.optfield4.setAlignment(Qt.AlignRight)
        self.optfield5.setAlignment(Qt.AlignRight)


    def set_layout(self):

        self.grid = QGridLayout()
        self.groupbox1 = QGroupBox("Select the data input:")
        self.groupbox1Layout = QFormLayout()
        self.groupbox1Layout.addRow("Select the downward shortwave radiation folder: ", self.button1)
        self.groupbox1Layout.addRow("Select the output folder: ", self.button2)
        self.groupbox1.setLayout(self.groupbox1Layout)

        self.groupbox2 = QGroupBox("Options:")
        self.groupbox2Layout = QFormLayout()
        self.groupbox2Layout.addRow("Type the a coefficient of Angströn-Prescott model:", self.optfield1)
        self.groupbox2Layout.addRow("Type the b coefficient of Angströn-Prescott model:", self.optfield2)
        self.groupbox2Layout.addRow("Type the variable name of downward shortwave radiation files:", self.optfield3)
        self.groupbox2Layout.addRow("Type the variable name of cloud cover files:", self.optfield4)
        self.groupbox2Layout.addRow("Type the pattern of output files:", self.optfield5)
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
        self.path1 = QFileDialog.getExistingDirectory(self, "Select folder...")
        if self.path1 == "":
            self.path1 == None
            self.button1.setText("Choose the folder")
            return
        self.path1 = self.path1+"/"
        self.button1.setText(self.path1)
        self.fnames = os.listdir(self.path1)
        self.nspc = len(self.fnames)
        try:
            self.table = getinfo(self.path1+self.fnames[0])
            self.logbox.clear()
            self.logbox.appendPlainText("Number of input files: "+str(self.nspc))
            self.logbox.appendPlainText("Latitude: "+str(round(self.table[1],2))+"° - "+str(round(self.table[2],2))+"°")
            self.logbox.appendPlainText("Longitude: "+str(round(self.table[3],2))+"° - "+str(round(self.table[4],2))+"°")
            self.logbox.appendPlainText("Resolution: "+str(round(self.table[5],2))+"° x "+str(round(self.table[6],2))+"°")
        except:
            self.logbox.clear()
            self.logbox.appendPlainText("Error: There are no valid files in the selected folder.")
            return

    def choose_directory2(self):
        self.path2 = QFileDialog.getExistingDirectory(self, "Select folder...")
        if self.path2 == "":
            self.path2 == None
            self.button2.setText("Choose the folder")
            return
        self.path2 = self.path2+"/"
        self.button2.setText(self.path2)


    def run(self):

        self.logbox.clear()

        try:
            self.coefa = float(self.optfield1.text())
            self.coefb = float(self.optfield2.text())
        except:
            self.messsage_box = QMessageBox.critical(self, "Error!", "The coefficients of Angströn-Prescott model must be numeric.")
            return

        if (self.path1 is None or self.path2 is None):
            self.messsage_box = QMessageBox.critical(self, "Error!", "The input and output folders must be selected before running the program.")
            return

        if self.optfield3.text() != "":
            self.invname = str(self.optfield3.text())
        else:
            self.logbox.appendPlainText("Erro: The variable name of the input file must be filled before running the program.")
            return

        if self.optfield4.text() != "":
            self.outvname = str(self.optfield4.text())
        else:
            self.logbox.appendPlainText("Erro: The variable name of the output file must be filled before running the program.")
            return

        if self.optfield5.text() != "":
            self.outpattern = str(self.optfield5.text())
        else:
            self.logbox.appendPlainText("Erro: The pattern of the output files must be filled before running the program.")
            return

        self.logbox.clear()
        self.logbox.appendPlainText("Wait...")
        self.worker = work(self.path1, self.path2, self.outpattern, self.invname, self.outvname, self.coefa, self.coefb)
        self.worker.done.connect(self.done)
        self.worker.erro.connect(self.erro)
        self.worker.start()

    def done(self):
        self.logbox.clear()
        self.logbox.appendPlainText("Concluded!")
        QMessageBox.information(self, "Concluded!", "The execution was completed successfully!")
        return

    @pyqtSlot(int)
    def erro(self, code):
        if(code == 1000):
            self.logbox.clear()
            self.logbox.appendPlainText("Error! There are no files in selected folder.")
        elif(code == 2000):
            self.logbox.clear()
            self.logbox.appendPlainText("Error! Variable "+self.invname+" could not be found.")
        elif(code == 9999):
            self.logbox.clear()
            self.logbox.appendPlainText("Error! Unable to run the program with selected input files.")


root = QApplication(sys.argv)
app = window()
app.show()

sys.exit(root.exec_())
