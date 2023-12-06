## Alternative method
import numpy as np
import tensorflow as tf
from tensorflow import keras as keras
from tensorflow.keras import layers
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

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
        
        # Convert to numpy array
        X = X.to_numpy()
        Y = Y.to_numpy()
        
        # Make into the correct format
        sequence_length = 100
        X_Data = []
        Y_Data = []
        
        # Loop through and make into correct format
        for i in range(len(X) - sequence_length + 1):
            X_Data.append(X[i:i + sequence_length])
            Y_Data.append(Y[i:i + sequence_length])
            
        # Convert from list to numpy array
        X_Data = np.array(X_Data)
        Y_Data = np.array(Y_Data)
        
        # Scale the data
        scalar_X = MinMaxScaler()
        scalar_Y = MinMaxScaler()
        
        # Reshape for scaling
        X_Data_Flattened = X_Data.reshape(-1, X_Data.shape[-1])
        Y_Data_Flattened = Y_Data.reshape(-1, Y_Data.shape[-1])
        
        X_Data_Scaled = scalar_X.fit_transform(X_Data_Flattened)
        Y_Data_Scaled = scalar_Y.fit_transform(Y_Data_Flattened)
        
        X_Data_Scaled = X_Data_Scaled.reshape(X_Data.shape)
        Y_Data_Scaled = Y_Data_Scaled.reshape(Y_Data.shape)
        
        split = int(0.8 * len(X_Data_Scaled))

        X_Data_Training, X_Val = X_Data_Scaled[:split], X_Data_Scaled[split:]
        Y_Data_Training, Y_Val = Y_Data_Scaled[:split], Y_Data_Scaled[split:]
        
    except:
        print('Lap Missing')    # If there is an error it will display the warning
    i = i+1

# ---------------------------------------------------------------------------------------------------------------

# Define the LSTM model
kModelLSTM = tf.keras.Sequential()
kModelLSTM.add(layers.LSTM(64, input_shape=(X_Data_Training.shape[1], X_Data_Training.shape[2]), return_sequences=True))
kModelLSTM.add(layers.Dense(4, activation='softmax'))

# Compile the model
kModelLSTM.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['accuracy'])

# Train the model
history = kModelLSTM.fit(X_Data_Training, Y_Data_Training, epochs=10, verbose=0)

# Make a prediction
kPrediction = kModelLSTM.predict(X_Val)

# Re-scale the data to compare
dPrediction_Scaled = scalar_Y.inverse_transform(kPrediction.reshape(-1, Y_Data_Training.shape[2]))
dActual_Values = scalar_Y.inverse_transform(Y_Val.reshape(-1, Y_Data_Training.shape[2]))

# Create plot to compare
plt.figure()
plt.plot(dPrediction_Scaled[:,0], label='Prediction', linestyle='-')
plt.plot(dActual_Values[:,0], label='Actual', linestyle='-')
plt.title('Comparison of predicted and actual tyre temperatures')
plt.xlabel('Lap Steps')
plt.ylabel('Tyre Temps (Degrees)')
plt.legend()
plt.show