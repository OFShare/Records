#
# created by OFShare on 2019-06-06
#

"""Validate mobilenet_v1 with options for quantization."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import numpy as np
import tensorflow as tf

import mobilenet_v1

slim = tf.contrib.slim

flags = tf.app.flags

flags.DEFINE_string('master', '', 'Session master')
flags.DEFINE_integer('batch_size', 1, 'Batch size')
flags.DEFINE_integer('num_classes', 10, 'Number of classes to distinguish')
flags.DEFINE_integer('num_examples', 1, 'Number of examples to evaluate')
flags.DEFINE_integer('image_size', 224, 'Input image resolution')
flags.DEFINE_float('depth_multiplier', 1.0, 'Depth multiplier for mobilenet')
flags.DEFINE_bool('quantize', True, 'Quantize training')
flags.DEFINE_string('checkpoint_dir', './train_dir/model.ckpt-5', 'The directory for checkpoints')
flags.DEFINE_string('eval_dir', './evel_dir', 'Directory for writing eval event logs')
flags.DEFINE_string('dataset_dir', '', 'Location of dataset')

FLAGS = flags.FLAGS

def build_model():
  """Build the mobilenet_v1 model for freeze.
  Returns:
    g: graph with rewrites after insertion of quantization ops and batch norm
    folding.
  """
  g = tf.Graph()
  with g.as_default():
    inputs = tf.placeholder(
            dtype=tf.float32,
            shape=[None, FLAGS.image_size,FLAGS.image_size, 3],
            name="input_node")
    scope = mobilenet_v1.mobilenet_v1_arg_scope(
        is_training=False, weight_decay=0.0)
    with slim.arg_scope(scope):
      logits, _ = mobilenet_v1.mobilenet_v1(
          inputs,
          is_training=False,
          depth_multiplier=FLAGS.depth_multiplier,
          num_classes=FLAGS.num_classes)
    logits = tf.identity(logits,name='output_node')
    if FLAGS.quantize:
      tf.contrib.quantize.create_eval_graph()
  return g


def frozen_model():
  """freeze mobilenet_v1 to frozen pb"""
  g = build_model()
  graph_name = 'frozen.pb'
  with g.as_default():
      with tf.Session() as sess:
        saver = tf.train.Saver()
        checkpoint_path = tf.train.latest_checkpoint('train_dir')
        saver.restore(sess=sess, save_path=checkpoint_path)
        output_graph = tf.graph_util.convert_variables_to_constants(
          sess,
          input_graph_def=sess.graph_def,
          output_node_names=['output_node'])

  ret_path = tf.train.write_graph(
      graph_or_graph_def=output_graph,
      logdir='frozen_models',
      name=graph_name,
      as_text=False)


def main(unused_arg):
  frozen_model()


if __name__ == '__main__':
  tf.app.run(main)
