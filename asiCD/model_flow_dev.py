# import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import numpy as np

from asiCD import asiCD_utils
from asiCD.model_utils import get_img_mask_generators
from asiCD.dist_remove import undistort
from asiCD.sun_remove import sun_remover_v1
# from asiCD.sun_remove import sun_remover_v2
# from asiCD.sun_remove import sun_remover_v3


config = asiCD_utils.load_json("config.json")
# print(config)

dataset_path = config["dataset_path"]
AUG_CONFIG = config["aug_config"]


def img_pre(img_arr):
    """
    docstring
    """
    # Remove distortion
    img_buff = undistort(img_arr, config["undistort"])

    # Remove sun from image
    output = sun_remover_v1(img_buff, config["sun-remover"])

    print(f"img_pre: {output.shape}")
    # print(np.max(output))
    # print(np.min(output))

    return output


def mask_pre(image):
    """
    docstring
    """
    output = img_pre(image)

    # Applying thresholding, get cloud mask

    img_buff = output.copy()
    output[..., 0] = img_buff[..., 0]
    output[..., 1] = np.where(img_buff[..., 1] < 223, img_buff[..., 1], 0)
    output[..., 2] = np.where(img_buff[..., 2] < 223, img_buff[..., 2], 0)

    output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    output = cv2.GaussianBlur(output, (7, 7), 0)
    output = cv2.threshold(output,
                           config["thres"], 255, cv2.THRESH_BINARY)[1]

    print(f"mask_pre: {output.shape}")

    if len(output.shape) != 3:
        output = np.expand_dims(output, axis=-1)

    return output


data_gen = get_img_mask_generators(dataset_path=dataset_path,
                                   ann_path="",
                                   target_size=AUG_CONFIG,
                                   img_preprocessor=img_pre,
                                   mask_preprocessor=mask_pre)


num_rows = 4
count = 0
plt.figure(figsize=(8, 6))
for img_arr, mask_arr in data_gen:

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
