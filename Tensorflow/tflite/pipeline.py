# author: OFShare
# date: Fri Apr 19 14:16:16 CST 2019

import tensorflow as tf
import numpy as np
import glog as logging
import os

input_data = np.random.uniform(low=0.0, high=10.0, size=10)
input_label = np.abs(input_data)
np_input = np.array([(a,b) for a,b in zip(input_data,input_label)])
logging.info('np_input:%s'%str(np_input))

def train_model():
    # prepare data
    dataset = tf.data.Dataset.from_tensor_slices(np_input)
    dataset = dataset.repeat(-1)
    dataset = dataset.prefetch(1)
    inputs = dataset.make_one_shot_iterator().get_next()

    # construct net architecture
    offset = tf.get_variable("offset", [1,], tf.float32)
    x = tf.placeholder(tf.float32, shape=(None,),name='Acui_input')
    y = tf.abs(x + offset,name='Acui_output')
    y_ = tf.placeholder(tf.float32, shape=(None,),name='Acui_output_2')
    loss = tf.reduce_sum(tf.square(y - y_))
    optimizer = tf.train.GradientDescentOptimizer(0.0079)
    train_op = optimizer.minimize(loss)

    saver = tf.train.Saver()
    init = tf.global_variables_initializer()

    # execute train model and save variables to checkpoint
    with tf.Session() as sess:
        sess.run(init)
        try:
            cnt = 0
            while True:
                cnt += 1
                np_inputs,np_labels = sess.run([inputs[0],inputs[1]])
                logging.info('np_inputs: %s,np_labels: %s'%(str(np_inputs),str(np_labels)))
                [_,np_offset,np_loss]= sess.run(fetches=[train_op,offset,loss],feed_dict={x:np.array([np_inputs]),y_:np.array([np_labels])})
                logging.info('np_offset: %s,np_loss: %s,cnt: %s'%(str(np_offset),str(np_loss),str(cnt)))
                if(cnt>=1000 or np_loss<1e-7):
                    break
        except tf.errors.OutOfRangeError:
        #except Exception as e:
            logging.info('train model done')
            #logging.info('Acui what error: %s'%str(e))
        finally:
            checkpoint_path = os.path.join('checkpoint_dir','Acuimodel')
            ret_prefix= saver.save(sess=sess, save_path=checkpoint_path, global_step=None)
            logging.info('ret_prefix:%s'%str(ret_prefix))
            logging.info('save checkpoint done')

    # from checkpoint convert to tensorflow frozened pb
    with tf.Session() as sess:
        checkpoint_path = tf.train.latest_checkpoint('checkpoint_dir')
        logging.info('latest_checkpoint:%s'%str(checkpoint_path))
        saver.restore(sess=sess, save_path=checkpoint_path)
        graph_name = 'Acui_frozened.pb'
        output_graph = tf.graph_util.convert_variables_to_constants(sess, input_graph_def=sess.graph_def, output_node_names=['Acui_output'])
        ret_path = tf.train.write_graph(graph_or_graph_def=output_graph,logdir='checkpoint_dir', name=graph_name, as_text=False)
        logging.info('ret_pbmodel_path:%s'%str(ret_path))
        logging.info('save frozen pb model done')

if __name__ == '__main__':
    train_model()
    pass
