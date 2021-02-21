import cv2
import numpy as np
from datetime import date, datetime
from pathlib import Path
from json import load as json_load


def load_json(json_file):
    """Returns a dict containing information read from a JSON file

    Args:
        json_file (str): Path of JSON file

    Returns:
        dict: Information from the JSON file
    """
    with open(json_file, 'r') as json_file:
        file_dict = json_load(json_file)

    return file_dict


def img_from_file(img_file_inst, load_grey=False, load_rgb=False):
    if load_grey:
        img = cv2.imread(str(img_file_inst), cv2.IMREAD_GRAYSCALE)
        img = np.expand_dims(img, axis=-1)
    elif load_rgb:
        img = cv2.imread(str(img_file_inst), cv2.IMREAD_UNCHANGED)
    else:
        img = cv2.imread(str(img_file_inst), cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img


def img_save_to_path(img_path):

    cv2.imwrite(str(img_path), cv2.IMREAD_UNCHANGED)

    return None


def get_timestamp():
    now_d = datetime.now().date()
    now_t = datetime.now().time()
    timestamp = f"{now_d}-{now_t.hour}-{now_t.minute}"
    # timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    return timestamp


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

    # TODO refactor using Path.mkdir(parents=True) for multiple

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
