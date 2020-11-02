# %% Dependencies
import argparse
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import os
import json
# import tensorflow as tf
# import imageio
# import polarTransform as pt

argparser = argparse.ArgumentParser(description = "Preprocess images from the dataset folder")
argparser.add_argument("-c", "--config", help="path to configuration file")

# %% Image transformation squareCrop
def square_crop(imageLoc: str, amount: int):
    """
    Crops the provided image by 'amount' pixels.
    Writes the croped image to the cropped images folder.
    Args:
        imageLoc (str): relative path to location of image

    Returns:
        [np.array]: [returns the cropped image as a numpy array]
    """
    imageLoc = imageLoc
    amount = amount
    img = cv.imread(imageLoc)
    # cv.imshow("image", img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    x, y, depth = np.shape(img)
    r = int((max(x, y) - amount) / 2)
    x = int(x / 2)
    y = int(y / 2)

    cv.circle(img, (x, y), r, (0, 0, 0), 2)
    crpdimg = img[x - r : x + r, y - r : y + r]

    # for debugging
    # cv.imshow("image", crpdimg)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # cv.imwrite("./dataset/cropped/croppedImage.jpg", crpdimg)
    return (crpdimg, r)


# %% Image transformation CircularCrop by applying mask


def apply_circular_mask(sq_image, radius:int):
    """
    [Apply a circular mask to a provided image.]
    Args:
        sq_image ([np.array]): [A previously cropped image obtained by calling the function square_crop()]
        radius ([int]): [radius of the circular mask to applied]

    Returns:
        img1_bg ([np.array]): [Returns a numpy array representing the image with a circular mask crop applied]
    """
    r = radius
    img1 = sq_image  # true image
    # create an arrray of zeros with same shape as true image, i.e. black image of same shape as true image
    img2 = np.zeros_like(sq_image)

    # draw a white circle with radius 'r' == cropping radius, onto 
    img2 = cv.circle(img2, (r, r), r, (255, 255, 255), -1)
    rows, cols, channels = img1.shape
    roi = img1[0:rows, 0:cols]
    img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
    mask_inv = cv.bitwise_not(mask)

    img1_bg = cv.bitwise_and(roi, roi, mask=mask)

    # for debugging
    # cv.startWindowThread()
    # cv.namedWindow("img1_bg", cv.WINDOW_NORMAL)
    # cv.imshow("img1_bg", img1_bg)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    
    return img1_bg


# Center coordinates and radius of circle
# x = int(1920/2)
# y = int(1920/2)
# r = int(1600/2)
# crpdimgCopy = crpdimg
    
# # circular mask of the radius 'r'
# # pixels outside the circle will be set to black
# mask = np.zeros_like(crpdimgCopy)
# cv.imshow('CorrectImage',mask)
# cv.waitKey(0)
# cv.destroyAllWindows
# mask = cv.circle(mask,(r,r),r,(255,255,255),-1)

# ret, mask = cv.threshold(mask, 10, 255, cv.THRESH_BINARY)

# mask_inv = cv.bitwise_not(mask)

# cv.imshow('CorrectImage',mask)
# cv.waitKey(0)
# cv.destroyAllWindows

# roi = crpdimg

# img1_bg = cv.bitwise_and(roi,roi,mask = mask_inv)
# img2_fg = cv.bitwise_and(mask,mask,mask = mask)

# dst = cv.add(img1_bg,img2_fg)
# crpdimgCopy =dst

# cv.imshow('CorrectImage',crpdimgCopy)
# cv.waitKey(0)
# cv.destroyAllWindows


# %% Main Block


def _main_(args):
    config_path = args.config

    with open(config_path) as config_buffer:
        config = json.load(config_buffer)
    print("Main method called")
    img_cropped, radius = square_crop(".\dataset\\20190701045440_11.jpg", config["preprocess"]["crop_px"])
    img_masked = apply_circular_mask(img_cropped, radius)
    cv.imwrite("./dataset/cropped/circularCroppedImage.jpg", img_masked)

if __name__== "__main__":
    args = argparser.parse_args()
    
    #default arguments
    args.conf = "config.json"
    _main_(args)
# %%
