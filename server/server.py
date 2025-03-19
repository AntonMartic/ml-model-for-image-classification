from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import main

app = Flask(__name__)
CORS(app)

@app.route('/api/home', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to Dog and Cat Classifier API"})

@app.route('/classify-image', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Läs in och klassificera bilden
        hog_features, _ = main.preprocess_single_image(file)
        prediction = main.svm_model.predict(hog_features)
        
        class_names = {0: "Cat", 1: "Dog"}
        result = class_names[prediction[0]]

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)