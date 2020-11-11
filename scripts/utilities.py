from os import name, pipe
from pathlib import Path
import json
from operator import methodcaller


def read_json(json_path):
    with open(json_path, 'r') as json_file:
        file_str = json_file.read()
        file_dict = json.loads(file_str)

    return file_dict


def get_dataset_dict(dataset_path, file_ext=".png"):
    dataset_dict = {
        "train": [list((dataset_path/"train").glob("**/*" + file_ext)),
                  list((dataset_path/"train_labels").glob("**/*" + file_ext))],
        "test":  [list((dataset_path/"test").glob("**/*" + file_ext)),
                  list((dataset_path/"test_labels").glob("**/*" + file_ext))],
        "val":   [list((dataset_path/"val").glob("**/*" + file_ext)),
                  list((dataset_path/"val_labels").glob("**/*" + file_ext))]
    }
    return dataset_dict


def check_dataset(dataset_dict):

    img_file_names = []
    lablel_file_names = []

    def flatten(t): return [item for sublist in t for item in sublist]

    for i, data_split in enumerate(["train", "test", "val"]):
        img_num, label_num = map(len, dataset_dict[data_split])

        img_file_names.append(dataset_dict[data_split][0])
        lablel_file_names.append(dataset_dict[data_split][1])

        print(f"{data_split} has {img_num} images and {label_num} labels")
        if img_num != label_num:
            print(f"{data_split} has missing values")
            return False

    img_file_names = [file.stem for file in flatten(img_file_names)]
    lablel_file_names = [file.stem for file in flatten(lablel_file_names)]

    # REFACTOR
    name_match = []
    for img_file, label_name in zip(img_file_names, lablel_file_names):
        if img_file != label_name:
            name_match.append(False)
        else:
            name_match.append(True)

    # print(name_match)
    if all(name_match):
        # Not sure if working
        print("Dataset is consistent (by count and filename)")
    else:
        print("Dataset is consistent by count but inconsistant by filename")

    return True
