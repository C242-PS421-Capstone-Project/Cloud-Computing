from google.cloud import storage
import tensorflow as tf
import cv2
import numpy as np
import os

def download_model_from_gcs(bucket_name, gcs_model_path, local_model_path):
    """Download model file from GCS bucket to local file system."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_model_path)
    blob.download_to_filename(local_model_path)
    print(f"Model downloaded from GCS bucket {bucket_name}/{gcs_model_path} to {local_model_path}")

def load_model(bucket_name="fresh-fish-bucket", 
               gcs_model_path="model-in-prod/fish_freshness_model.h5", 
               local_model_path="./temp_model.h5"):
    """Load model from GCS or use the locally cached version if available."""
    if not os.path.exists(local_model_path):
        download_model_from_gcs(bucket_name, gcs_model_path, local_model_path)
    return tf.keras.models.load_model(local_model_path)

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
