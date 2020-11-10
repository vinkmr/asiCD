from pathlib import Path
from utilities import read_json, get_dataset_dict


config = read_json("config.json")
dataset_path = Path.cwd().parent / config["dataset_path"]


dataset_dict = get_dataset_dict(dataset_path)
print("train size:\t", len(dataset_dict["train"][0]))
print("test size:\t", len(dataset_dict["test"][0]))
print("valid size:\t", len(dataset_dict["val"][0]))
