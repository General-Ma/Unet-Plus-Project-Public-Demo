import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Conv2DTranspose, concatenate, BatchNormalization, Add

def res_unet_2d(n_class=1, input_size=(200, 200, 1)):
    inputs = Input(input_size)
    
    # Encoder
    e11 = Conv2D(16, (3, 3), activation='relu', padding='same')(inputs)
    # add residual layer
    shortcut_e1 = Conv2D(16, (1, 1), activation='relu', padding='same')(inputs)
    e11 = BatchNormalization()(e11)
    e12 = Conv2D(16, (3, 3), activation='relu', padding='same')(e11)
    e12 = BatchNormalization()(e12)
    # add residual path
    shortcut_e1 = BatchNormalization()(shortcut_e1)
    e12 = Add()([e12,shortcut_e1])
    pool1 = MaxPooling2D(pool_size=(2, 2))(e12)
    
    e21 = Conv2D(32, (3, 3), activation='relu', padding='same')(pool1)
    # add residual layer
    shortcut_e2 = Conv2D(32, (1, 1), activation='relu', padding='same')(e21)
    e21 = BatchNormalization()(e21)
    e22 = Conv2D(32, (3, 3), activation='relu', padding='same')(e21)
    e22 = BatchNormalization()(e22)
    # add residual path
    shortcut_e2 = BatchNormalization()(shortcut_e2)
    e22 = Add()([e22,shortcut_e2])
    pool2 = MaxPooling2D(pool_size=(2, 2))(e22)
    
    e31 = Conv2D(64, (3, 3), activation='relu', padding='same')(pool2)
    # add residual layer
    shortcut_e3 = Conv2D(64, (1, 1), activation='relu', padding='same')(e31)
    e31 = BatchNormalization()(e31)
    e32 = Conv2D(64, (3, 3), activation='relu', padding='same')(e31)
    e32 = BatchNormalization()(e32)
    # add residual path
    shortcut_e3 = BatchNormalization()(shortcut_e3)
    e32 = Add()([e32,shortcut_e3])
    pool3 = MaxPooling2D(pool_size=(2, 2))(e32)
    
    e41 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool3)
    # add residual layer
    shortcut_e4 = Conv2D(128, (1, 1), activation='relu', padding='same')(e41)
    e41 = BatchNormalization()(e41)
    e42 = Conv2D(128, (3, 3), activation='relu', padding='same')(e41)
    e42 = BatchNormalization()(e42)
    # add residual path
    shortcut_e4 = BatchNormalization()(shortcut_e4)
    e42 = Add()([e41,shortcut_e4])
    
    # Decoder
    upconv3 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(e42)
    merge3 = concatenate([upconv3, e32])
    d31 = Conv2D(64, (3, 3), activation='relu', padding='same')(merge3)
    # add residual layer
    shortcut_d3 = Conv2D(64, (1, 1), activation='relu', padding='same')(merge3)
    d31 = BatchNormalization()(d31)
    d32 = Conv2D(64, (3, 3), activation='relu', padding='same')(d31)
    d32 = BatchNormalization()(d32)
    #add residual path
    shortcut_d3 = BatchNormalization()(shortcut_d3)
    d32 = Add()([d32, shortcut_d3])
    
    # Decoder block for e22
    upconv2 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(d32)
    merge2 = concatenate([upconv2, e22])
    d21 = Conv2D(32, (3, 3), activation='relu', padding='same')(merge2)
    # add residual layer
    shortcut_d2 = Conv2D(32, (1, 1), activation='relu', padding='same')(merge2)
    d21 = BatchNormalization()(d21)
    d22 = Conv2D(32, (3, 3), activation='relu', padding='same')(d21)
    d22 = BatchNormalization()(d22)
    # add residual path
    shortcut_d2 = BatchNormalization()(shortcut_d2)
    d22 = Add()([d22, shortcut_d2])
    
    # Decoder block for e12
    upconv1 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(d22)
    merge1 = concatenate([upconv1, e12])
    d11 = Conv2D(16, (3, 3), activation='relu', padding='same')(merge1)
    # add residual layer
    shortcut_d1 = Conv2D(16, (1, 1), activation='relu', padding='same')(merge1)
    d11 = BatchNormalization()(d11)
    d12 = Conv2D(16, (3, 3), activation='relu', padding='same')(d11)
    d12 = BatchNormalization()(d12)
    # add residual path
    shortcut_d1 = BatchNormalization()(shortcut_d1)
    d12 = Add()([d12, shortcut_d1])
    
    out_conv = Conv2D(n_class, (1, 1), activation='sigmoid')(d12)
    
    model = tf.keras.Model(inputs=inputs, outputs=out_conv)
    
    return model

if __name__ == "__main__":
    model = res_unet_2d()
    model.summary()