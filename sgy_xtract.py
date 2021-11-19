# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 15:16:31 2021

@author: mmach
"""

# import the necessary modules/libraries
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
from obspy.io.segy.core import _read_segy
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
        values = []
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
        index = []
        
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
    
#sgy = sgy_xtract()
#sgy.trace=2
#sgy.execute()