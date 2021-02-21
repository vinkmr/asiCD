import numpy as np
from pathlib import Path
from tensorflow.keras.models import load_model

from asiCD.model_utils import get_img_mask_generators
from asiCD.asiCD_utils import load_json
from asiCD.asiCD_utils import img_save_to_path
from asiCD.asiCD_utils import get_timestamp
from asiCD.img_postprocessing import apply_post_processing


def load_pred_data(data_path, input_size):

    train_gen_X, _ = get_img_mask_generators(
        dataset_path=data_path + "train/",
        target_size=input_size)

    test_gen_X, _ = get_img_mask_generators(
        dataset_path=data_path + "test/",
        target_size=input_size)

    val_gen_X, _ = get_img_mask_generators(
        dataset_path=data_path + "val/",
        target_size=input_size)

    return train_gen_X, test_gen_X, val_gen_X


def model_loader(model_path):
    """
    docstring
    """
    models_paths = list(Path(model_path).glob("**/*.h5"))

    loaded_models = {}
    for model_path in models_paths:
        loaded_models[model_path.stem] = load_model(str(model_path))

    return loaded_models


def model_predictor(model, model_name, data_dict, output_path):
    """
    Predicts based on loaded model on data, saves into output_path
    """

    for data_g in data_dict:
        # Creating output paths
        predict_out_path = f"{output_path}/{model_name}/{data_g}"
        Path(predict_out_path).mkdir(parents=True)

        # Making predictions
        print(f"Num of images: {len(data_g)}")

        for i in range(10):
            pred_img = model.predict((data_dict[data_g]).next(),
                                     batch_size=1)

            # Applying post-processing
            img_post = apply_post_processing(pred_img[0, :, :, 0])

            # Saving the prediction
            pred_path = f"{predict_out_path}/pred_{i}.png"
            img_save_to_path(pred_path, img_post)

            # Saving to npy
            np.save(pred_path, img_post)

    return None


def main(data_path, model_path, output_path, config):

    INPUT_SIZE = tuple(config["model_config"]["input_size"])

    # Loading the data
    train_gen, test_gen, val_gen = load_pred_data(data_path,
                                                  INPUT_SIZE)

    data_gens = {"train": train_gen,
                 "test": test_gen,
                 "val": val_gen}

    # Load the models
    models_dict = model_loader(model_path)

    # Run Inference, save image
    for model_name in models_dict:
        model_predictor(model=models_dict[model_name],
                        model_name=model_name,
                        data_dict=data_gens,
                        output_path=output_path)

    return None


if __name__ == "__main__":

    # DATASET_PATH = "dataset/RASID100/"
    DATASET_PATH = "dataset/swimseg-asiCD/"
    # MODEL_PATH = "outputs/model_out/2021-02-20-14-28/"
    MODEL_PATH = "outputs/model_out/2021-02-20-17-5/"
    OUTPUT_PATH = "outputs/postprocessing_out/" + get_timestamp()

    # Creating output path
    Path(OUTPUT_PATH).mkdir(parents=True)

    CONFIG = load_json("config.json")

    main(data_path=DATASET_PATH,
         model_path=MODEL_PATH,
         output_path=OUTPUT_PATH,
         config=CONFIG)
