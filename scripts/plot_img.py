import numpy as np
import matplotlib.pyplot as plt


def main(output_path):
    """
    docstring
    """
    model_name = "vgg16_last_w"
    data_split = "train"
    img_id = 0
    for i in range(10):
        img = np.load(output_path+"/"+model_name+"/" +
                      data_split+"/pred_"+str(i)+".png.npy")

        plt.imshow(img)
        plt.colorbar()
        plt.clim(1, 10)
        plt.axis("off")
        plt.show()

    return None


if __name__ == "__main__":

    OUTPUT_PATH = "outputs/postprocessing_out/" + "2021-02-20-17-5" + "/"

    main(output_path=OUTPUT_PATH)
