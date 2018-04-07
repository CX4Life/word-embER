import zipfile
import json
import numpy as np
import tensorflow as tf
from os import path
from tf_args import parse_args

__author__ = 'Tim Woods'
__copyright__ = 'Copyright (c) 2018, Tim Woods'

INPUT_ZIP = 'dicts.zip'
RANKS_FILE = 'bag_of_ranks.json'


def select_optimizer(optimizer_string):
    optimizer_lookup = {
        'SGD': tf.train.GradientDescentOptimizer,
        'Adam': tf.train.AdamOptimizer
    }
    return optimizer_lookup[optimizer_string]


def load_training_set():
    """ Returns complete numpy array of continuous word ranks created from narratives.
        Extracts files from dicts.zip if not already extracted.
    """
    if not path.isfile(RANKS_FILE):
        with zipfile.ZipFile(INPUT_ZIP, 'r') as open_zip:
            open_zip.extractall()

    with open(RANKS_FILE, 'r') as bag_of_ranks:
        np_ranks = np.array(
            json.load(bag_of_ranks)
        )

    return np_ranks


def create_batch(np_ranks, **kwargs):
    pass


def build_graph(validation_samples, args):
    graph = tf.Graph()
    with graph.as_default():
        train_inputs = tf.placeholder(tf.int32, shape=[args.mb])
        train_labels = tf.placeholder(tf.int32, shape=[args.mb, 1])
        validation_set = tf.constant(validation_samples, dtype=tf.int32)
        embeddings = tf.Variable(
            tf.random_uniform([args.dict_size, args.dim], -1.0, 1.0)
        )
        embed = tf.nn.embedding_lookup(embeddings, train_inputs)

        nce_weights = tf.Variable(
            tf.truncated_normal(
                [args.dict_size, args.dim],
                stddev=1.0 / np.sqrt(args.dim)
            )
        )
        nce_biases = tf.Variable(tf.zeros([args.dict_size]))

        loss = tf.nn.nce_loss(
            weights=nce_weights,
            biases=nce_biases,
            labels=train_labels,
            inputs=embed,
            num_sampled=args.neg_samp,
            num_classes=args.dict_size
        )

        opt = select_optimizer(args.opt)(args.lr).minimize(loss)

        init = tf.global_variables_initializer()
        saver = tf.train.Saver()

    return graph


def run(cbor, graph, args):
    with tf.Session(graph=graph) as sess:
        init.run()

        for epoch in range(args.epochs):
            pass


def main():
    args = parse_args()
    cbor = load_training_set()
    print(cbor)


if __name__ == '__main__':
    main()
