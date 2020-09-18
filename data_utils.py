"""
Utility function for data loading and processing
"""
import re
import numpy as np
import os
from nltk import word_tokenize


def load_ohsumed_data(path, lower_case=False, tokenize=False):
    """Load Ohsumed data from the directory path
    
    :param path: Path to data
    :return:
        texts: list of texts
        labels: list of labels
    """
    texts = []
    labels = []
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    for dirname in dirs:
        dirpath = os.path.join(path, dirname)
        filenames = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f)) and not re.search(r'\._', f)]
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            lines = []
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line == "": continue;
                    lines.append(line)
            text = " ".join(lines)
            if tokenize:
                text = " ".join(word_tokenize(text))
            if lower_case:
                text = text.lower()
            texts.append(text)
            labels.append(dirname)
    return texts, labels


def label2index(_train_labels, _test_labels):
    label2id = {}
    id2label = {}
    sorted_labels = sorted(np.unique(_train_labels).tolist())
    for i,lb in enumerate(sorted_labels):
        label2id[lb] = i
        id2label[i] = lb
    train_y = [label2id[lb] for lb in _train_labels]
    test_y = [label2id[lb] for lb in _test_labels]
    return train_y, test_y, label2id, id2label
