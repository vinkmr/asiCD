from tensorflow.keras.preprocessing.image import ImageDataGenerator


def get_dataset_dict(dataset_path, file_ext=".png"):
    dataset_dict = {
        "train": [list((dataset_path/"train").glob("**/*" + file_ext)),
                  list((dataset_path/"train_labels").glob("**/*" + file_ext))],
        "test":  [list((dataset_path/"test").glob("**/*" + file_ext)),
                  list((dataset_path/"test_labels").glob("**/*" + file_ext))],
        "val":   [list((dataset_path/"val").glob("**/*" + file_ext)),
                  list((dataset_path/"val_labels").glob("**/*" + file_ext))]
    }
    return dataset_dict


def check_dataset(dataset_dict):

    img_file_names = []
    lablel_file_names = []

    def flatten(t): return [item for sublist in t for item in sublist]

    for i, data_split in enumerate(["train", "test", "val"]):
        img_num, label_num = map(len, dataset_dict[data_split])

        img_file_names.append(dataset_dict[data_split][0])
        lablel_file_names.append(dataset_dict[data_split][1])

        print(f"{data_split} has {img_num} images and {label_num} labels")
        if img_num != label_num:
            print(f"{data_split} has missing values")
            return False

    img_file_names = [file.stem for file in flatten(img_file_names)]
    lablel_file_names = [file.stem for file in flatten(lablel_file_names)]

    # REFACTOR
    name_match = []
    for img_file, label_name in zip(img_file_names, lablel_file_names):
        if img_file != label_name:
            name_match.append(False)
        else:
            name_match.append(True)

    # print(name_match)
    if all(name_match):
        # Not sure if working
        print("Dataset is consistent (by count and filename)")
    else:
        print("Dataset is consistent by count, but inconsistant by filename")

    return True


def get_img_mask_generators(dataset_path, aug_config, SEED=1,
                            labels_path_mod="_labels",
                            img_preprocessor=None,
                            mask_preprocessor=None):
    """
    docstring
    """
    print(f"From {dataset_path}")
    image_datagen = ImageDataGenerator(rescale=1./255,
                                       preprocessing_function=img_preprocessor)
    mask_datagen = ImageDataGenerator(rescale=1./255,
                                      preprocessing_function=mask_preprocessor)

    image_generator = image_datagen.flow_from_directory(dataset_path,
                                                        target_size=aug_config["target_size"],
                                                        color_mode="rgb",
                                                        class_mode=None,
                                                        seed=SEED)

    mask_generator = mask_datagen.flow_from_directory(dataset_path + labels_path_mod,
                                                      target_size=aug_config["target_size"],
                                                      color_mode="grayscale",
                                                      class_mode=None,
                                                      seed=SEED)

    # combine generators into one which yields image and masks
    date_generator = zip(image_generator, mask_generator)

    return date_generator
