"""
Prepare line by line from training part
"""
import os
from data_utils import load_ohsumed_data


def dump_data(filename, texts):
    with open(filename, "w") as fo:
        for line in texts:
            print(line, file=fo)


train_dir = "./data/ohsumed/ohsumed_single_23/training"
test_dir = "./data/ohsumed/ohsumed_single_23/test"
output_dir = "./data/ohsumed_within_task_pretraining"
os.makedirs(output_dir, exist_ok=True)

train_texts, _ = load_ohsumed_data(train_dir)
test_texts, _ = load_ohsumed_data(test_dir)

dump_data(os.path.join(output_dir, "train.txt"), train_texts)
dump_data(os.path.join(output_dir, "valid.txt"), test_texts)



