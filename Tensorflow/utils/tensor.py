import tensorflow as tf

# Cast a constant integer tensor into floating point.
float_tensor = tf.cast(tf.constant([1, 2, 3]), dtype=tf.float32)

with tf.Session() as sess:
        print(sess.run(float_tensor))