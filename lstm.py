import numpy as np
import tensorflow as tf
import constants

# 输入输出的张量维度[批量大小，信号长度，信号维度]
X = tf.placeholder(tf.float32, [None, None, constants.input_size])
Y = tf.placeholder(tf.float32, [None, None, constants.output_size])

# 权重和偏重
weights = {
    'in': tf.Variable(tf.random.normal([constants.input_size, constants.rnn_unit])),
    'out': tf.Variable(tf.random.normal([constants.rnn_unit, constants.output_size]))
}
biases = {
    'in': tf.Variable(tf.constant(0.1, shape=[constants.rnn_unit, ])),
    'out': tf.Variable(tf.constant(0.1, shape=[constants.output_size, ]))
}

class lstm:

    #初始化公共参数
    def init(self, time_step):
        global X, Y
        X = tf.placeholder(tf.float32, [None, time_step, constants.input_size])
        Y = tf.placeholder(tf.float32, [None, time_step, constants.output_size])

    #lstm网络结构
    def lstm(self, time_step):
        w_in = weights['in']
        b_in = biases['in']
        input = tf.reshape(X, [-1, constants.input_size])
        input_rnn = tf.matmul(input, w_in) + b_in
        input_rnn = tf.reshape(input_rnn, [-1, time_step, constants.rnn_unit])
        cell = tf.nn.rnn_cell.MultiRNNCell([tf.nn.rnn_cell.BasicLSTMCell(constants.rnn_unit) for i in range(constants.lstm_layers)])
        output_rnn, final_states = tf.nn.dynamic_rnn(cell, input_rnn, dtype=tf.float32)
        output = tf.reshape(output_rnn, [-1, constants.rnn_unit])
        w_out = weights['out']
        b_out = biases['out']
        pred = tf.matmul(output, w_out) + b_out
        return pred, final_states

    #训练lstm网络
    def train_lstm(self, train_x, train_y, scope_name, time_step, file_name):
        with tf.variable_scope(scope_name, reuse=tf.AUTO_REUSE):
            pred, _ = self.lstm(time_step)
            loss = tf.reduce_mean(tf.square(tf.reshape(pred, [-1]) - tf.reshape(Y, [-1])))
            train_op = tf.train.AdamOptimizer(constants.learning_rate).minimize(loss)
            saver = tf.train.Saver(tf.global_variables())
            loss_list = []
            with tf.Session() as sess:
                sess.run(tf.global_variables_initializer())

                for i in range(constants.iterations):
                    start = 0
                    end = start + constants.batch_size
                    loss_ = 0
                    while end < len(train_x):
                        _, loss_ = sess.run([train_op, loss], feed_dict={X: train_x[start:end], Y: train_y[start:end]})
                        start = start + constants.batch_size
                        end = end + constants.batch_size
                        if end >= len(train_x):
                            end = len(train_x)
                            _, loss_ = sess.run([train_op, loss], feed_dict={X: train_x[start:end], Y: train_y[start:end]})
                            break
                    loss_list.append(loss_)

                    if i%10==0:
                        print("Number of iterations:", i, " loss:", loss_list[-1])
                    if i > 0 and np.min(loss_list) == loss_list[-1]:
                        saver.save(sess, file_name)

                print("The train has finished")
                sess.close()

            return loss_list

    #预测输入结果
    def prediction(self, test_x, scope_name, time_step, file_name):
        with tf.variable_scope(scope_name, reuse=tf.AUTO_REUSE):
            pred, _ = self.lstm(time_step)
            saver = tf.train.Saver(tf.global_variables())

            test_predict = []
            with tf.Session() as sess:
                saver.restore(sess, file_name)

                for i in range(0, np.shape(test_x)[0]):
                    next_seq = sess.run(pred, feed_dict={X: [test_x[i]]})
                    test_predict.append(next_seq)
                sess.close()
            return  test_predict