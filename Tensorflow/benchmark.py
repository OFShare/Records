#
# Created by OFShare on 2019-11-15
#

# This script tests speed of frozen pb and tflite model

# Usage:

# 1. run frozen pb: 
#    python benchmark.py --model models/input.pb --batch_size 1 --height 320 --width 320 1> log.std 2> log.err & 

# 2. run tflite:
#    python benchmark.py --model models/input.tflite 1> log.std 2> log.err &



import tensorflow as tf
import tensorflow.contrib.tensorrt as trt
import cv2, time, sys
import numpy as np
import glog as logging

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0, 1, 2, 3, 4"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--model', default='input.pb', help = 'model path, tflite or pb graph')
parser.add_argument('--batch_size', default=1, type = int, help = 'batch size')
parser.add_argument('--height', default=224, type = int, help = 'image height')
parser.add_argument('--width', default=224, type = int, help = 'image width')
args = parser.parse_args()

class Benchmark:
    def __init__(self):
        self._is_tflite = args.model.split('.')[-1] == 'tflite'
        model_path = args.model
        if not self._is_tflite:
            logging.info('load frozen pb graph') 
            with tf.gfile.GFile(model_path, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
            graph = tf.Graph()
            with graph.as_default():
                tf.import_graph_def(graph_def, name='')

            self.input_image = graph.get_tensor_by_name('image_tensor:0')
            self.output_ops = [
                graph.get_tensor_by_name('num:0'),
            ]
            # gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction = 0.67)
            # config = tf.ConfigProto(allow_soft_placement = True, log_device_placement = False, gpu_options = gpu_options)
            config = tf.ConfigProto(allow_soft_placement = True, log_device_placement = False)
            self._sess = tf.Session(graph=graph, config = config)
        else:
            logging.info('load tflite graph') 
            # Load TFLite model and allocate tensors.
            self._interpreter = tf.lite.Interpreter(model_path=model_path)
            self._interpreter.allocate_tensors()
            # Get input and output tensors.
            self._input_details = self._interpreter.get_input_details()
            self._output_details = self._interpreter.get_output_details()

    def __call__(self):
        # Test model on random input data.
        if not self._is_tflite:
            dummy_input = np.random.random_sample((args.batch_size, args.height, args.width, 3))
            while True:
                start = time.time()
                out = self._sess.run(self.output_ops, feed_dict={self.input_image: dummy_input})
                end = time.time()
                print("### frozen pb inference time: ", end - start , " seconds")
        else:
            input_shape = self._input_details[0]['shape']
            dummy_input = np.array(np.random.random_sample(input_shape), dtype = np.float32)
            while True: 
                self._interpreter.set_tensor(self._input_details[0]['index'], dummy_input)
                start = time.time()
                self._interpreter.invoke()
                end = time.time()
                print("### tflite inference time: ", end - start , " seconds")

if __name__ == '__main__':
    model = Benchmark()
    model()
