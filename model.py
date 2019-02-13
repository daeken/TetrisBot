import tensorflow as tf
from tensorflow.keras import layers

"""
inputs:
	- direction to nearest, lowest, flattest point
	- portion of piece to land 'flat' (all bottom tiles sitting on others/the base)
outputs: left/right (-1..1), ccw/cw (-1..1), drop (>=0.9)

weights: 3 * 2
biases: 3
"""

model = tf.keras.Sequential()
model.add(layers.Dense(3, activation='tanh', input_dim=2))

model.compile(optimizer=tf.train.AdamOptimizer(0.001), loss='mse', metrics=['mae'])
