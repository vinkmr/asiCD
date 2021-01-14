"""
Returns VGG-16-like model, orignally intended for input size of 224x224x3.
FC (Dense) layers from VGG-16 are omitted for fully convolutional layers.
Using LeakyReLU instead of ReLU.
Using BatchNormalization (use_bias is thus set to False)
Number of kernels is scaled down by 8
Number of Dense units is scaled down by 64
"""

# import the necessary packages

from tensorflow.keras import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import Reshape
# from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.optimizers import Adam


class MultiExpoNet:
    def __init__(self, grid_h, grid_w, num_exp, num_classes, depth, init_lr, epochs):
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.num_exp = num_exp
        self.num_classes = num_classes
        self.depth = depth

        self.init_lr = init_lr
        self.epochs = epochs

    @staticmethod
    def denife_cnn(height, width, num_exposures, num_classes, depth=3):
        input_layer = Input(shape=(height, width, depth*num_exposures),
                            name="input_1")
        x = input_layer
        num_layer = 1

        # stack 1
        for i in range(0, 2):
            x = Conv2D(8, (3, 3), strides=(1, 1), padding='same',
                       name='conv_' + str(num_layer), use_bias=False)(x)
            x = BatchNormalization(name='norm_' + str(num_layer))(x)
            x = LeakyReLU(alpha=0.1)(x)
            num_layer += 1

        # x = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)

        print("stack 1")

        # stack 2
        for i in range(0, 2):
            x = Conv2D(16, (3, 3), strides=(1, 1), padding='same',
                       name='conv_' + str(num_layer), use_bias=False)(x)
            x = BatchNormalization(name='norm_' + str(num_layer))(x)
            x = LeakyReLU(alpha=0.1)(x)
            num_layer += 1

        # x = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)

        print("stack 2")

        # stack 3
        for i in range(0, 2):
            x = Conv2D(32, (3, 3), strides=(1, 1), padding='same',
                       name='conv_' + str(num_layer), use_bias=False)(x)
            x = BatchNormalization(name='norm_' + str(num_layer))(x)
            x = LeakyReLU(alpha=0.1)(x)
            num_layer += 1

        x = Conv2D(32, (1, 1), strides=(1, 1), padding='same',
                   name='conv_' + str(num_layer), use_bias=False)(x)
        x = BatchNormalization(name='norm_' + str(num_layer))(x)
        x = LeakyReLU(alpha=0.1)(x)
        num_layer += 1

        # x = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)
        print("stack 3")

        # stack 4
        for i in range(0, 2):
            x = Conv2D(64, (3, 3), strides=(1, 1), padding='same',
                       name='conv_' + str(num_layer), use_bias=False)(x)
            x = BatchNormalization(name='norm_' + str(num_layer))(x)
            x = LeakyReLU(alpha=0.1)(x)
            num_layer += 1

        x = Conv2D(64, (1, 1), strides=(1, 1), padding='same',
                   name='conv_' + str(num_layer), use_bias=False)(x)
        x = BatchNormalization(name='norm_' + str(num_layer))(x)
        x = LeakyReLU(alpha=0.1)(x)
        num_layer += 1

        # x = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)
        print("stack 4")

        # stack 5
        for i in range(0, 2):
            x = Conv2D(64, (3, 3), strides=(1, 1), padding='same',
                       name='conv_' + str(num_layer), use_bias=False)(x)
            x = BatchNormalization(name='norm_' + str(num_layer))(x)
            x = LeakyReLU(alpha=0.1)(x)
            num_layer += 1

        x = Conv2D(64, (1, 1), strides=(1, 1), padding='same',
                   name='conv_' + str(num_layer), use_bias=False)(x)
        x = BatchNormalization(name='norm_' + str(num_layer))(x)
        x = LeakyReLU(alpha=0.1)(x)
        num_layer += 1

        # x = MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)
        print("stack 5")

        # stack 6
        x = Conv2D(num_classes, (1, 1), strides=(1, 1), padding='same',
                   name='conv_' + str(num_layer), use_bias=False)(x)
        x = BatchNormalization(name='norm_' + str(num_layer))(x)
        x = LeakyReLU(alpha=0.1)(x)

        num_layer += 1
        print("stack 6")

        # Output Detection layer
        x = Conv2D(num_classes, (1, 1), strides=(1, 1),
                   padding='same', name='DetectionLayer', use_bias=False)(x)

        output_layer = Reshape((height, width, num_classes),
                               name="reshape_1")(x)

        return input_layer, output_layer

    @staticmethod
    def build(grid_h, grid_w, num_exp, num_classes, depth, init_lr, epochs):
        """Build model with CategoricalCrossentropy loss
        """
        input_l, output_l = MultiExpoNet.denife_cnn(height=grid_h,
                                                    width=grid_w,
                                                    num_exposures=num_exp,
                                                    num_classes=num_classes,
                                                    depth=depth)
        # Model Defenition
        model = Model(inputs=input_l, outputs=output_l,
                      name="cnn_model_" + str(num_exp) + "_exp")

        opt = Adam(lr=init_lr,
                   decay=init_lr / (epochs * 0.5))

        model.compile(loss=CategoricalCrossentropy(from_logits=True),
                      optimizer=opt,
                      metrics=["accuracy"])
        return model
