import matplotlib.pyplot as plt
from pathlib import Path
import argparse


# Local Moduels
from asiCD.asiCD_utils import img_from_file
from asiCD.asiCD_utils import load_json
from asiCD.dist_remove import undistort
from asiCD.sun_remove import sun_remover_v1
from asiCD.sun_remove import sun_remover_v2


def main():

    # construct the argument parse and parse the arguments
    global args

    ap = argparse.ArgumentParser(
        description='Detect and encircle the sun for a provided image')
    ap.add_argument("-i", "--image_id", type=int, default=0,
                    help="index of image file")
    ap.add_argument("-r", "--radius", type=int, default=120,
                    help="radius of sun circle for sun_remover_v1")
    ap.add_argument("-t", "--thres_low", type=int, default=253,
                    help="lower thershold for sun_remover_v2")
    args = vars(ap.parse_args())

    # Fetch image

    img_files = list(Path("dataset/asi").glob("**/*.jpg"))
    img_arr = img_from_file(str(img_files[args["image_id"]]))

    # Remove distortion
    config = load_json("camera_config.json")
    img_arr_undist = undistort(img_arr, config)

    # Remove sun from image
    img_arr_v1 = sun_remover_v1(img_arr_undist, args, fill_mode=-1)
    img_arr_v2 = sun_remover_v2(img_arr_undist, args)

    # Showing results
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 4, 1)
    plt.title("Original image")
    plt.imshow(img_arr)
    plt.axis("off")

    plt.subplot(1, 4, 2)
    plt.title("Undistored image")
    plt.imshow(img_arr_undist)
    plt.axis("off")

    plt.subplot(1, 4, 3)
    plt.title("sun_remover_v1")
    plt.imshow(img_arr_v1)
    plt.axis("off")

    plt.subplot(1, 4, 4)
    plt.title("sun_remover_v2")
    plt.imshow(img_arr_v2)
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    return None


if __name__ == "__main__":
    main()
