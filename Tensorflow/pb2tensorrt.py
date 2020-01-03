#
# Created by OFShare on 2019-11-15
#

# This script convert frozen pb to TensorRt accelerated frozen pb

import tensorflow as tf
import tensorflow.contrib.tensorrt as trt
import cv2, time, sys
import numpy as np
import glog as logging

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0, 1, 2, 3, 4"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_model', default='input.pb', type =str, help = 'input frozen pb')
parser.add_argument('--output_model', default='output_TRTFP16.pb', type =str, help = 'output frozen pb with TensorRt accelerated')
args = parser.parse_args()

def getFP16(graph_def, batch_size = 1, workspace_size = 1<<30):
   filename = args.output_model 
   if tf.gfile.Exists(filename):
     print("#### load TensorRt pb from disk that already existed")
     with tf.gfile.GFile(filename, 'rb') as f:
         graph_def = tf.GraphDef()
         graph_def.ParseFromString(f.read())
         return graph_def
 
   trt_graph = trt.create_inference_graph(graph_def, ["outputs"],
                                          max_batch_size=batch_size,
                                          max_workspace_size_bytes=workspace_size,
                                          precision_mode="FP16")  # Get optimized graph
   with tf.gfile.FastGFile(filename, 'wb') as f:
     f.write(trt_graph.SerializeToString())
   return trt_graph

if __name__ == '__main__':
    model_path = args.input_model
    with tf.gfile.GFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    graph = tf.Graph()
    with graph.as_default():
        tf.import_graph_def(getFP16(graph_def), name='')
