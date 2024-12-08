import tensorflow as tf
import cv2
import numpy as np

import tensorflow as tf

def load_model_from_url(bucket_url):
    """Load HDF5 model directly from GCS bucket URL."""
    # Download the model file to a temporary location
    model_path = tf.keras.utils.get_file(
        fname="fish_freshness_model.h5",  # Temporary name for the model
        origin=bucket_url
    )
    # Load the model from the downloaded file
    return tf.keras.models.load_model(model_path)

def preprocess_image(image_path, target_size):
    """Preprocess the image for prediction."""
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    image = cv2.resize(image, target_size) / 255.0  # Resize and normalize
    return np.expand_dims(image, axis=0)  # Add batch dimension

def predict_image(model, image_path, target_size):
    """Predict the class of the image using the loaded model."""
    prediction = model.predict(preprocess_image(image_path, target_size))[0][0]
    return f"{'Fresh' if prediction < 0.5 else 'Not Fresh'} {prediction:.2f}"
