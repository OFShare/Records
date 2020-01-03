#
# Created by OFShare on 2019-06-03
#

"""Build and train mobilenet_v1 with options for quantization."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from mobilenet import mobilenet_v1

import tensorflow as tf
import glog as logging
import numpy as np
import os
import tensorflow.contrib.slim as slim

flags = tf.app.flags

flags.DEFINE_string('master', '', 'Session master')
flags.DEFINE_integer('task', 0, 'Task')
flags.DEFINE_integer('ps_tasks', 0, 'Number of ps')
flags.DEFINE_integer('batch_size', 64, 'Batch size')
flags.DEFINE_integer('num_classes', 10, 'Number of classes to distinguish')
flags.DEFINE_integer('number_of_steps', None,
                     'Number of training steps to perform before stopping')
flags.DEFINE_integer('image_size', 224, 'Input image resolution')
flags.DEFINE_float('depth_multiplier', 1.0, 'Depth multiplier for mobilenet')
flags.DEFINE_bool('quantize', True, 'Quantize training')
flags.DEFINE_string('fine_tune_checkpoint', '',
                    'Checkpoint from which to start finetuning.')
flags.DEFINE_string('checkpoint_dir', '',
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


def imagenet_input(is_training):
  # 10 classification
  input_data = []
  input_label = []
  lam_data = lambda : np.random.randint(low=0, high=255, size=[224,224,3])
  lam_label = lambda : np.random.randint(low=0, high=10,size=1)
  for i in range(10):
      input_data.append(lam_data())
      input_label.append(lam_label())
  input_data = np.array(input_data,dtype='float32')
  input_label = np.array(input_label,dtype='int64')

  # prepare data
  dataset_a=tf.data.Dataset.from_tensor_slices(input_data)
  dataset_b=tf.data.Dataset.from_tensor_slices(input_label)
  dataset=tf.data.Dataset.zip((dataset_a,dataset_b))
  dataset = dataset.batch(2)
  dataset = dataset.repeat(-1)
  dataset = dataset.prefetch(1)
  inputs = dataset.make_one_shot_iterator().get_next()
  images, labels = inputs[0], inputs[1]
  labels = slim.one_hot_encoding(labels, FLAGS.num_classes)
  labels = tf.squeeze(labels)
  return images, labels


def build_model(is_train=True):
  """Builds graph for model to train with rewrites for quantization.
  Returns:
    g: Graph with fake quantization ops and batch norm folding suitable for
    training quantized weights.
    train_tensor: Train op for execution during training.
  """
  g = tf.Graph()
  with g.as_default():
    inputs, labels = imagenet_input(is_training=True)
    if is_train==False:
      inputs = tf.placeholder(
                  dtype=tf.float32,
                  shape=[None, 224, 224, 3],
                  name="image"
      )
    with slim.arg_scope(mobilenet_v1.mobilenet_v1_arg_scope(is_training=True)):
      logits, end_points = mobilenet_v1.mobilenet_v1(
          inputs,
          is_training=True,
          depth_multiplier=FLAGS.depth_multiplier,
          num_classes=FLAGS.num_classes)
    for k,v in end_points.items():
      print('key: ',k,' value.name ',v.name)
    tf.identity(end_points['Conv2d_1_pointwise'],name='Acui_output')
    # tf.losses.softmax_cross_entropy(labels, logits)
    loss = tf.reduce_sum(tf.square(logits))

    # Call rewriter to produce graph with fake quant ops and folded batch norms
    # quant_delay delays start of quantization till quant_delay steps, allowing
    # for better model accuracy.
    # if FLAGS.quantize:
    #   tf.contrib.quantize.create_training_graph(quant_delay=get_quant_delay())

    # optimizer = tf.train.GradientDescentOptimizer(0.0079)
    # train_op = optimizer.minimize(loss)
    # total_loss = tf.losses.get_total_loss(name='total_loss')
    # decay_steps=10000
    # learning_rate = tf.train.exponential_decay(
    #     get_learning_rate(),
    #     tf.train.get_or_create_global_step(),
    #     decay_steps,
    #     _LEARNING_RATE_DECAY_FACTOR,
    #     staircase=True)
    # opt = tf.train.GradientDescentOptimizer(learning_rate)

    # train_tensor = slim.learning.create_train_op(
    #     total_loss,
    #     optimizer=opt)

  # slim.summaries.add_scalar_summary(total_loss, 'total_loss', 'losses')
  # slim.summaries.add_scalar_summary(learning_rate, 'learning_rate', 'training')
  return g, loss


def get_checkpoint_init_fn():
  """Returns the checkpoint init_fn if the checkpoint is provided."""
  if FLAGS.fine_tune_checkpoint:
    variables_to_restore = slim.get_variables_to_restore()
    global_step_reset = tf.assign(tf.train.get_or_create_global_step(), 0)
    # When restoring from a floating point model, the min/max values for
    # quantized weights and activations are not present.
    # We instruct slim to ignore variables that are missing during restoration
    # by setting ignore_missing_vars=True
    slim_init_fn = slim.assign_from_checkpoint_fn(
        FLAGS.fine_tune_checkpoint,
        variables_to_restore,
        ignore_missing_vars=True)

    def init_fn(sess):
      slim_init_fn(sess)
      # If we are restoring from a floating point model, we need to initialize
      # the global step to zero for the exponential decay to result in
      # reasonable learning rates.
      sess.run(global_step_reset)
    return init_fn
  else:
    return None


def train_model():
  """Trains mobilenet_v1."""
  g, loss = build_model()
  with g.as_default():
    # Call rewriter to produce graph with fake quant ops and folded batch norms
    # quant_delay delays start of quantization till quant_delay steps, allowing
    # for better model accuracy.
    if FLAGS.quantize:
      tf.contrib.quantize.create_training_graph(quant_delay=0)
    optimizer = tf.train.GradientDescentOptimizer(0.0079)
    train_op = optimizer.minimize(loss)

    init = tf.global_variables_initializer()
    saver = tf.train.Saver()
    # execute train model and save variables to checkpoint
    with tf.Session() as sess:
        sess.run(init)
        try:
            cnt = 0
            while True:
                cnt += 1
                [_]= sess.run(fetches=[train_op])
                if(cnt>=10):
                    break
        except tf.errors.OutOfRangeError:
        #except Exception as e:
            logging.info('train model done')
        finally:
            checkpoint_path = os.path.join('checkpoint_dir','Acuimodel')
            ret_prefix= saver.save(sess=sess, save_path=checkpoint_path, global_step=None)

    # from checkpoint convert to tensorflow frozened pb
    # with tf.Session() as sess:
    #     checkpoint_path = tf.train.latest_checkpoint('checkpoint_dir')
    #     logging.info('latest_checkpoint:%s'%str(checkpoint_path))
    #     saver.restore(sess=sess, save_path=checkpoint_path)
    #     graph_name = 'Acui_frozened.pb'
    #     output_graph = tf.graph_util.convert_variables_to_constants(sess, input_graph_def=sess.graph_def, output_node_names=['Acui_output'])
    #     ret_path = tf.train.write_graph(graph_or_graph_def=output_graph,logdir='checkpoint_dir', name=graph_name, as_text=False)
    #     logging.info('ret_pbmodel_path:%s'%str(ret_path))
    #     logging.info('save frozen pb model done')
  # with g.as_default():
  #   slim.learning.train(
  #       train_tensor,
  #       FLAGS.checkpoint_dir,
  #       is_chief=(FLAGS.task == 0),
  #       master=FLAGS.master,
  #       log_every_n_steps=FLAGS.log_every_n_steps,
  #       graph=g,
  #       number_of_steps=FLAGS.number_of_steps,
  #       save_summaries_secs=FLAGS.save_summaries_secs,
  #       save_interval_secs=FLAGS.save_interval_secs,
  #       init_fn=get_checkpoint_init_fn(),
  #       global_step=tf.train.get_global_step())

def save_model():
  """Trains mobilenet_v1."""
  g, loss = build_model(is_train=False)
  with g.as_default():
    tf.contrib.quantize.create_eval_graph(input_graph=g)
    saver = tf.train.Saver()
    # from checkpoint convert to tensorflow frozened pb
    with tf.Session() as sess:
        # Save the checkpoint and eval graph proto to disk for freezing
        # and providing to TFLite.
        with open('eval_graph_def.pb', 'w') as f:
          f.write(str(sess.graph_def))
        checkpoint_path = tf.train.latest_checkpoint('checkpoint_dir')
        logging.info('latest_checkpoint:%s'%str(checkpoint_path))
        saver.restore(sess=sess, save_path=checkpoint_path)
        graph_name = 'Acui_frozened.pb'
        output_graph = tf.graph_util.convert_variables_to_constants(sess, input_graph_def=sess.graph_def, output_node_names=['Acui_output'])
        ret_path = tf.train.write_graph(graph_or_graph_def=output_graph,logdir='checkpoint_dir', name=graph_name, as_text=False)
        logging.info('ret_pbmodel_path:%s'%str(ret_path))
        logging.info('save frozen pb model done')


def main(unused_arg):
  train_model()
  save_model()


if __name__ == '__main__':
  tf.app.run(main)
