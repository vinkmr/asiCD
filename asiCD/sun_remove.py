import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# Local Moduels
from asiCD.asiCD_utils import img_from_file


def main():
    img_files = list(Path("outputs").glob("**/*.jpg"))
    img_arr = img_from_file(str(img_files[0]))

    plt.imshow(img_arr)
    plt.show()

    return None


if __name__ == "__main__":
    main()
