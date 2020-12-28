from json import json_load


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
