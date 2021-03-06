def conv_ae_ap():
    from keras.models import Model
    from keras.layers.convolutional import Conv2D, Conv2DTranspose
    from keras.layers import Input, AveragePooling2D, UpSampling2D

    channel_num = 1
    input_tensor = Input(shape=(160, 240, channel_num))

    conv1 = Conv2D(128, kernel_size=(7, 7), padding='same', name='conv1', activation='relu')(input_tensor)
    conv1 = AveragePooling2D((2,2), padding='same')(conv1)

    conv2 = Conv2D(64, kernel_size=(3, 3), padding='same', strides=(2, 2), name='conv2', activation='relu')(conv1)
    conv2 = AveragePooling2D((2, 2), padding='same')(conv2)

    conv3 = Conv2D(32, kernel_size=(3, 3), padding='same', strides=(1, 1), name='conv3', activation='relu')(conv2)
    conv3 = AveragePooling2D((2, 2), padding='same')(conv3)

    deconv1 = Conv2D(32, kernel_size=(3, 3), padding='same', strides=(1, 1), name='deconv1', activation='relu')(conv3)
    deconv1 = UpSampling2D((2, 2))(deconv1)

    deconv2 = Conv2D(32, kernel_size=(3, 3), padding='same', strides=(1, 1), name='deconv2', activation='relu')(deconv1)
    deconv2 = UpSampling2D((2, 2))(deconv2)

    deconv3 = Conv2D(64, kernel_size=(3, 3), padding='same', strides=(1, 1), name='deconv3', activation='relu')(deconv2)
    deconv3 = UpSampling2D((2, 2))(deconv3)

    deconv4 = Conv2D(64, kernel_size=(3, 3), padding='same', strides=(1, 1), name='deconv4', activation='relu')(deconv3)
    deconv4 = UpSampling2D((2, 2))(deconv4)

    decoded = Conv2D(channel_num, kernel_size=(3, 3), padding='same', strides=(1, 1), name='deconvAAAA', activation="sigmoid")(deconv4)

    return Model(inputs=input_tensor, outputs=decoded)


def conv_ae_mp():
    from keras.models import Model
    from keras.layers.convolutional import Conv2D, Conv2DTranspose
    from keras.layers import Input, MaxPool2D

    channel_num = 1
    input_tensor = Input(shape=(160, 240, channel_num))

    conv1 = Conv2D(128, kernel_size=(7, 7), padding='same', name='conv1', activation='relu')(input_tensor)
    conv1 = MaxPool2D((2,2), padding='same')(conv1)

    conv2 = Conv2D(64, kernel_size=(3, 3), padding='same', strides=(2, 2), name='conv2', activation='relu')(conv1)
    conv2 = MaxPool2D((2,2), padding='same')(conv2)

    conv3 = Conv2D(32, kernel_size=(3, 3), padding='same', strides=(1, 1), name='conv3', activation='relu')(conv2)

    deconv2 = Conv2DTranspose(32, kernel_size=(3, 3), padding='same', strides=(2, 2), name='deconv2', activation='relu')(conv3)

    deconv3 = Conv2DTranspose(64, kernel_size=(3, 3), padding='same', strides=(2, 2), name='deconv3', activation='relu')(deconv2)

    decoded = Conv2DTranspose(channel_num, kernel_size=(3, 3), padding='same', strides=(2, 2), name='deconvAAAA')(deconv3)

    return Model(inputs=input_tensor, outputs=decoded)

def conv_ae():
    from keras.models import Model
    from keras.layers.convolutional import Conv2D, Conv2DTranspose
    from keras.layers.normalization import BatchNormalization
    from keras.layers.core import Activation
    from keras.layers import Input

    channel_num = 1
    input_tensor = Input(shape=(160, 240, channel_num))

    conv1 = Conv2D(128, kernel_size=(7, 7), padding='same', strides=(4, 4), name='conv1')(input_tensor)
    conv1 = BatchNormalization()(conv1)
    conv1 = Activation('relu')(conv1)

    conv2 = Conv2D(64, kernel_size=(5, 5), padding='same', strides=(2, 2), name='conv2')(conv1)
    conv2 = BatchNormalization()(conv2)
    conv2 = Activation('relu')(conv2)

    conv3 = Conv2D(32, kernel_size=(3, 3), padding='same', strides=(1, 1), name='conv3')(conv2)
    conv3 = BatchNormalization()(conv3)
    conv3 = Activation('relu')(conv3)

    deconv2 = Conv2DTranspose(64, kernel_size=(3, 3), padding='same', strides=(2, 2), name='deconv2')(conv3)
    deconv2 = BatchNormalization()(deconv2)
    deconv2 = Activation('relu')(deconv2)

    decoded = Conv2DTranspose(channel_num, kernel_size=(11, 11), padding='same', strides=(4, 4), name='deconvAAAA')(deconv2)

    return Model(inputs=input_tensor, outputs=decoded)

def conv_lstm_ae():
    from keras.models import Model
    from keras.layers.convolutional import Conv2D, Conv2DTranspose
    from keras.layers.convolutional_recurrent import ConvLSTM2D
    from keras.layers.normalization import BatchNormalization
    from keras.layers.wrappers import TimeDistributed
    from keras.layers.core import Activation
    from keras.layers import Input
    import yaml

    with open('config.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    t = cfg['time_length']
    input_tensor = Input(shape=(t, 160, 240, 1))

    conv1 = TimeDistributed(Conv2D(128, kernel_size=(11, 11), padding='same', strides=(4, 4), name='conv1'),
                            input_shape=(t, 160, 240, 1))(input_tensor)
    conv1 = TimeDistributed(BatchNormalization())(conv1)
    conv1 = TimeDistributed(Activation('relu'))(conv1)

    conv2 = TimeDistributed(Conv2D(64, kernel_size=(5, 5), padding='same', strides=(2, 2), name='conv2'))(conv1)
    conv2 = TimeDistributed(BatchNormalization())(conv2)
    conv2 = TimeDistributed(Activation('relu'))(conv2)

    convlstm1 = ConvLSTM2D(64, kernel_size=(3, 3), padding='same', return_sequences=True, name='convlstm1')(conv2)
    convlstm2 = ConvLSTM2D(32, kernel_size=(3, 3), padding='same', return_sequences=True, name='convlstm2')(convlstm1)
    convlstm3 = ConvLSTM2D(64, kernel_size=(3, 3), padding='same', return_sequences=True, name='convlstm3')(convlstm2)

    deconv1 = TimeDistributed(Conv2DTranspose(128, kernel_size=(5, 5), padding='same', strides=(2, 2), name='deconv1'))(convlstm3)
    deconv1 = TimeDistributed(BatchNormalization())(deconv1)
    deconv1 = TimeDistributed(Activation('relu'))(deconv1)

    decoded = TimeDistributed(Conv2DTranspose(1, kernel_size=(11, 11), padding='same', strides=(4, 4), name='deconv2'))(
        deconv1)

    return Model(inputs=input_tensor, outputs=decoded)

conv_ae().summary()