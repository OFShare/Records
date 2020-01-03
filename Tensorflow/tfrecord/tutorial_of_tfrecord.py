import tensorflow as tf
import numpy as np
import dataset_util,os,preprocessing,cv2

def create_tf_example(input_features, image_dir='/'):
    image_path = input_features['image']
    label = input_features['label']
    image_path = os.path.join(image_dir, image_path)
    image = cv2.imread(image_path)
    encoded_jpg = cv2.imencode('.jpg', image)[1].tostring()
    feature_dict = {
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/label': dataset_util.int64_feature(label),
        'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
    }
    example = tf.train.Example(features=tf.train.Features(
        feature=feature_dict))
    return example

def parse_tf_example(example, is_training, image_size):
    features = {
        'image/label': tf.FixedLenFeature([], dtype=tf.int64),
        'image/encoded': tf.FixedLenFeature([], dtype=tf.string)
    }
    parsed = tf.parse_single_example(serialized=example, features=features)
    label = parsed['image/label']
    encode_image = parsed['image/encoded']

    # return image of [0,1),shape(?,?,3)
    image = preprocessing.decode_image(encode_image)
    # return image of [-1,1),need 4-D of input,but shape(?,?,3) is also ok from my test.
    image = preprocessing.preprocess_image(
        image,
        is_training=is_training,
        height=image_size[0],
        width=image_size[1],
        min_scale=0.8,
        max_scale=1,
        p_scale_up=0.5,
        aug_color=True,
    )
    return image, label

if __name__ == "__main__":
    input_features = {'image':'/home/acui/16.jpg','label':2}
    example = create_tf_example(input_features,image_dir='')
    image,label = parse_tf_example(example.SerializeToString(),is_training=False,image_size=(480,640))
    with tf.Session() as sess:
        image = sess.run(image)
        print('type of image: ',type(image))
        print('image shape: ',image.shape)
        print(image)
        image += 1
        image *=0.5*255
        image = image.astype(np.uint8)
        cv2.imshow('tensorflow.jpg',image)
        cv2.imwrite('tensorflow.jpg',image)
        cv2.waitKey(-1)
