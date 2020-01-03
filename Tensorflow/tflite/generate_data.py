#
# created by OFShare on 2019-06-06
#

import tensorflow as tf
import numpy as np

def generate_data():
    batch_size = 1
    height, width = 2, 2
    gene_data = tf.random_uniform((batch_size, height, width, 3))
    return gene_data

def prepare_data(np_input):
    # prepare data
    dataset = tf.data.Dataset.from_tensors(np_input)
    dataset = dataset.repeat(-1)
    dataset = dataset.prefetch(1)
    input_data = dataset.make_one_shot_iterator().get_next()
    return input_data

# init = tf.global_variables_initializer()

with tf.Session() as sess:
    # sess.run([init])
    np_input = sess.run(generate_data())
    print('np_input: ',np_input)

with tf.Session() as sess:
    input_data = prepare_data(np_input)
    np_ret = sess.run(input_data)
    print('\nnp_ret1: ',np_ret)
    np_ret = sess.run(input_data)
    print('\nnp_ret2: ',np_ret)
