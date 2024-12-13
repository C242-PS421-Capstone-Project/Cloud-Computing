import tensorflow as tf
import cv2
import numpy as np

import tensorflow as tf

def load_model_from_url(bucket_url):
    """Load HDF5 model directly from GCS bucket URL."""
    model_path = tf.keras.utils.get_file(
        fname="fish_freshness_model.h5",
        origin=bucket_url
    )
    return tf.keras.models.load_model(model_path)

def preprocess_image(image_path, target_size):
    """Preprocess the image for prediction."""
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, target_size) / 255.0
    return np.expand_dims(image, axis=0)

def predict_image(model, image_path, target_size):
    """Predict the class of the image using the loaded model."""
    prediction = model.predict(preprocess_image(image_path, target_size))[0][0]
    return f"{'Fresh' if prediction < 0.5 else 'Not Fresh'} {prediction:.2f}"
