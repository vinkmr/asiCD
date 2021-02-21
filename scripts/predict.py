from pathlib import Path
from tensorflow.keras.models import load_model

from asiCD.model_utils import get_img_mask_generators
from asiCD.asiCD_utils import load_json
from asiCD.asiCD_utils import img_save_to_path
from asiCD.asiCD_utils import get_timestamp


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

        # Making prediction
        print(f"Num of images: {len(data_g)}")

        for i in range(10):
            pred_img = model.predict((data_dict[data_g]).next(), step=1)
            print(type(pred_img))
            print(pred_img.shape)

            # Saving the prediction
            pred_path = f"{predict_out_path}/pred_{i}.png"
            img_save_to_path(pred_path, pred_img)

    return None


def main(data_path, model_path, output_path, config):

    INPUT_SIZE = tuple(config["model_config"]["input_size"])

    # Loading the data
    train_gen, test_gen, val_gen = load_data(data_path,
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

    DATASET_PATH = "dataset/RASID100/"
    MODEL_PATH = "outputs/model_out/2021-02-20-14-28/"
    OUTPUT_PATH = "outputs/postprocessing_out/" + get_timestamp()

    # Creating output path
    Path(OUTPUT_PATH).mkdir(parents=True)

    CONFIG = load_json("config.json")

    main(data_path=DATASET_PATH,
         model_path=MODEL_PATH,
         output_path=OUTPUT_PATH,
         config=CONFIG)