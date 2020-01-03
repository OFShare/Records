from __future__ import division, print_function, absolute_import

import tensorflow as tf
layers = tf.keras.layers
from tensorflow.contrib import autograph

import numpy as np
import matplotlib.pyplot as plt

#tf.enable_eager_execution()


import numpy as np

@autograph.convert()
def collatz(x):
  x = tf.reshape(x,())
  assert x > 0
  n = tf.convert_to_tensor((0,))
  while not tf.equal(x, 1):
    n += 1
    if tf.equal(x%2, 0):
      x = x // 2
    else:
      x = 3 * x + 1

  return n

with tf.Graph().as_default(),tf.Session() as sess:
  print(sess.run(collatz(np.array([1]))))

# with tf.Graph().as_default():
#   model = tf.keras.Sequential([
#     tf.keras.layers.Lambda(collatz, input_shape=(1,), output_shape=())
#   ])

# graph = tf.get_default_graph()

# with graph.as_default():
#   result = model.predict(np.array([6171]))
#   print(result)

