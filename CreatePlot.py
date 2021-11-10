# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 14:41:53 2021

@author: mattb
"""

import ReadFiles_D1
import os
import matplotlib.pyplot as plt
import seaborn as sns




def getData(filepath):
    patientInfo = ReadFiles_D1.getPatientInfo(filepath)
    analyzeInfo = ReadFiles_D1.getAnalyzeInfo(filepath)
    measureInfo = ReadFiles_D1.getMeasureInfo(filepath)
    stimTimes = ReadFiles_D1.getStimTimes(filepath)
    expData = ReadFiles_D1.getExpData(filepath)
        
    return patientInfo, analyzeInfo, measureInfo, stimTimes, expData



def getFilePaths():
    
    directory = 'Dataset1_VM/VMData/'
    filepaths = []

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            filepaths.append(f)
    return filepaths



#patientInfo, analyzeInfo, measureInfo, stimTimes, expData = getData('Dataset1_VM/VMData/VM0003_ViMo_HBA_Probe1_Total.csv')




def generatePlots(filepaths):
    
    for i in range(len(filepaths)):
        patientInfo, analyzeInfo, measureInfo, stimTimes, expData = getData(filepaths[i])
        
        samples = expData.iloc[:, 1:25]

        avg = samples.mean()

        plot_filename = filepaths[i].split('/')[-1]
        plot_filename = plot_filename.split('.csv')[0]
        
        directory = 'Dataset1_plots/'
        
        plot_bar = directory + plot_filename + "_bar"
        plot_line = directory + plot_filename + "_line"
        plot_heat = directory + plot_filename + "_heat"

        plt.bar(avg.index.values, avg)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        
        plt.savefig(plot_bar)
        plt.show()

        plt.plot( avg, linewidth=5)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        
        plt.savefig(plot_line)
        plt.show()


        heat = sns.heatmap(samples, cmap="YlOrBr")
        plt.gca().invert_yaxis()
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        
        plt.savefig(plot_heat)
        plt.show()
        
        meta = directory + plot_filename + "_metadata.txt"
        
        with open(meta, 'w') as f:
            f.write(patientInfo + "\n\n\n" +analyzeInfo+ "\n\n\n" + measureInfo + "\n\n\nStimTimes:\n"+ stimTimes)
        
        
        
    
        
        
filepaths = getFilePaths()
generatePlots(filepaths)







