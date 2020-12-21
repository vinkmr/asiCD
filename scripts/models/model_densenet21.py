"""
Add Doc for DenseNet
"""

# import the necessary packages

from tensorflow.keras import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.layers import Reshape
# from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Concatenate
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
    def dense_block(x_in, kernel_no, num_layer):
        # sub-block 1
        x_1 = x_in
        x = BatchNormalization(name='norm_' + str(num_layer))(x_1)
        x = LeakyReLU(alpha=0.1)(x)
        x = Conv2D(kernel_no, (1, 1), strides=(1, 1), padding='same',
                   name='conv_' + str(num_layer), use_bias=False)(x)
        num_layer += 1

        x = BatchNormalization(name='norm_' + str(num_layer))(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = Conv2D(kernel_no, (3, 3), strides=(1, 1), padding='same',
                   name='conv_' + str(num_layer), use_bias=False)(x)
        num_layer += 1

        # skip-line 1
        x_2 = Concatenate(axis=3)([x, x_1])

        # sub-block 2
        x = BatchNormalization(name='norm_' + str(num_layer))(x_2)
        x = LeakyReLU(alpha=0.1)(x)
        x = Conv2D(kernel_no, (1, 1), strides=(1, 1), padding='same',
                   name='conv_' + str(num_layer), use_bias=False)(x)
        num_layer += 1

        x = BatchNormalization(name='norm_' + str(num_layer))(x)
        x = LeakyReLU(alpha=0.1)(x)
        x = Conv2D(kernel_no, (3, 3), strides=(1, 1), padding='same',
                   name='conv_' + str(num_layer), use_bias=False)(x)
        num_layer += 1

        # skip-line 1
        x_3 = Concatenate(axis=3)([x, x_2, x_1])

        # transition layer
        x = BatchNormalization(name='norm_' + str(num_layer))(x_3)
        x_out = Conv2D(kernel_no, (1, 1), strides=(1, 1), padding='same',
                       name='conv_' + str(num_layer), use_bias=False)(x)

        num_layer += 1

        return x_out, num_layer

    @staticmethod
    def denife_cnn(height, width, num_exposures, num_classes, depth=3):
        input_layer = Input(shape=(height, width, depth*num_exposures),
                            name="input_1")
        x = input_layer
        num_layer = 1

        # stack 1
        x = Conv2D(8, (7, 7), strides=(1, 1), padding='same',
                   name='conv_' + str(num_layer), use_bias=False)(x)

        num_layer += 1
        print("stack 1")

        # stack 2
        x, num_layer = MultiExpoNet.dense_block(x, 8, num_layer)
        print("stack 2")

        # stack 3
        x, num_layer = MultiExpoNet.dense_block(x, 16, num_layer)
        print("stack 3")

        # stack 4
        x, num_layer = MultiExpoNet.dense_block(x, 32, num_layer)
        print("stack 4")

        # stack 5
        x, num_layer = MultiExpoNet.dense_block(x, 64, num_layer)
        print("stack 5")

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
