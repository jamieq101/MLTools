# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 13:54:02 2023

@author: jamie
"""

def func_ExtractCarData(strCarDataCSV):
    
    # Imports a CSV file containing car telemetary data and then splits it up
    # into car data
    
    import pandas as pd
    import datetime
    
    dfRAWData = pd.read_csv(strCarDataCSV) # Imports RAW telemetry data from CSV

    print("Loaded in RAW CSV data. Timestamp: ", datetime.datetime.now())
    
    # Need to loop through CSV data to extract data for each car
    dfDriverID = dfRAWData['pilot_index']
    dfDriverID = dfDriverID.unique()        # Finds the unique driver IDs for the dataset
    
    lDriverData = []                        # Makes a blank list that driver data will be added to
    
    try:
        for iDriver in dfDriverID:          # Loops through each driver and finds the rows which correspond
            intID = dfDriverID[iDriver]
            dfRowsIDMatch = dfRAWData.loc[dfRAWData['pilot_index'] == intID]
            lDriverData.append(dfRowsIDMatch)   # Adds data for each driver to a list
    except:
        print("Unable to find rows for each driver")
    
    return lDriverData
            
    