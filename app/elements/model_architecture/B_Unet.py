import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Conv2DTranspose, concatenate, BatchNormalization

# For most slices in our initial projects are 200 * 200, it is set as default, but you can mannually change it to any multiples of 4 no smaller than 128
# Automatic resize will be enabled in futhre updates
def unet_2d(n_class=1, input_size=(200, 200, 1)):
    inputs = Input(input_size)
    
    # Encoder
    e11 = Conv2D(16, (3, 3), activation='relu', padding='same')(inputs)
    e11 = BatchNormalization()(e11)
    e12 = Conv2D(16, (3, 3), activation='relu', padding='same')(e11)
    e12 = BatchNormalization()(e12)
    pool1 = MaxPooling2D(pool_size=(2, 2))(e12)
    
    e21 = Conv2D(32, (3, 3), activation='relu', padding='same')(pool1)
    e21 = BatchNormalization()(e21)
    e22 = Conv2D(32, (3, 3), activation='relu', padding='same')(e21)
    e22 = BatchNormalization()(e22)
    pool2 = MaxPooling2D(pool_size=(2, 2))(e22)
    
    e31 = Conv2D(64, (3, 3), activation='relu', padding='same')(pool2)
    e31 = BatchNormalization()(e31)
    e32 = Conv2D(64, (3, 3), activation='relu', padding='same')(e31)
    e32 = BatchNormalization()(e32)
    pool3 = MaxPooling2D(pool_size=(2, 2))(e32)
    
    e41 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool3)
    e41 = BatchNormalization()(e41)
    e42 = Conv2D(128, (3, 3), activation='relu', padding='same')(e41)
    e42 = BatchNormalization()(e42)
    
    # Decoder
    upconv3 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='valid')(e42)
    merge3 = concatenate([upconv3, e32])
    d31 = Conv2D(64, (3, 3), activation='relu', padding='same')(merge3)
    d31 = BatchNormalization()(d31)
    d32 = Conv2D(64, (3, 3), activation='relu', padding='same')(d31)
    d32 = BatchNormalization()(d32)
    
    upconv2 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='valid')(d32)
    merge2 = concatenate([upconv2, e22])
    d21 = Conv2D(32, (3, 3), activation='relu', padding='same')(merge2)
    d21 = BatchNormalization()(d21)
    d22 = Conv2D(32, (3, 3), activation='relu', padding='same')(d21)
    d22 = BatchNormalization()(d22)
    
    upconv1 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='valid')(d22)
    merge1 = concatenate([upconv1, e12])
    d11 = Conv2D(16, (3, 3), activation='relu', padding='same')(merge1)
    d11 = BatchNormalization()(d11)
    d12 = Conv2D(16, (3, 3), activation='relu', padding='same')(d11)
    d12 = BatchNormalization()(d12)
    
    out_conv = Conv2D(n_class, (1, 1), activation='sigmoid')(d12)
    
    model = tf.keras.Model(inputs=inputs, outputs=out_conv)
    
    return model


if __name__ == "__main__":
    model = unet_2d()
    model.summary()