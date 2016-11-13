#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Creates corpus.npz from a full corpus stored as an SQLite database.

The file contains one-hot encoded matrices.
"""

import sys

import numpy as np
from tqdm import tqdm

from corpus import Corpus
from vectorize_tokens import vectorize_tokens
from vocabulary import vocabulary

if __name__ == '__main__':
    _, filename, size = sys.argv

    corpus = Corpus.connect_to(filename)
    n_files = len(corpus)
    n_vocab = len(vocabulary)
    dimensions = (n_files, maxlen, n_vocab)

    array = np.zero(dimensions, dtype=np.bool8)

    for i, tokens in enumerate(tqdm(corpus, total=len(corpus))):
        for t, index in enumerate(vectorize_tokens(tokens)):
            array[i, t, index] = 1
        del tokens

    np.save('corpus-bytearray', array)
