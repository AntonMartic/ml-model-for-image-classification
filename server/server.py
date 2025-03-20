import base64
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import matplotlib.pyplot as plt
import main  # Importerar din klassificeringslogik

app = Flask(__name__)
CORS(app)

@app.route('/api/home', methods=['GET'])
def home():
    return jsonify({"message": "API Online"})

@app.route('/classify-image', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Preprocess image once
        preprocessed_data = main.preprocess_single_image(file)

        # Predict class
        prediction = main.svm_model.predict(preprocessed_data["features"])
        class_names = {0: "Cat", 1: "Dog"}
        result = class_names[prediction[0]]

        # Generate occlusion sensitivity heatmap
        heatmap_base64 = main.occlusion_sensitivity(file, main.svm_model, preprocessed_data)

        # Generate HOG feature visualization
        hog_viz_base64 = main.visualize_hog_features(preprocessed_data)

        return jsonify({
            "result": result,
            "heatmap": heatmap_base64,
            "hog_visualization": hog_viz_base64
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
if __name__ == '__main__':
    app.run(debug=True, port=8080)
