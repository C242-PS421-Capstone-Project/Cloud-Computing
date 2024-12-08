from flask import Flask, request, jsonify
import os
import uuid
from datetime import datetime
from model import load_model_from_url, predict_image

app = Flask(__name__)

# URL Bucket Configuration
BUCKET_MODEL_URL = "https://storage.googleapis.com/fresh-fish-bucket/model-in-prod/fish_freshness_model.h5"

# Load the model once at the start
model = load_model_from_url(BUCKET_MODEL_URL)

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
        # Generate prediction
        prediction = predict_image(model, temp_path, target_size=(128, 128))
        print(f"Prediction output: {prediction}")  # Debugging output

        # Parse prediction result
        if prediction.startswith("Fresh"):
            result = "Fresh"
            message = "Fish Looks Fresh!"
        elif prediction.startswith("Not Fresh"):
            result = "Not Fresh"
            message = "Fish doesn't look fresh!"
        else:
            raise ValueError("Unexpected prediction output")

        # Generate unique ID and timestamp
        prediction_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Construct response
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
        print(f"Error: {e}")  # Debugging output
        return jsonify({
            "status": "fail",
            "message": "An error occurred in making a prediction"
        }), 400
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)  # Ensure the temporary file is always removed


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
