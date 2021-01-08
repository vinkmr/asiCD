import numpy as np
from datetime import datetime
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
from pathlib import Path
# from operator import methodcaller


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
        print("Dataset is consistent by count, but inconsistant by filename")

    return True


def get_img_mask_generators(dataset_path, aug_config, SEED=1):
    """
    docstring
    """
    print(f"From {dataset_path}")
    image_datagen = ImageDataGenerator(rescale=1./255)
    mask_datagen = ImageDataGenerator(rescale=1./255)

    image_generator = image_datagen.flow_from_directory(dataset_path,
                                                        target_size=aug_config["target_size"],
                                                        color_mode="rgb",
                                                        class_mode=None,
                                                        seed=SEED)

    mask_generator = mask_datagen.flow_from_directory(dataset_path + "_labels",
                                                      target_size=aug_config["target_size"],
                                                      color_mode="grayscale",
                                                      class_mode=None,
                                                      seed=SEED)

    # combine generators into one which yields image and masks
    train_generator = zip(image_generator, mask_generator)

    return train_generator


def get_timestamp():
    now_d = datetime.now().date()
    now_t = datetime.now().time()
    timestamp = f"{now_d}-{now_t.hour}-{now_t.minute}"
    # timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    return timestamp


def load_npy(npy_file):
    npy_arr = np.load(npy_file)

    return npy_arr


def create_output_dir():
    """Create an output directory in the current working directory
    """
    output_dir = Path("output")

    if output_dir.is_dir():
        print("output folder exists")
    else:
        print("output folder created")
        output_dir.mkdir()

    return None


def create_dataset_dir(output_dir):
    """Create train, test and  validation directories
    """
    timestamp = get_timestamp()
    folder_split = f"{output_dir}/{timestamp}"
    Path(folder_split).mkdir()

    # Test
    Path(f"{folder_split}/test").mkdir()
    Path(f"{folder_split}/test/img").mkdir()

    Path(f"{folder_split}/test_labels").mkdir()
    Path(f"{folder_split}/test_labels/img").mkdir()

    # Train
    Path(f"{folder_split}/train").mkdir()
    Path(f"{folder_split}/train/img").mkdir()

    Path(f"{folder_split}/train_labels").mkdir()
    Path(f"{folder_split}/train_labels/img").mkdir()

    # Train
    Path(f"{folder_split}/val").mkdir()
    Path(f"{folder_split}/val/img").mkdir()

    Path(f"{folder_split}/val_labels").mkdir()
    Path(f"{folder_split}/val_labels/img").mkdir()

    return f"{output_dir}/{timestamp}"
