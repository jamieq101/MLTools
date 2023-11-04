# Example Python Script to Fit a Linear Regression to a Dataset
# Uses TensorFlow (the backend of Keras)

import tensorflow as tf
import keras
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Import data to use to train the machine learning model for this example use 
# example data. There are 8 input variables (X) and one output variable (y) 
# which is a 1 or 0.

aSampleData = np.loadtxt(r'C:\Users\jamie\OneDrive - University of Southampton\GDP Personal\Test Data\TestData.csv', delimiter=',')
aInputX = aSampleData[:,0:8]
aInputy = aSampleData[:,8]

# Define the Keras model. A Keras model is defined in a sequence of layers.
# Dense is the class to define connected layers

kModel = Sequential()
kModel.add(Dense(12, input_shape=(8,), activation='relu')) # There are 12 nodes with 8 variables.
kModel.add(Dense(8, activation='relu'))
kModel.add(Dense(1, activation='sigmoid')) # In total there are 3 layers

# Compile the Keras model. binary_crossentropy is used as the loss model
# An Adam optimer is used. It is one of the best ones to use

kModel.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Next the Keras is ready to be fitted. Epochs and batches have to be defined.
# Epoch defines the number of times the model passes through the dataset. Batch
# defines how many rows it looks at before updating.

kModel.fit(aInputX, aInputy, epochs=10, batch_size=10)

# The above step will run the model and its accuracy can be evaluated:
_, fAccuracy = kModel.evaluate(aInputX, aInputy)
print('Accuracy: %.2f' % (fAccuracy*100))

yPrediction = kModel.predict(aInputX[1])
print(yPrediction)
           
