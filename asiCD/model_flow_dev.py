# import tensorflow as tf
from typing import Counter
import matplotlib.pyplot as plt
import tensorflow


from asiCD import asiCD_utils
from asiCD.model_utils import get_img_mask_generators


config = asiCD_utils.load_json("config.json")
# print(config)

dataset_path = config["dataset_path"]
AUG_CONFIG = config["aug_config"]


data_gen = get_img_mask_generators(dataset_path=dataset_path+"/train",
                                   aug_config=AUG_CONFIG)


num_img = 5
count = 0
for img_arr, mask_arr in data_gen:

    if count < num_img*2:

        img = img_arr[1]
        mask = mask_arr[1]

        plt.subplot(num_img, 2, count+1)
        plt.title(f"Image: {img.shape}")
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])

        plt.subplot(num_img, 2, count+2)
        plt.title(f"Mask: {mask.shape}")
        plt.imshow(mask[:, :, 0])
        plt.xticks([])
        plt.yticks([])

        count += 2
    else:
        break


plt.show()
