from pathlib import Path
import matplotlib.pyplot as plt

from asiCD.model_utils import get_img_mask_generators
from asiCD.asiCD_utils import load_json
from asiCD.asiCD_utils import get_timestamp

from asiCD.models import model_vgg16
from asiCD.models import model_resnet18
from asiCD.models import model_densenet21


def load_data(data_path, input_size):

    train_generator = get_img_mask_generators(
        dataset_path=data_path + "train/",
        target_size=input_size)

    test_generator = get_img_mask_generators(
        dataset_path=data_path + "test/",
        target_size=input_size)

    val_generator = get_img_mask_generators(
        dataset_path=data_path + "val/",
        target_size=input_size)

    return train_generator, test_generator, val_generator


def model_trainer(model, train_gen, test_gen, train_params):
    """
    docstring
    """
    model = model.MultiExpoNet.build(grid_h=train_params["input_size"][0],
                                     grid_w=train_params["input_size"][1],
                                     num_exp=train_params["num_exp"],
                                     num_classes=train_params["num_classes"],
                                     depth=train_params["num_channels"],
                                     init_lr=train_params["lr"],
                                     epochs=train_params["epochs"])

    model_hist = model.fit(train_gen,
                           epochs=train_params["epochs"],
                           batch_size=train_params["batch_size"],
                           validation_data=test_gen,
                           validation_steps=train_params["val_steps"],
                           steps_per_epoch=train_params["steps_per_epoch"])

    return model


def model_save_results(model, model_name, output_path):
    """
    docstring
    """

    model.save(f"{output_path}/{model_name}_last_w.h5")

    return None


def main(data_path, output_path, config):

    INPUT_SIZE = tuple(config["model_config"]["input_size"])

    # Loading the data
    train_gen, test_gen, val_gen = load_data(data_path,
                                             INPUT_SIZE)
    # Loading the models
    # models = [model_vgg16,
    #           model_resnet18,
    #           model_densenet21]
    # model_names = ["vgg16",
    #                "resnet18",
    #                "densenet21"]

    models_dict = {"vgg16": model_vgg16,
                   "resnet18": model_resnet18,
                   "densenet21": model_densenet21}

    for model_name in models_dict:
        model_t = model_trainer(model=models_dict[model_name],
                                train_gen=train_gen,
                                test_gen=test_gen,
                                train_params=config["model_config"])

        model_save_results(model=model_t,
                           model_name=model_name,
                           output_path=output_path)

    # call a funciton
    #   train with X params (import, build, train)
    #   save the weights, inside outputs/model_out/<timestamp>/weights

    return None


if __name__ == "__main__":

    DATASET_PATH = "dataset/RASID100/"
    OUTPUT_PATH = "outputs/model_out/" + get_timestamp()

    # Creating output path
    Path(OUTPUT_PATH).mkdir(parents=True)

    CONFIG = load_json("config.json")

    main(data_path=DATASET_PATH,
         output_path=OUTPUT_PATH,
         config=CONFIG)
