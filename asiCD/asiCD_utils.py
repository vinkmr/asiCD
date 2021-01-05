import cv2
from json import load as json_load


def load_json(json_file):
    """Returns a dict containing information read from a JSON file

    Args:
        json_file (str): Path of JSON file

    Returns:
        dict: Information from the JSON file
    """
    with open(json_file, 'r') as fp:
        file_dict = json_load(fp)

    return file_dict


def img_from_file(img_file_inst):
    img = cv2.imread(str(img_file_inst), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img
