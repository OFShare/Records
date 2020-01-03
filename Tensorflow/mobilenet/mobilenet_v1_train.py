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

"""Build and train mobilenet_v1 with options for quantization."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import mobilenet_v1

slim = tf.contrib.slim

flags = tf.app.flags

flags.DEFINE_string('master', '', 'Session master')
flags.DEFINE_integer('task', 0, 'Task')
flags.DEFINE_integer('ps_tasks', 0, 'Number of ps')
flags.DEFINE_integer('batch_size', 1, 'Batch size')
flags.DEFINE_integer('num_classes', 10, 'Number of classes to distinguish')
flags.DEFINE_integer('number_of_steps', 5,
                     'Number of training steps to perform before stopping')
flags.DEFINE_integer('image_size', 224, 'Input image resolution')
flags.DEFINE_float('depth_multiplier', 1.0, 'Depth multiplier for mobilenet')
flags.DEFINE_bool('quantize', True, 'Quantize training')
flags.DEFINE_string('fine_tune_checkpoint', '',
                    'Checkpoint from which to start finetuning.')
flags.DEFINE_string('checkpoint_dir', './train_dir',
                    'Directory for writing training checkpoints and logs')
flags.DEFINE_string('dataset_dir', '', 'Location of dataset')
flags.DEFINE_integer('log_every_n_steps', 100, 'Number of steps per log')
flags.DEFINE_integer('save_summaries_secs', 100,
                     'How often to save summaries, secs')
flags.DEFINE_integer('save_interval_secs', 100,
                     'How often to save checkpoints, secs')

FLAGS = flags.FLAGS

_LEARNING_RATE_DECAY_FACTOR = 0.94


def get_learning_rate():
  if FLAGS.fine_tune_checkpoint:
    # If we are fine tuning a checkpoint we need to start at a lower learning
    # rate since we are farther along on training.
    return 1e-4
  else:
    return 0.045


def get_quant_delay():
  if FLAGS.fine_tune_checkpoint:
    # We can start quantizing immediately if we are finetuning.
    return 0
  else:
    # We need to wait for the model to train a bit before we quantize if we are
    # training from scratch.
    return 250000


def build_model():
  """Builds graph for model to train with rewrites for quantization.
  Returns:
    g: Graph with fake quantization ops and batch norm folding suitable for
    training quantized weights.
    train_tensor: Train op for execution during training.
  """
  g = tf.Graph()
  with g.as_default(), tf.device(
      tf.train.replica_device_setter(FLAGS.ps_tasks)):
    inputs = np.random.randint(0, 255, size=(1,224,224,3))
    labels = np.random.randint(0, 10, size=(1))
    labels = slim.one_hot_encoding(labels, FLAGS.num_classes)
    inputs = tf.Variable(inputs,dtype=tf.float32)
    labels = tf.Variable(labels,dtype=tf.float32)
    with slim.arg_scope(mobilenet_v1.mobilenet_v1_arg_scope(is_training=True)):
      logits, _ = mobilenet_v1.mobilenet_v1(
          inputs,
          is_training=True,
          depth_multiplier=FLAGS.depth_multiplier,
          num_classes=FLAGS.num_classes)

    tf.losses.softmax_cross_entropy(labels, logits)

    # Call rewriter to produce graph with fake quant ops and folded batch norms
    # quant_delay delays start of quantization till quant_delay steps, allowing
    # for better model accuracy.
    if FLAGS.quantize:
      tf.contrib.quantize.create_training_graph(quant_delay=0)

    total_loss = tf.losses.get_total_loss(name='total_loss')
    # Configure the learning rate using an exponential decay.
    num_epochs_per_decay = 2.5
    imagenet_size = 1271167
    decay_steps = int(imagenet_size / FLAGS.batch_size * num_epochs_per_decay)

    learning_rate = tf.train.exponential_decay(
        get_learning_rate(),
        tf.train.get_or_create_global_step(),
        decay_steps,
        _LEARNING_RATE_DECAY_FACTOR,
        staircase=True)
    opt = tf.train.GradientDescentOptimizer(learning_rate)

    train_tensor = slim.learning.create_train_op(
        total_loss,
        optimizer=opt)

  slim.summaries.add_scalar_summary(total_loss, 'total_loss', 'losses')
  slim.summaries.add_scalar_summary(learning_rate, 'learning_rate', 'training')
  return g, train_tensor


def train_model():
  """Trains mobilenet_v1."""
  g, train_tensor = build_model()
  with g.as_default():
    slim.learning.train(
        train_tensor,
        FLAGS.checkpoint_dir,
        is_chief=(FLAGS.task == 0),
        master=FLAGS.master,
        log_every_n_steps=FLAGS.log_every_n_steps,
        graph=g,
        number_of_steps=FLAGS.number_of_steps,
        save_summaries_secs=FLAGS.save_summaries_secs,
        save_interval_secs=FLAGS.save_interval_secs,
        init_fn=None,
        global_step=tf.train.get_global_step())


def main(unused_arg):
  train_model()


if __name__ == '__main__':
  tf.app.run(main)
