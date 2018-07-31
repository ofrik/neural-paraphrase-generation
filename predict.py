import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import logging
import tensorflow as tf
from seq2seq import Seq2seq
from data_handler_test import Data

FLAGS = tf.flags.FLAGS

# Model related
tf.flags.DEFINE_integer('num_units', 256, 'Number of units in a LSTM cell')
tf.flags.DEFINE_integer('embed_dim', 256, 'Size of the embedding vector')

# Training related
tf.flags.DEFINE_float('learning_rate', 0.001, 'learning rate for the optimizer')
tf.flags.DEFINE_string('optimizer', 'Adam', 'Name of the train source file')
tf.flags.DEFINE_integer('batch_size', 32, 'random seed for training sampling')
tf.flags.DEFINE_integer('print_every', 100, 'print records every n iteration')
tf.flags.DEFINE_integer('iterations', 10000, 'number of iterations to train')
tf.flags.DEFINE_string('model_dir', 'checkpoints', 'Directory where to save the model')

tf.flags.DEFINE_integer('input_max_length', 30, 'Max length of input sequence to use')
tf.flags.DEFINE_integer('output_max_length', 30, 'Max length of output sequence to use')

tf.flags.DEFINE_bool('use_residual_lstm', True, 'To use the residual connection with the residual LSTM')

# Data related
tf.flags.DEFINE_string('input_filename', 'data/test_source.txt', 'Name of the train source file')
tf.flags.DEFINE_string('vocab_filename', 'data/train_vocab.txt', 'Name of the vocab file')


def main(args):
    tf.logging._logger.setLevel(logging.INFO)

    data = Data(FLAGS)
    model = Seq2seq(data.vocab_size, FLAGS)

    input_fn, feed_fn = data.make_input_fn()
    print_inputs = tf.train.LoggingTensorHook(['source', 'predict'], every_n_iter=1,
                                              formatter=data.get_formatter(['source', 'predict']))

    estimator = tf.estimator.Estimator(model_fn=model.make_graph, model_dir=FLAGS.model_dir, params=FLAGS)

    def get_vocabulary(fn):
        f = open(fn, 'r')
        return f.read().splitlines()

    vocab = get_vocabulary(FLAGS.vocab_filename)
    rslt = estimator.predict(input_fn=input_fn, hooks=[tf.train.FeedFnHook(feed_fn), print_inputs])
    for k in rslt:
        pass
        # print(" ".join([vocab[i] for i in k if vocab[i] not in ["<S>","</S>"]]))


if __name__ == "__main__":
    tf.app.run()
