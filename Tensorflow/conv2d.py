#
# created by OFShare on 2019-05-29
#

# that's a simple case to demenstrate conv2d

import tensorflow as tf
import tensorflow.contrib.slim as slim

_init_xavier = tf.contrib.layers.xavier_initializer()
_init_norm = tf.truncated_normal_initializer(stddev=0.01)
_init_zero = slim.init_ops.zeros_initializer()
_l2_regularizer_00004 = tf.contrib.layers.l2_regularizer(0.00004)

def _conv_bn_relu(inputs, filters, kernel_size = 1, strides = 1, pad = 'VALID', name = 'conv_bn_relu'):
	""" Spatial Convolution (CONV2D) + BatchNormalization + ReLU Activation
	Args:
		inputs			: Input Tensor (Data Type : NHWC)
		filters		: Number of filters (channels)
		kernel_size	: Size of kernel
		strides		: Stride
		pad				: Padding Type (VALID/SAME) # DO NOT USE 'SAME' NETWORK BUILT FOR VALID
		name			: Name of the block
	Returns:
		norm			: Output Tensor
	"""
	with tf.name_scope(name):
		kernel = tf.Variable(tf.contrib.layers.xavier_initializer(uniform=False)([kernel_size,kernel_size, inputs.get_shape().as_list()[3], filters]), name= 'weights')
		conv = tf.nn.conv2d(inputs, kernel, [1,strides,strides,1], padding='VALID', data_format='NHWC')
		norm = tf.contrib.layers.batch_norm(conv, 0.9, epsilon=1e-5, activation_fn = tf.nn.relu, is_training = True)
		return norm

input = tf.get_variable(name = 'Acui',shape = (3,262,262,3) )
with slim.arg_scope([slim.batch_norm], decay = 0.999, fused = True, is_training = True):
    output = slim.convolution2d(
        inputs = input,
        num_outputs = 16,
        kernel_size = [3, 3],
        stride = 5,
        padding = 'same', # 'valid', 'same'
        normalizer_fn = slim.batch_norm,
        weights_regularizer = _l2_regularizer_00004,
        weights_initializer = _init_xavier,
        biases_initializer = _init_zero,
        activation_fn = tf.nn.relu,
        scope = 'Acui_test',
        trainable =True )

conv1 = _conv_bn_relu(input, filters= 64, kernel_size = 7, strides = 2, name = 'conv_256_to_128')

init = tf.global_variables_initializer()

if __name__ == '__main__':
    with tf.Session() as sess:
        sess.run(init)
        np_ret1, np_ret2 = sess.run([output,conv1])
        print('input.shape: ', input.shape)
        print('np_ret1.shape: ', np_ret1.shape)
        print('np_ret2.shape: ', np_ret2.shape)
