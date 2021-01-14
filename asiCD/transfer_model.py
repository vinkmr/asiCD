# * https://www.tensorflow.org/guide/keras/save_and_serialize#the_short_answer_to_saving_loading

from tensorflow.keras import backend as K
from tensorflow.keras import models
from tensorflow.keras import Model
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.optimizers import Adam, RMSprop, SGD


class some_transfer_model:
    def __init__(
        self,
        path_to_model_h5: str = "some_weights.h5",
        percentage_layers_trainable: int = 0.1,
        debug: bool = False,
    ):
        self.debug = debug
        self.path = path_to_model_h5
        self.percentage_layers_trainable = percentage_layers_trainable
        self.pretrained_model = models.load_model(self.path)
        self.new_model = self.freeze(
            percentage_layers_trainable=self.percentage_layers_trainable,
            prev_model=self.pretrained_model
        )

    def freeze(self,percentage_layers_trainable: int, prev_model: Model):

        num_trainable_layers = int(len(prev_model.layers) * percentage_layers_trainable)

        for layer in prev_model.layers[:num_trainable_layers]:
            layer.trainable = False
        return prev_model

    def download(self):
        model = self.new_model
        return model

    def build(self, optimizer: str = "Adam", lr_rate: float = 0.001):

        model = self.new_model

        K.clear_session()

        opt = {
            "Adam": Adam(lr=lr_rate),
            "RMSprop": RMSprop(lr=lr_rate),
            "SGD": SGD(lr_rate),
        }

        model.compile(
            loss=CategoricalCrossentropy(from_logits=True),
            optimizer=opt.get(optimizer),
            metrics=["accuracy"],
        )

        if self.debug:
            model.summary()
            print(
                "\n====================================================================\n"
            )
            print("\t\t\tNon-Trainable Layers\t\t\t")
            print(
                "\n====================================================================\n"
            )
            count = 0
            for layer in model.layers:
                if layer.trainable == False:
                    print(layer.name)
                    count += 1
            print()
            print(f"Total number of layers:\t{len(model.layers)}")
            print(f"Total number of non-trainable layers:\t{count}")

        return model


if __name__ == "__main__":

    trained_model = some_transfer_model(debug=True)
    trained_model.build()
