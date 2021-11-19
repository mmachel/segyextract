# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 15:16:31 2021

@author: mmach
"""

# import the necessary modules/libraries
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
#from obspy.io.segy.core import _read_segy
from obspy import read
import pandas as pd
import numpy as np

#define the main class to extract the trace from seg-y file
class sgy_xtract():  
    def __init__(self, file, trace):
        self.filename = file
        self.trace = trace-1
    # read the file in segy
    
    def execute(self):
        '''
        The code reads seg-y file and extract the trace
        '''
        #st = _read_segy(self.filename)
        st = read(self.filename)
    
        # extract the trace of interest
        tr1 = st[self.trace].data
        
        # define empty lists
        idx = []
        pvalues = abs(tr1) # absolute values
        
        # fill the lists with trace values and index
        # fill index
        for i in range(0,len(tr1)):
            idx.append(i)
    
        self.values = tr1
        values2 = -1*tr1
        # sort trace values in ascending and descending order
        #trasort = sorted(values)
        #trdsort = sorted(values, reverse=True)
        
        #peaks, _ = find_peaks(values, height=0)
        self.maxpeaks, _ = find_peaks(self.values, prominence=1)
        self.minpeaks, _ = find_peaks(values2, prominence=1)
        self.maxvalues = self.values[self.maxpeaks]
        self.minvalues = self.values[self.minpeaks]
        # Only for developer test
        #plt.figure(figsize=(20,5))
        #plt.plot(self.values)
        #plt.plot(self.minpeaks, self.minvalues, 'o')
        #plt.plot(self.maxpeaks, self.maxvalues, "x")
        #plt.show()

        # join arrays of peaks and values and create dataframe
        self.index = np.concatenate((self.minpeaks,self.maxpeaks))
        self.maxmin = np.concatenate((self.minvalues,self.maxvalues))
        self.dictvalue = {'idx': self.index, 'value': self.maxmin}
        self.data = {'traceid':idx, 'tracevalues':self.values, '+tracevalues':pvalues}
        # Only for developer test
        #plt.figure(figsize=(20,5))
        #plt.plot(self.values)
        #plt.plot(self.index, self.maxmin, 'x')
        #plt.show()
        # create data frames of the extracted values
        #self.df = pd.DataFrame(data)
        #self.df2 = pd.DataFrame(dictvalue)
        
    def savetrace(self):
        self.execute()
        # create data frames of the extracted values
        df = pd.DataFrame(self.data)
        df2 = pd.DataFrame(self.dictvalue)
        
        idx = self.filename.index('.')
        tempfile = self.filename[:idx]
        outputfile = tempfile+'_trace'+str(self.trace+1)+'.xlsx'
        outputfile2 = tempfile+'_maxtrace'+str(self.trace+1)+'.xlsx'
        # export the data as excel files for further analysis
        df.to_excel(outputfile, index=False)
        df2.to_excel(outputfile2, index=False)
        
# importing the necessary modules for the GUI
import sys
import PyQt5.QtCore as QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Extract SEG-Y Trace DATA')
        self.setStyleSheet("background-color: silver")
        app_icon = QtGui.QIcon()
        app_icon.addFile('icon0.ico')
        app_icon.addFile('icon1.ico')
        app_icon.addFile('icon2.ico')
        app_icon.addFile('icon3.ico')
        app_icon.addFile('xticon.png')
        self.setWindowIcon(app_icon)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        #self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setGeometry(100,100,400,140)
        self.path = None
        
    def start(self):
        #Start the execution of the program
        self.readButton = QPushButton('Read')
        self.plotButton = QPushButton('Plot')
        self.saveButton = QPushButton('Save')
        self.closeButton = QPushButton('Close')
        self.enterTraceButton = QLabel('Trace')
        self.enterTraceEdit = QLineEdit(self)
        self.enterTraceEdit.setText('1')
        
        # Layout
        self.btn = QVBoxLayout()
        self.btn.addStretch(1)
        self.btn.addWidget(self.readButton)
        self.btn.addWidget(self.enterTraceButton)
        self.btn.addWidget(self.enterTraceEdit)
        self.btn.addWidget(self.plotButton)
        self.btn.addWidget(self.saveButton)
        self.btn.addWidget(self.closeButton)
        
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.btn)        
        self.setLayout(self.layout)
        
        self.closeButton.setFocus()
        self.readButton.clicked.connect(self.readfile)
        self.plotButton.clicked.connect(self.plottrace)
        self.saveButton.clicked.connect(self.savefile)
        self.closeButton.clicked.connect(self.close_program)
    
    # read seg-y file 
    def readfile(self):
        self.path = QFileDialog.getOpenFileName()[0]
    
    # save the trace and its amplitude in an excel table
    def savefile(self):
        segy = sgy_xtract(file=self.path, trace=int(self.enterTraceEdit.text()))

        segy.savetrace()
    
    # plot the trace to be sure that you save the right extrema
    def plottrace(self):
        self.segy = sgy_xtract(file=self.path, trace=int(self.enterTraceEdit.text()))
        self.segy.execute()
        plt.figure(figsize=(20,5))
        plt.plot(self.segy.values)
        plt.plot(self.segy.minpeaks, self.segy.minvalues, 'o')
        plt.plot(self.segy.maxpeaks, self.segy.maxvalues, "x")
        plt.show()     
    def close_program(self):
        QApplication.quit()
        
if __name__ == '__main__':
    def run():
        app = QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon('xticon.png'))
        window = Window()
        window.show()
        window.start()
        app.exec()
    run()