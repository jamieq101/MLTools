# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 22:12:59 2023

@author: jamie
"""

def func_ProcessCarData(strCircuitSavePath):
    
    # Takes saved car data for a circuit and processes the data to give the 
    # required inputs that the ML model takes
    
    # Import modules
    import pandas as pd
    
    iDriver = 0
    
    # Loop through each driver 
    while iDriver<20:
        strDriver     = "\DriverData_" + str(iDriver)
        strDirCurr    = strCircuitSavePath + strDriver + strDriver + "_RAW.csv"
        dfCircuitData = pd.read_csv(strDirCurr)     # Loads in data for current driver
        
        # Remove unecesary columns
        dfCircuitDataProcessed = dfCircuitData[['gForceLateral', 'gForceLongitudinal',
                                                'gForceVertical', 'speed', 'tyresPressure', 
                                                'brakesTemperature', 'tyresSurfaceTemperature']]
        iDriver =+ 1 
        
        