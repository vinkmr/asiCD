import json


def read_json(json_path):
    with open(json_path, 'r') as json_file:
        file_str = json_file.read()
        file_dict = json.loads(file_str)

    return file_dict


def get_dataset_dict(dataset_path):
    dataset_dict = {
        "train": [list((dataset_path/"train").glob("**/*.png")),
                  list((dataset_path/"train").glob("**/*.png"))],
        "test":  [list((dataset_path/"test").glob("**/*.png")),
                  list((dataset_path/"test").glob("**/*.png"))],
        "val":   [list((dataset_path/"val").glob("**/*.png")),
                  list((dataset_path/"val").glob("**/*.png"))]
    }
    return dataset_dict
