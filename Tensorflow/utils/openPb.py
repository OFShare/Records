# encoding=utf-8
# python3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

model = '/home/acui/download/model.pb' 
graph = tf.get_default_graph()
graph_def = graph.as_graph_def()
graph_def.ParseFromString(tf.gfile.GFile(model, 'rb').read())
tf.import_graph_def(graph_def)
summaryWriter = tf.summary.FileWriter('Acuilog/', graph)



