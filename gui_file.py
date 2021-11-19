# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 15:46:10 2021

@author: mmach
"""

# importing the necessary modules
import sys
import PyQt5.QtCore as QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
import sgy_xtract

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Extract SEG-Y Trace DATA')
        self.setStyleSheet("background-color: silver")
        app_icon = QtGui.QIcon()
        app_icon.addFile('supporting_files/icon0.ico')
        app_icon.addFile('supporting_files/icon1.ico')
        app_icon.addFile('supporting_files/icon2.ico')
        app_icon.addFile('supporting_files/icon3.ico')
        app_icon.addFile('supporting_files/xticon.png')
        self.setWindowIcon(app_icon)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        #self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setGeometry(100,100,400,140)
        self.path = None
        
    def start(self):
        #Start the execution of the program
        self.readButton = QPushButton('Read')
        self.saveButton = QPushButton('Save')
        self.closeButton = QPushButton('Close')
        self.enterTraceButton = QLabel('Trace')
        self.enterTraceEdit = QLineEdit(self)
        self.enterTraceEdit.setText('0')
        
        # Layout
        self.btn = QVBoxLayout()
        self.btn.addStretch(1)
        self.btn.addWidget(self.readButton)
        self.btn.addWidget(self.enterTraceButton)
        self.btn.addWidget(self.enterTraceEdit)
        self.btn.addWidget(self.saveButton)
        self.btn.addWidget(self.closeButton)
        
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.btn)        
        self.setLayout(self.layout)
        
        self.closeButton.setFocus()
        self.readButton.clicked.connect(self.readfile)
        self.saveButton.clicked.connect(self.savefile)
        self.closeButton.clicked.connect(self.close_program)
        
        #self.exec()
    def readfile(self):
        self.path = QFileDialog.getOpenFileName()[0]
        
    def savefile(self):
        segy = sgy_xtract.sgy_xtract(file=self.path, trace=int(self.enterTraceEdit.text()))
        #segy.trace = int(self.enterTraceEdit.text())
        #segy.filename = self.path
        if self.path == None:
            self.mfile()
        segy.execute()
    def mfile(self):
        msg = QMessageBox()
        msg.setWindowTitle("Load File")
        msg.setText("Please load SEG-Y File!")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Retry|QMessageBox.Ignore)
        msg.setDefaultButton(QMessageBox.Retry)
        msg.setInformativeText("Only valid file!")
        msg.setDetailedText("SEG-Y File and specify the trace")
        
    def close_program(self):
        QApplication.quit()
        
if __name__ == '__main__':
    def run():
        app = QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon('supporting_files/xticon.png'))
        window = Window()
        window.show()
        window.start()
        app.exec()
    run()