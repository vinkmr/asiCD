import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import argparse
import numpy as np
import imutils

# Local Moduels
from asiCD.asiCD_utils import img_from_file
from asiCD.decorators import timef


@timef
def sun_remover_v1(img_arr, args, fill=True):

    if fill is True:
        fill = -1
    else:
        fill = 2

    # https://www.pyimagesearch.com/2014/09/29/finding-brightest-spot-image-using-python-opencv/
    # Convert image to grayscale adnd apply Gaussian blur
    gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # Find the brightest region
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(blurred)

    if maxVal >= args["low_thres"]:
        img_arr = cv2.circle(img_arr.copy(), maxLoc, args["radius"],
                             (0, 0, 0), thickness=fill)

    return img_arr


@timef
def sun_remover_v2(img_arr, args, fill=True):
    # https://www.pyimagesearch.com/2016/10/31/detecting-multiple-bright-spots-in-an-image-with-python-and-opencv/

    if fill is True:
        fill = -1
    else:
        fill = 2

    # Convert image to grayscale adnd apply Gaussian blur
    gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # Find the brightest region
    thresh = cv2.threshold(blurred,
                           args["low_thres"], 255, cv2.THRESH_BINARY)[1]

    if thresh.any():
        retval_erode = cv2.getStructuringElement(shape=cv2.MORPH_RECT,
                                                 ksize=(9, 9))
        retval_dilate = cv2.getStructuringElement(shape=cv2.MORPH_RECT,
                                                  ksize=(9, 9))

        thresh = cv2.erode(src=thresh, kernel=retval_erode, iterations=3)
        thresh = cv2.dilate(src=thresh, kernel=retval_dilate, iterations=4)

    # Applying mask v1
    mask = cv2.bitwise_not(thresh)
    output = cv2.bitwise_and(img_arr, img_arr, mask=mask)

    # Applyting mask v2
    # mask = cv2.bitwise_not(thresh)
    # print(np.max(mask))
    # print(np.min(mask))

    # output = np.zeros(img_arr.shape)
    # output[..., 0] = img_arr[..., 0] * mask / 255
    # output[..., 1] = img_arr[..., 1] * mask / 255
    # output[..., 2] = img_arr[..., 2] * mask / 255

    return output


@timef
def sun_remover_v3(img_arr, args, fill=True):
    # https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/

    if fill is True:
        fill = -1
    else:
        fill = 2

    # Convert image to grayscale adnd apply Gaussian blur
    gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # Find the brightest region
    thresh = cv2.threshold(blurred,
                           args["low_thres"], 255, cv2.THRESH_BINARY)[1]

    if thresh.any():
        retval_erode = cv2.getStructuringElement(shape=cv2.MORPH_RECT,
                                                 ksize=(9, 9))
        retval_dilate = cv2.getStructuringElement(shape=cv2.MORPH_RECT,
                                                  ksize=(9, 9))

        thresh = cv2.erode(src=thresh, kernel=retval_erode, iterations=3)
        thresh = cv2.dilate(src=thresh, kernel=retval_dilate, iterations=4)

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(),
                            cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # draw the contour and center of the shape on the image
        cv2.drawContours(img_arr, [c], -1, (0, 255, 0), 2)
        cv2.circle(img_arr, (cX, cY), 7, (255, 255, 255), -1)

    return img_arr


def main():

    # construct the argument parse and parse the arguments

    ap = argparse.ArgumentParser(
        description='Detect and encircle the sun for a provided image')
    ap.add_argument("-i", "--image_id", type=int, default=0,
                    help="index of image file")
    ap.add_argument("-r", "--radius", type=int, default=100,
                    help="radius of sun circle for sun_remover_v1")
    ap.add_argument("-t", "--low_thres", type=int, default=253,
                    help="lower thershold for sun_remover_v2")
    args = vars(ap.parse_args())

    # Fetch image
    img_files = list(Path("outputs").glob("**/*.jpg"))
    img_arr = img_from_file(str(img_files[args["image_id"]]))

    # Remove sun from image
    img_arr_v1 = sun_remover_v1(img_arr, args, fill=False)
    img_arr_v2 = sun_remover_v2(img_arr, args)

    # Showing results
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("sun_remover_v1")
    plt.imshow(img_arr_v1)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("sun_remover_v2")
    plt.imshow(img_arr_v2)
    plt.axis("off")

    plt.show()

    return None


if __name__ == "__main__":
    main()
