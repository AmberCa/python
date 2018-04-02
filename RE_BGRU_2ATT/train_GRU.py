import tensorflow as tf
import numpy as np
import time
import datetime
import os
import network
import utils as us
from tensorflow.contrib.tensorboard.plugins import projector

flags = tf.app.flags
FLAGS = tf.app.flags.FLAGS
#add by dbj
flags.DEFINE_string("model_path",    "model",      "Path to save model")
tf.app.flags.DEFINE_string('summary_dir', '.', 'path to store summary')


def main(_):
    #add by dbj
    #us.clean(FLAGS.model_path)
    # the path to save models
    save_path = './model/' + FLAGS.model_path + '/'

    print('reading wordembedding')
    wordembedding = np.load('./data/' + FLAGS.model_path + '/vec.npy')

    print('reading training data')
    train_y = np.load('./data/' + FLAGS.model_path + '/train_y.npy')
    train_word = np.load('./data/' + FLAGS.model_path + '/train_word.npy')
    train_pos1 = np.load('./data/' + FLAGS.model_path + '/train_pos1.npy')
    train_pos2 = np.load('./data/' + FLAGS.model_path + '/train_pos2.npy')

    settings = network.Settings()
    settings.num_classes = us.getClassNum(FLAGS.model_path)
    settings.vocab_size = len(wordembedding)
    settings.num_classes = len(train_y[0])

    big_num = settings.big_num

    with tf.Graph().as_default():

        sess = tf.Session()
        with sess.as_default():

            initializer = tf.contrib.layers.xavier_initializer()
            with tf.variable_scope("model", reuse=None, initializer=initializer):
                m = network.GRU(is_training=True, word_embeddings=wordembedding, settings=settings)
            global_step = tf.Variable(0, name="global_step", trainable=False)
            optimizer = tf.train.AdamOptimizer(0.0005)

            train_op = optimizer.minimize(m.final_loss, global_step=global_step)
            sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver(max_to_keep=None)
           
            merged_summary = tf.summary.merge_all()
            summary_writer = tf.summary.FileWriter(FLAGS.summary_dir + '/train_loss' + '/' + FLAGS.model_path, sess.graph)

            def train_step(word_batch, pos1_batch, pos2_batch, y_batch, big_num):

                feed_dict = {}
                total_shape = []
                total_num = 0
                total_word = []
                total_pos1 = []
                total_pos2 = []
                for i in range(len(word_batch)):
                    total_shape.append(total_num)
                    total_num += len(word_batch[i])
                    for word in word_batch[i]:
                        total_word.append(word)
                    for pos1 in pos1_batch[i]:
                        total_pos1.append(pos1)
                    for pos2 in pos2_batch[i]:
                        total_pos2.append(pos2)
                total_shape.append(total_num)
                total_shape = np.array(total_shape)
                total_word = np.array(total_word)
                total_pos1 = np.array(total_pos1)
                total_pos2 = np.array(total_pos2)

                feed_dict[m.total_shape] = total_shape
                feed_dict[m.input_word] = total_word
                feed_dict[m.input_pos1] = total_pos1
                feed_dict[m.input_pos2] = total_pos2
                feed_dict[m.input_y] = y_batch

                temp, step, loss, accuracy, summary, l2_loss, final_loss = sess.run(
                    [train_op, global_step, m.total_loss, m.accuracy, merged_summary, m.l2_loss, m.final_loss],
                    feed_dict)
                time_str = datetime.datetime.now().isoformat()
                accuracy = np.reshape(np.array(accuracy), (big_num))
                acc = np.mean(accuracy)
                summary_writer.add_summary(summary, step)
                #print("--------------step:%s"%step)
                if step % 50 == 0:
                    tempstr = "{}: step {}, softmax_loss {:g}, acc {:g}".format(time_str, step, loss, acc)
                    print(tempstr)
            print('settings.num_epochs----%s'%settings.num_epochs)
            for one_epoch in range(settings.num_epochs):
                #print('one_epoch------%s'%one_epoch)
                #print('len(train_word)------%s'%len(train_word))
                temp_order = list(range(len(train_word)))
                print('len(temp_order)------%s'%int(len(temp_order)))
                print('all_steps------', settings.num_epochs*(int(len(temp_order) / float(settings.big_num))))
                np.random.shuffle(temp_order)
                for i in range(int(len(temp_order) / float(settings.big_num))):
                    #print('i---------%s,int(len(temp_order) / float(settings.big_num))------%s'%(i, int(len(temp_order) / float(settings.big_num))))
                    temp_word = []
                    temp_pos1 = []
                    temp_pos2 = []
                    temp_y = []

                    temp_input = temp_order[i * settings.big_num:(i + 1) * settings.big_num]
                    for k in temp_input:
                        temp_word.append(train_word[k])
                        temp_pos1.append(train_pos1[k])
                        temp_pos2.append(train_pos2[k])
                        temp_y.append(train_y[k])
                    num = 0
                    for single_word in temp_word:
                        num += len(single_word)

                    if num > 1500:
                        print('out of range')
                        continue

                    temp_word = np.array(temp_word)
                    temp_pos1 = np.array(temp_pos1)
                    temp_pos2 = np.array(temp_pos2)
                    temp_y = np.array(temp_y)
                    #print('--------setting.bignum:%s,--------global_step:%s'%(settings.big_num, global_step))
                    train_step(temp_word, temp_pos1, temp_pos2, temp_y, settings.big_num)

                    current_step = tf.train.global_step(sess, global_step)
                    print("---------------------current_step:%s"%current_step)
                    if current_step >= 100  and current_step % 100 == 0:
                        print('saving model')
                        path = saver.save(sess, save_path + 'ATT_GRU_model')
                        tempstr = 'have saved model to ' + path
                        print(tempstr)


if __name__ == "__main__":
    tf.app.run()
