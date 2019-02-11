import tensorflow as tf
from tensorflow.keras import layers

"""
inputs: 10x20 grid, piece x and y (0..1), piece orientation (0, 0.25, 0.5, 1), piece type (0..1), next piece (0..1)
outputs: left, right, rotate left, rotate right

weights: 64 * 205 + 32 * 64 + 4 * 32
biases: 64 + 32 + 4
"""

model = tf.keras.Sequential()
model.add(layers.Dense(64, activation='sigmoid', input_dim=10 * 20 + 5))
model.add(layers.Dense(32, activation='sigmoid'))
model.add(layers.Dense(4, activation='sigmoid'))

model.compile(optimizer=tf.train.AdamOptimizer(0.001), loss='mse', metrics=['mae'])
