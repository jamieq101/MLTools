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
    import os
    import matplotlib.pyplot as plt

    iDriver = 0

    # Loop through each driver 
    while iDriver<19:
        strDriver     = "\DriverData_" + str(iDriver)
        strDirCurr    = strCircuitSavePath + strDriver + strDriver + "_RAW.csv"
        dfCircuitData = pd.read_csv(strDirCurr)     # Loads in data for current driver

        # Remove unecesary columns
        dfCircuitDataProcessed = dfCircuitData[['gForceLateral', 'gForceLongitudinal',
                                                'gForceVertical', 'speed', 'steer',
                                                'brakesTemperature', 'tyresSurfaceTemperature', 
                                                'currentLapNum', 'pitStatus', 'throttle', 'brake']]
        
        # Create a common alias for each column
        strColumnAlias = {'gForceLateral': 'gLat', 'gForceLongitudinal': 'gLong', 
                          'gForceVertical': 'gVert', 'speed': 'vCar', 'steer': 'aSteer',
                          'throttle': 'pThrottle', 'brake': 'pBrake'}
        
        # Create separated brake and tyre temperatures
        TBrakesAll = dfCircuitDataProcessed['brakesTemperature'].str.split('/', expand=True)       
        TTyreSurface = dfCircuitDataProcessed['tyresSurfaceTemperature'].str.split('/', expand=True)
        
        TBrakeFL  = TBrakesAll[0]
        TBrakeFR  = TBrakesAll[1]
        TBrakeRL  = TBrakesAll[2]
        TBrakeRR  = TBrakesAll[3]       
        TTyreSurfaceFL = TTyreSurface[0]
        TTyreSurfaceFR = TTyreSurface[1]
        TTyreSurfaceRL = TTyreSurface[2]
        TTyreSurfaceRR = TTyreSurface[3]
        
        dfCircuitDataProcessed.loc[:,'TBrakeFL'] = TBrakeFL
        dfCircuitDataProcessed.loc[:,'TBrakeFR'] = TBrakeFR
        dfCircuitDataProcessed.loc[:,'TBrakeRL'] = TBrakeRL
        dfCircuitDataProcessed.loc[:,'TBrakeRR'] = TBrakeRR
        dfCircuitDataProcessed.loc[:,'TTyreSurfaceFL'] = TTyreSurfaceFL
        dfCircuitDataProcessed.loc[:,'TTyreSurfaceFR'] = TTyreSurfaceFR
        dfCircuitDataProcessed.loc[:,'TTyreSurfaceRL'] = TTyreSurfaceRL
        dfCircuitDataProcessed.loc[:,'TTyreSurfaceRR'] = TTyreSurfaceRR
        
        dfCircuitDataProcessed = dfCircuitDataProcessed.drop(['brakesTemperature', 'tyresSurfaceTemperature'], axis=1)
        
        # Set column names to match common alias
        dfCircuitDataProcessed = dfCircuitDataProcessed.rename(columns=strColumnAlias)
        
        # Save the processed list as a csv for each driver
        strSaveLoc = strCircuitSavePath + strDriver + strDriver + "_Processed.csv" 
        #dfCircuitDataProcessed.to_csv(strSaveLoc, index=False)  # Save the processed data
        
        # Seperate into different laps for each driver
        strNewDir = strCircuitSavePath + strDriver +  "\\Laps\\"
        try: 
            os.mkdir(strNewDir)
        except:
            print('Filepath cannot be created')
        
        dfCircuitDataProcessed = dfCircuitDataProcessed[dfCircuitDataProcessed['vCar'] != 0] # Removes points where the car is stationary
        
        dfLapUnique = dfCircuitDataProcessed['currentLapNum'].unique() # Finds unique lap numbers

        for iLap in dfLapUnique:
            tCurrLap = dfCircuitDataProcessed[dfCircuitDataProcessed.currentLapNum == iLap]
            dfCurrLap = pd.DataFrame(tCurrLap)
            bIncludesPit = (dfCurrLap['pitStatus'] == 'pitting').any()
            
            if bIncludesPit:
                strSaveLoc = strNewDir + strDriver + '_Lap_NOTE:_PIT' + str(iLap) + '.csv'
                strSaveFig = strNewDir + strDriver + '_Lap_NOTE:_PIT' + str(iLap) + '.jpg'
            else:
                strSaveLoc = strNewDir + strDriver + '_Lap_' + str(iLap) + '.csv'
                strSaveFig = strNewDir + strDriver + '_Lap_' + str(iLap) + '.jpg'
            
            dfCurrLap = dfCurrLap.drop(['currentLapNum', 'pitStatus'], axis=1) # Remove additional lap info
            dfCurrLap.to_csv(strSaveLoc, index=False) # Save the lap by lap data
            
            # Make plots for verification later
            x = len(dfCurrLap['vCar'])
            y1 = dfCurrLap['vCar']
            y2 = dfCurrLap['gLat']
            y3 = dfCurrLap['gLong']
            y4 = dfCurrLap['pThrottle']
            y5 = dfCurrLap['pBrake']
            
            ax = plt.subplots(3)
            
            ax[0].plot(y1, label='vCar (kph)', color='blue')
            ax[0].legend()
            ax[0].grid()
            ax[1].plot(y2, label='gLat', color='blue')
            ax[1].plot(y3, label='gLong', color='red')
            ax[1].legend()
            ax[1].grid()
            ax[2].plot(y4, label='pThrottle (%)', color='blue')
            ax[2].plot(y5, label='pBrake (%)', color='red')
            ax[2].legend()
            ax[2].grid()
            plt.savefig(strSaveFig)
        
        iDriver = iDriver + 1
        
        