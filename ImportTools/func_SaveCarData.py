# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 16:56:35 2023

@author: jamie
"""

def func_SaveCarData(strCarDataCSV, strSavePath):
        
    # Import function to load car data
    import pandas as pd
    from func_ExtractCarData import func_ExtractCarData
    import os

    lDriverData = func_ExtractCarData(strCarDataCSV);
    os.mkdir(strSavePath)

    # Loop through each driver that has data and save to CSV
    iDriver = 0
    while iDriver < len(lDriverData):
        try:
            dfCurrDriverData = lDriverData[iDriver] # Extract data for current driver only
            strFolderName = "\DriverData_" + str(iDriver) # Define name of RAW data file
            strCSVName = "\DriverData_" + str(iDriver) + "_RAW.csv" # Define name of RAW data file
            strSavePathCurr = strSavePath + strFolderName
            
            try:
                os.mkdir(strSavePathCurr)
            except:
                print('File Path Cannot be Made')
                
            strSavePathCurr = "{}{}".format(strSavePathCurr, strCSVName) # Define the save location
            dfCurrDriverData.to_csv(strSavePathCurr, index=False)
        except:
            print('Unable to save data for Driver: ', str(iDriver))
        iDriver += 1
