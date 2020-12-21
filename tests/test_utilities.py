from pathlib import Path
from scripts import utilities


def test_get_dataset_dict():
    test_path = Path("sample_path")
    dataset_dict = utilities.get_dataset_dict(test_path)
    assert(dataset_dict.keys() == {"train", "test", "val"})
