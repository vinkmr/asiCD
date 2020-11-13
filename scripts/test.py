from pathlib import Path
from utilities import read_json, get_dataset_dict, check_dataset


def main():
    config = read_json("config.json")
    dataset_path = Path(config["dataset_path"])
    dataset_dict = get_dataset_dict(dataset_path)

    try:
        check_dataset(dataset_dict)
    finally:
        return None


if __name__ == "__main__":
    main()
