import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse


# Local Moduels
from asiCD.asiCD_utils import img_from_file


def sun_remover_v1(img_arr, args, fill=True):

    if fill == True:
        fill = -1
    else:
        fill = 2

    # https://www.pyimagesearch.com/2014/09/29/finding-brightest-spot-image-using-python-opencv/
    # Convert image to grayscale adnd apply Gaussian blur
    gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # Find the brightest region
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

    img_arr = cv2.circle(img_arr.copy(), maxLoc, args["radius"],
                         (0, 0, 0), fill)

    return img_arr


def sun_remover_v2(img_arr, args, fill=True):
    # https://www.pyimagesearch.com/2016/10/31/detecting-multiple-bright-spots-in-an-image-with-python-and-opencv/
    
    if fill == True:
            fill = -1
    else:
        fill = 2
        
    # Convert image to grayscale adnd apply Gaussian blur
    gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # Find the brightest region
    thresh = cv2.threshold(blurred,
                           args["thres_low"], 255, cv2.THRESH_BINARY_INV)[1]

    retval_erode = cv2.getStructuringElement(shape=cv2.MORPH_RECT,
                                             ksize=(9, 9))
    retval_dilate = cv2.getStructuringElement(shape=cv2.MORPH_RECT,
                                              ksize=(9, 9))

    thresh = cv2.erode(src=thresh, kernel=retval_erode, iterations=2)
    thresh = cv2.dilate(src=thresh, kernel=retval_dilate, iterations=4)

    return thresh


def main():

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser(
        description='Detect and encircle the sun for a provided image')
    ap.add_argument("-i", "--image_id", type=int, default=0,
                    help="index of image file")
    ap.add_argument("-r", "--radius", type=int, default=120,
                    help="radius of sun circle for sun_remover_v1")
    ap.add_argument("-t", "--thres_low", type=int, default=220,
                    help="lower thershold for sun_remover_v2")
    args = vars(ap.parse_args())

    # Fetch image
    img_files = list(Path("outputs").glob("**/*.jpg"))
    img_arr = img_from_file(str(img_files[args["image_id"]]))

    # Remove sun from image
    img_arr_v1 = sun_remover_v1(img_arr, args, fill=Ture)
    img_arr_v2 = sun_remover_v2(img_arr, args)

    # Showing results
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("sun_remover_v1")
    plt.imshow(img_arr_v1)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("sun_remover_v2")
    plt.imshow(img_arr_v2, cmap='magma')
    plt.axis("off")

    plt.show()

    return None


if __name__ == "__main__":
    main()
