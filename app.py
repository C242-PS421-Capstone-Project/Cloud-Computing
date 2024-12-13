from firebase_admin import firestore
from flask import Flask, request, jsonify
import os
import uuid
from datetime import datetime
from google.cloud import secretmanager
from model import load_model_from_url, predict_image
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)

def get_firebase_credentials():
    """Retrieve Firebase credentials from Google Secret Manager."""
    secret_name = "projects/fresh-fish-api/secrets/firebase/versions/latest"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": secret_name})
    credentials = response.payload.data.decode("utf-8")
    return credentials

def initialize_firestore():
    """Initialize Firestore connection."""
    firebase_credentials = get_firebase_credentials()
    cred = credentials.Certificate(eval(firebase_credentials))
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = initialize_firestore()

BUCKET_MODEL_URL = "https://storage.googleapis.com/fresh-fish-bucket/model-in-prod/fish_freshness_model.h5"

model = load_model_from_url(BUCKET_MODEL_URL)

def save_to_firestore(prediction_id, result, message):
    """Save prediction result to Firestore."""
    try:
        prediction_doc = {
            "id": prediction_id,
            "result": result,
            "message": message,
            "createdAt": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        db.collection('predictions').document(prediction_id).set(prediction_doc)
        print(f"Prediction saved to Firestore: {prediction_doc}")
    except Exception as e:
        print(f"Error saving prediction to Firestore: {e}")

@app.route('/predict', methods=['POST'])
def identifikasi():
    """Handle image prediction requests."""
    image_file = request.files.get('image')

    if not image_file:
        return jsonify({
            "status": "fail",
            "message": "No image uploaded"
        }), 400

    temp_path = 'temp_image.jpg'
    image_file.save(temp_path)

    try:
        prediction = predict_image(model, temp_path, target_size=(128, 128))
        print(f"Prediction output: {prediction}")

        if prediction.startswith("Fresh"):
            result = "Fresh"
            message = "Fish Looks Fresh!"
        elif prediction.startswith("Not Fresh"):
            result = "Not Fresh"
            message = "Fish doesn't look fresh!"
        else:
            raise ValueError("Unexpected prediction output")

        prediction_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        save_to_firestore(prediction_id, result, message)

        response = {
            "status": "success",
            "message": "Model is predicted successfully",
            "data": {
                "id": prediction_id,
                "result": result,
                "massage": message,
                "createdAt": timestamp
            }
        }
        return jsonify(response), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "status": "fail",
            "message": "An error occurred in making a prediction"
        }), 400
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.route('/predictions', methods=['GET'])
def get_predictions():
    """Fetch predictions data from Firestore."""
    try:
        predictions_ref = db.collection('predictions')
        docs = predictions_ref.stream()
        predictions = []
        for doc in docs:
            predictions.append(doc.to_dict())
        return jsonify({
            "status": "success",
            "data": predictions
        }), 200
    except Exception as e:
        print(f"Error fetching predictions: {e}")
        return jsonify({
            "status": "fail",
            "message": "An error occurred while fetching data"
        }), 500

articles = [
    {
        "image_url": "https://storage.googleapis.com/fresh-fish-bucket/image-in-prod/tuna.jpg",
        "title": "Mengenal Ikan Tuna",
        "description": "Ikan tuna merupakan salah satu ikan laut yang banyak dikonsumsi karena kaya akan protein.",
    },
    {
        "image_url": "https://storage.googleapis.com/fresh-fish-bucket/image-in-prod/salmon.jpg",
        "title": "Manfaat Ikan Salmon",
        "description": "Ikan salmon mengandung asam lemak omega-3 yang baik untuk kesehatan jantung.",
    }
]

@app.route('/articles', methods=['GET'])
def get_articles():
    """Fetch articles data."""
    try:
        return jsonify({
            "status": "success",
            "data": articles
        }), 200
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return jsonify({
            "status": "fail",
            "message": "An error occurred while fetching articles"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
