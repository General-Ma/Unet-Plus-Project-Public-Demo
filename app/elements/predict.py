import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os
import glob

def list_images_in_dir_pred(directory):
    images = []
    image_filenames = glob.glob(os.path.join(directory,'*.tiff'))
    if len(image_filenames) == 0:
        image_filenames = glob.glob(os.path.join(directory,'*.png'))
    for img_file in image_filenames:
        img = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)
        images.append(img)
    #return image arrays, and filenames
    return images, image_filenames

def data_reader_pred(data_dir):
    data_var, data_filenames = list_images_in_dir_pred(data_dir)
    # normalize original image
    normalized_data_var = []
    for image in data_var:
        #image = np.array(image)
        image = np.array(image, dtype=np.int64)
        normalized_data = (image - image.min()) / (image.max() - image.min()) * 5
        normalized_data_var.append(normalized_data)
    shortened_filenames = []
    for filename in data_filenames:
        filename = filename.split('\\')[-1].split('\/')[-1].split('/')[-1]
        filename = filename.split('.')[0]
        shortened_filenames.append(filename)
    return normalized_data_var, shortened_filenames

# predict main functionality
def start_predict(predict_data_dir:str, output_mask_dir:str, model_dir:str):
    # Validate all input parameters is set and is legal
    assert predict_data_dir != '', f'Prediction data directory is missing.'
    assert model_dir != '', f'Model directory is missing.'
    assert output_mask_dir != '', f'Output directory is missing.'
    assert os.path.isdir(predict_data_dir), f"Prediction data directory '{predict_data_dir}' does not exist."
    assert os.path.isdir(model_dir), f"Model cannot be found in '{model_dir}' ."
    assert os.path.isdir(output_mask_dir), f"Output directory '{output_mask_dir}' does not exist."
    model = load_model(model_dir)
    print("Model loaded successfully")

    # Read data
    input_images, filenames = data_reader_pred(predict_data_dir)
    print("Image loaded successfully")
    device_name = '/GPU:0'if len(tf.config.list_physical_devices('GPU')) > 0 else '/CPU:0'
    with tf.device(device_name):
        # Make predictions
        predicted_images = []
        for image in input_images:
            image = np.expand_dims(image, axis=0)
            prediction = model.predict(image)
            predicted_images.append(prediction)
        
        # Format the output and save in the designated folder
        for image, name in zip(predicted_images, filenames):
            image = image.squeeze()

            # Save the mask as binary or as a probability range from 0-255, depending on the requirement and future use
            image = (image * 255).astype(np.uint8)
            #image = np.where(image > 0.5, 1, 0).astype(np.uint8)
            
            cv2.imwrite(os.path.join(output_mask_dir, name+'_predicted.png'), image)

    return