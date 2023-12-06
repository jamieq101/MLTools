import numpy as np
import tensorflow as tf
from tensorflow import keras as keras
from tensorflow.keras import layers
import pandas as pd

# ---------------------------------------------------------------------------------------------------------------

X_Data = []
Y_Data =[]
strLapData = r"C:\Users\jamie\University of Southampton\GDP 23 24 - General\Artifical Inteligence\Data Sets\Sample Data Sets\F1 Data (From Kaggle)\CircuitZandvoort\\"
i = 1
dMaxIter = 2

# Loop through data to extract X and Y data and format as required
while i<dMaxIter:
    strLapDataCSV = strLapData + 'DriverData_' + str(i) + '\Laps' + '\\DriverData_' + str(i) + '_Lap_' + str(i) + '.csv'
    try:
        lData = pd.read_csv(strLapDataCSV)
        X = lData[["gLat","gLong","gVert","vCar","aSteer","pThrottle","pBrake","TBrakeFL","TBrakeFR","TBrakeRL","TBrakeRR"]] # Isolates columns required
        Y = lData[["TTyreSurfaceFL","TTyreSurfaceFR","TTyreSurfaceRL","TTyreSurfaceRR"]]
        X = X.to_numpy()
        dSizeX   = len(X)
        dNumVarX = len(X[1])
        X_Data = X.reshape((dMaxIter-1, dSizeX, dNumVarX))  # Converts to a 3D array as required by LSTM
        Y = Y.to_numpy()
        dSizeY   = len(Y)
        dNumVarY = len(Y[1])
        Y_Data = Y.reshape((dMaxIter-1, dSizeY, dNumVarY))
    except:
        print('Lap Missing')    # If there is an error it will display the warning
    i = i+1

# ---------------------------------------------------------------------------------------------------------------

# Define the LTSM model
kModelLSTM = tf.keras.Sequential()
kModelLSTM.add(layers.LSTM(64, input_shape=(X_Data.shape[1], X_Data.shape[2])))
kModelLSTM.add(layers.BatchNormalization())
kModelLSTM.add(layers.Dense(4, activation='softmax'))
print(kModelLSTM.summary())

# Compile the model
kModelLSTM.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['accuracy'])

# Train the model
kModelLSTM.fit(X_Data, Y_Data, epochs=10, verbose=0)

# plt.plot(model.predict(X_test))
# plt.ylim(75,120)
# plt.show()