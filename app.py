from flask import Flask, request, jsonify
import os
from model import load_model, predict_image

app = Flask(__name__)

# Load the model once at the start
model = load_model()

@app.route('/predict', methods=['POST'])
def identifikasi():
    image_file = request.files.get('image')

    if not image_file:
        return jsonify({'error': 'No image uploaded'}), 400

    temp_path = 'temp_image.jpg'
    image_file.save(temp_path)

    try:
        prediction = predict_image(model, temp_path, target_size=(128, 128))
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)  # Ensure the temporary file is always removed


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
