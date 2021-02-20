"""Testing on-the-fly execution
"""
import matplotlib.pyplot as plt

from asiCD.model_utils import get_img_mask_generators
from asiCD.asiCD_utils import load_json


# Globals
DATASET_PATH = "dataset/RASID100/train/"
CONFIG = load_json("config.json")
INPUT_SIZE = tuple(CONFIG["model_config"]["input_size"])


def main(data_path, aug_config):
    train_generator = get_img_mask_generators(
        dataset_path=data_path,
        target_size=INPUT_SIZE)

    num_rows = 4
    count = 0
    plt.figure(figsize=(8, 6))
    for img_arr, mask_arr in train_generator:

        if count < num_rows*4:

            img = img_arr[1]
            mask = mask_arr[1]

            plt.subplot(num_rows, 4, count+1)
            plt.title(f"img_{count}")
            plt.imshow(img)
            plt.xticks([])
            plt.yticks([])

            plt.subplot(num_rows, 4, count+2)
            plt.title(f"mask_{count}")
            plt.imshow(mask[:, :, 0])
            plt.xticks([])
            plt.yticks([])

            count += 2
        else:
            break

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    main(DATASET_PATH, CONFIG)
