import matplotlib.pyplot as plt
from pathlib import Path
import argparse


# Local Moduels
from asiCD.asiCD_utils import img_from_file
from asiCD.asiCD_utils import load_json
from asiCD.dist_remove import undistort
from asiCD.sun_remove import sun_remover_v1
from asiCD.sun_remove import sun_remover_v2
# from asiCD.sun_remove import sun_remover_v3


def img_preprocess(img_files, img_id, config, args):
    """Returns imgages in each step of preprocessing

    Args:
        img_files (list): List of image file paths
        img_id (int): Image id
        config (dict): Config dict
        args (dict): Passed arguments dict

    Returns:
        numpy.array: Original Image array
        numpy.array: Undistorted Image array
        numpy.array: Undistorted Image array with sun removed (v1)
        numpy.array: Undistorted Image array with sun removed (v2)
    """

    # Load image
    img_orig = img_from_file(str(img_files[img_id]))

    # Remove distortion
    img_undist = undistort(img_orig.copy(), config["undistort"])

    # Remove sun from image
    img_sun_v1 = sun_remover_v1(img_undist.copy(), args, fill=True)
    img_sun_v2 = sun_remover_v2(img_undist.copy(), args)

    return img_orig, img_undist, img_sun_v1, img_sun_v2


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
    img_files = list(Path("dataset/asi").glob("**/*.jpg"))
    config = load_json("config.json")

    # img, img_u, img_s_v1, img_s_v2 = img_preprocess(img_files,
    #                                                 img_id=args["image_id"],
    #                                                 config=config,
    #                                                 args=args)

    img_picks = [0, 50, 23,  9]
    num_rows = len(img_picks)
    fig_counter = 0
    plt.figure(figsize=(12, 12))

    for img_id in img_picks:

        img, img_u, img_s_v1, img_s_v2 = img_preprocess(img_files,
                                                        img_id=img_id,
                                                        config=config,
                                                        args=args)

        # Showing results
        plt.subplot(num_rows, 4, fig_counter+1)
        plt.title("Original image")
        plt.imshow(img)
        plt.axis("off")

        plt.subplot(num_rows, 4, fig_counter+2)
        plt.title("Undistored image")
        plt.imshow(img_u)
        plt.axis("off")

        plt.subplot(num_rows, 4, fig_counter+3)
        plt.title("sun_remover_v1")
        plt.imshow(img_s_v1)
        plt.axis("off")

        plt.subplot(num_rows, 4, fig_counter+4)
        plt.title("sun_remover_v2")
        plt.imshow(img_s_v2)
        plt.axis("off")

        plt.tight_layout()
        fig_counter += 4

    # plt.savefig("./preprocess-example.png")
    plt.show()

    return None


if __name__ == "__main__":
    main()
