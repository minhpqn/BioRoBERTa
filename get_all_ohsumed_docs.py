"""
Get all Ohsumed documents
"""
from data_utils import load_ohsumed_data


def dump_data(filename, texts):
    with open(filename, "w") as fo:
        for line in texts:
            print(line, file=fo)


texts, _ = load_ohsumed_data("./data/ohsumed/ohsumed-all")
dump_data("./data/ohsumed/ohsumed-all.txt", texts)