import numpy as np
from cv2 import cv2
from pathlib import Path

# Local Modules
from asiCD.asiCD_utils import load_json
from asiCD.decorators import timef


@timef
def undistort(img_arr, camera_config):
    DIM = tuple(camera_config["DIM"])
    K = np.asarray(camera_config["K"])
    D = np.asarray(camera_config["D"])

    h, w = img_arr.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3),
                                                     K,
                                                     DIM,
                                                     cv2.CV_16SC2)
    undistorted_img = cv2.remap(img_arr, map1, map2,
                                interpolation=cv2.INTER_LINEAR,
                                borderMode=cv2.BORDER_CONSTANT)

    return undistorted_img


if __name__ == '__main__':

    images = list(Path("dataset/asi").glob("**/*.jpg"))
    config = load_json("config.json")["undistort"]

    for img_file in images:
        img = cv2.imread(str(img_file))
        img_undist = undistort(img, config)
        cv2.imwrite("outputs/"+img_file.stem + ".jpg", img_undist)
