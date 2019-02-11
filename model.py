import tensorflow as tf
from tensorflow.keras import layers

"""
inputs: 10 columns with the value being the height of the top, piece x and y (0..1), piece orientation (0, 0.25, 0.5, 1), piece type (0..1), next piece (0..1)
outputs: left, right, rotate left, rotate right

weights: 32 * 15 + 16 * 32 + 4 * 16
biases: 32 + 16 + 4
"""

model = tf.keras.Sequential()
model.add(layers.Dense(32, activation='tanh', input_dim=10 + 5))
model.add(layers.Dense(16, activation='tanh'))
model.add(layers.Dense(4, activation='tanh'))

model.compile(optimizer=tf.train.AdamOptimizer(0.001), loss='mse', metrics=['mae'])
