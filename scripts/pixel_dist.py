import argparse
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


# Local Moduels
from asiCD.asiCD_utils import img_from_file
from asiCD.asiCD_utils import load_json


def gen_flat_img(img_inst, ann_inst):

    img_flat = np.zeros([img_inst.shape[0]*img_inst.shape[1], 4])

    for i in range(4):
        if i == 3:
            img_flat[:, i] = ann_inst[:, :, 0].flatten()
        else:
            img_flat[:, i] = img_inst[:, :, i].flatten()

    return img_flat


def create_pixel_dist(img_files, ann_files):
    print(f"Image File: {img_files[0]}")
    print(f"Mask File: {ann_files[0]}")
    img_inst = img_from_file(img_files[96])/255
    ann_inst = img_from_file(ann_files[96], load_grey=True)/255

    img_flat = gen_flat_img(img_inst, ann_inst)

    # Pixels within masked area
    img_flat = img_flat[img_flat[:, 3] == 1]

    print(img_flat.shape)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.title("Green vs. Red")
    plt.scatter(x=img_flat[:, 0], y=img_flat[:, 1],
                c=img_flat[:, 0:3], alpha=0.1)

    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.xlabel("R")
    plt.ylabel("G")

    plt.subplot(1, 2, 2)
    plt.title("Blue vs. Red")
    plt.scatter(x=img_flat[:, 0], y=img_flat[:, 2],
                c=img_flat[:, 0:3], alpha=0.1)

    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.xlabel("R")
    plt.ylabel("B")

    plt.show()

    return None


def main():

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser(
        description='Detect and encircle the sun for a provided image')
    ap.add_argument("-i", "--image_id", type=int, default=0,
                    help="index of image file")
    ap.add_argument("-r", "--radius", type=int, default=120,
                    help="radius of sun circle for sun_remover_v1")
    ap.add_argument("-t", "--low_thres", type=int, default=253,
                    help="lower thershold for sun_remover_v2")
    args = vars(ap.parse_args())

    # Fetch image files
    img_files = list(Path("dataset/swimseg-2/train").glob("**/*.png"))
    ann_files = list(Path("dataset/swimseg-2/train_labels").glob("**/*.png"))
    config = load_json("config.json")

    print(f"Image Files: {len(img_files)}")
    print(f"Mask Files: {len(ann_files)}")

    create_pixel_dist(img_files, ann_files)

    return None


if __name__ == "__main__":
    main()
