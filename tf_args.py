""" Generic argument parsing method for TensorFlow projects.
    Returns an object with the various fields listed below.

    Usage:
    from tf_args import parse_args

    args = parse_args()

    # access any field

    learning_rate = args.lr

    Tim Woods - 2018
"""
import argparse

__author__ = 'Tim Woods'
__copyright__ = 'Copyright (c) 2018, Tim Woods'


def parse_args():
    parser = argparse.ArgumentParser()

    # Hyper-parameters
    parser.add_argument('-lr', help='Learning rate', type=float, default=0.1)
    parser.add_argument('-mb', help='Mini-batch size (power of 2 is nice)', type=int, default=128)
    parser.add_argument('-epochs', help='Number of epochs to train', type=int, default=30)
    parser.add_argument('-opt', help='Which optimizer to use', type=str, default='SGD', choices=['SGD', 'Adam'])

    # Word embedding dimensions
    parser.add_argument('-dim', help='Dimension of word embedding', type=int, default=300)
    parser.add_argument('-dict_size', help='Size of embedding dictionary', type=int, default=10000)
    parser.add_argument('-window', help='Size of context window', type=int, default=3)
    parser.add_argument('-skips', help='Number of times to reuse input as label', type=int, default=2)
    parser.add_argument('-neg_samp', help='Number of negative sample for NCE', type=int, default=64)

    return parser.parse_args()
