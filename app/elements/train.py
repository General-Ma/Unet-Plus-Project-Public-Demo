import tensorflow as tf
import os
from .model_architecture import B_Unet, ResUnet, UResNet
import glob
import cv2
import numpy as np

# help function to read data from directory
def list_images_in_dir(directory):
    images = []
    image_files = glob.glob(os.path.join(directory,'*.tiff'))
    if len(image_files) == 0:
        image_files = glob.glob(os.path.join(directory,'*.png'))
    for img_file in image_files:
        img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)
        images.append(img)
    return images

# read and load Orig and TG images into a numpy array list
def data_reader(data_dir, mask_dir):
    data_var = list_images_in_dir(data_dir)
    masks_var = list_images_in_dir(mask_dir)
    
    # Process mask
    processed_masks_var = []
    for mask in masks_var:
        processed_mask = np.where(mask > 0, 1, 0)
        processed_masks_var.append(processed_mask)

    # normalize original image
    normalized_data_var = []
    for image in data_var:
        #image = np.array(image)
        image = np.array(image, dtype=np.int64)
        normalized_data = (image - image.min()) / (image.max() - image.min()) * 5
        normalized_data_var.append(normalized_data)
    
    return normalized_data_var, processed_masks_var

# train main functionality
def start_train(orig_data_dir:str, mask_data_dir:str, model_type:str, epoch:int) -> tf.keras.Model:
    # Validate all input parameters is set and is legal
    assert orig_data_dir != '', f'Original data directory is missing.'
    assert mask_data_dir != '', f'True Ground data directory is missing.'
    assert os.path.isdir(orig_data_dir), f"Original data directory '{orig_data_dir}' does not exist."
    assert os.path.isdir(mask_data_dir), f"True Ground data directory '{mask_data_dir}' does not exist."
    assert model_type is not None, f"Model type is not specified."
    try:
        epoch = int(epoch)
    except:
        raise ValueError("Epoch must be a integer between 1-200.")
    assert isinstance(epoch, int) and epoch > 0 and epoch < 201, "Epoch must be a integer between 1-200."

    # load data and assign train, validation data, in this version all data will be used for training
    data_origs, data_masks = data_reader(orig_data_dir,mask_data_dir)
    X_train = data_origs
    y_train = data_masks
    # reformat data for model inputs
    X_train = np.expand_dims(np.stack(X_train, axis=0), axis=-1)
    y_train = np.expand_dims(np.stack(y_train, axis=0), axis=-1)

    # use CUDA for trainning if possible
    device_name = '/GPU:0'if len(tf.config.list_physical_devices('GPU')) > 0 else '/CPU:0'
    if model_type == 'b_unet':
        model = B_Unet.unet_2d()
    elif model_type == 'resunet':
        model = ResUnet.res_unet_2d()
    elif model_type == 'uresnet':
        model = UResNet.u_resnet_2d()
    else:
        raise Exception('Unknown model')
    with tf.device(device_name):
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
        model.fit(X_train, y_train, batch_size=8, epochs=epoch, verbose=None)

    return model