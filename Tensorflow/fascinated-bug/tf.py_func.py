#
# created by OFShare on 2019-06-29
#

import tensorflow as tf
import numpy as np
import cv2
from pycocotools.coco import COCO

COCO_DATA = None

def _parse_function(imgId):
    global COCO_DATA
    # Function test2 executes the one of following below two lines of code is the same, will not report an error.
    # But in test1, only the first sentence function can be executed, and the second sentence will report an error.
    # error looks like this: TypeError: 'NoneType' object is not subscriptable, indicate COCO_DATA.loadImgs(imgId) is 'NoneType'
    # instead of type of List
    if imgId == 37777:
        print('doing test2...')
        img_meta = COCO_DATA.loadImgs([imgId])[0]
        img_meta = COCO_DATA.loadImgs(imgId)[0]
    elif imgId == 397133:
        print('doing test1...')
        img_meta = COCO_DATA.loadImgs([imgId])[0]
        # img_meta = COCO_DATA.loadImgs(imgId)[0]

    return np.float32(imgId),np.float32(imgId*10)

def pipeline():
    lis = [397133]
    dataset = tf.data.Dataset.from_tensor_slices(lis)
    dataset = dataset.map(
        lambda imgId: tuple(
            tf.py_func(
               func=_parse_function,
               inp=[imgId],
               Tout=[tf.float32, tf.float32]
            )
        ))
    return dataset

def test1():
    train_dataset = pipeline()
    train_iterator = train_dataset.make_one_shot_iterator()
    input_image, input_heat = train_iterator.get_next()
    with tf.Session() as sess:
        ret1, ret2 = sess.run([input_image,input_heat])
        print('okkkkkkk')

def test2():
    lis = [37777]
    _parse_function(lis[0])
    print('okkkkkk')

if __name__ == '__main__':
    COCO_DATA = COCO('/home/acui/Desktop/coco2017/annotations/person_keypoints_val2017.json')
    test1()
    test2()
