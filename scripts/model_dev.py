from asiCD.asiCD_utils import load_json


from asiCD.models import model_vgg16
from asiCD.models import model_resnet18
from asiCD.models import model_densenet21
from asiCD.models import asiCD_mod1


def main(train_params):

    models = {"vgg16": model_vgg16,
              "resnet18": model_resnet18,
              "densenet21": model_densenet21,
              "asiCD_mod1": asiCD_mod1
              }

    model = models["asiCD_mod1"].MultiExpoNet.build(grid_h=train_params["input_size"][0],
                                                    grid_w=train_params["input_size"][1],
                                                    num_exp=train_params["num_exp"],
                                                    num_classes=train_params["num_classes"],
                                                    depth=train_params["num_channels"],
                                                    init_lr=train_params["lr"],
                                                    epochs=train_params["epochs"])

    model.summary()

    return None


if __name__ == "__main__":

    CONFIG = load_json("config.json")

    main(train_params=CONFIG["model_config"])
