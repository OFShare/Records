# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

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

def metrics(logits, labels):
  """Specify the metrics for eval.
  Args:
    logits: Logits output from the graph.
    labels: Ground truth labels for inputs.
  Returns:
     Eval Op for the graph.
  """
  # labels = tf.squeeze(labels)
  # print('logits: ',logits)
  # print('labels: ',labels)
  # raise ValueError('stop here')
  names_to_values, names_to_updates = slim.metrics.aggregate_metric_map({
      'Accuracy': tf.metrics.accuracy(tf.argmax(logits, 1), tf.argmax(labels,1)),
      # 'Recall_1': tf.metrics.recall_at_k(labels, logits, 1),
  })
  for name, value in names_to_values.items():
    slim.summaries.add_scalar_summary(
        value, name, prefix='eval', print_summary=True)
  return names_to_updates.values()


def build_model():
  """Build the mobilenet_v1 model for evaluation.
  Returns:
    g: graph with rewrites after insertion of quantization ops and batch norm
    folding.
    eval_ops: eval ops for inference.
    variables_to_restore: List of variables to restore from checkpoint.
  """
  g = tf.Graph()
  with g.as_default():
    # inputs, labels = imagenet_input(is_training=False)
    inputs = np.random.randint(0, 255, size=(1,224,224,3))
    labels = np.random.randint(0, 10, size=(1,10))
    inputs = tf.Variable(inputs,dtype=tf.float32)
    labels = tf.Variable(labels,dtype=tf.float32)
    scope = mobilenet_v1.mobilenet_v1_arg_scope(
        is_training=False, weight_decay=0.0)
    with slim.arg_scope(scope):
      logits, _ = mobilenet_v1.mobilenet_v1(
          inputs,
          is_training=False,
          depth_multiplier=FLAGS.depth_multiplier,
          num_classes=FLAGS.num_classes)

    if FLAGS.quantize:
      tf.contrib.quantize.create_eval_graph()

    eval_ops = metrics(logits, labels)

  return g, eval_ops


def eval_model():
  """Evaluates mobilenet_v1."""
  g, eval_ops = build_model()
  with g.as_default():
    # num_batches = math.ceil(FLAGS.num_examples / float(FLAGS.batch_size))
    num_batches = 1
    slim.evaluation.evaluate_once(
        FLAGS.master,
        FLAGS.checkpoint_dir,
        logdir=FLAGS.eval_dir,
        num_evals=num_batches,
        eval_op=(list(eval_ops ) ))
    # raise ValueError('stop here')


def main(unused_arg):
  eval_model()


if __name__ == '__main__':
  tf.app.run(main)
