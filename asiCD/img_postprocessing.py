import cv2

# Local modules
from asiCD.asiCD_utils import load_json

# Globals
CONFIG = load_json("config.json")


def apply_post_processing(img_inst):

    # Normalizing
    norm_image = cv2.normalize(img_inst,
                               None,
                               alpha=0,
                               beta=1,
                               norm_type=cv2.NORM_MINMAX,
                               dtype=cv2.CV_32F)
    # Thresholding
    # Find the brightest region
    img_post = cv2.threshold(norm_image,
                             CONFIG["post-process"]["low_thres"],
                             CONFIG["post-process"]["high_thres"],
                             cv2.THRESH_BINARY)[1]

    return img_post
