from flask import Flask, request, jsonify
from flask_cors import CORS
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
    class_type = (request.form.get("type") or "SVM").strip().upper()  # SVM or RF
    try:
        # Extract HOG features
        hog_features, img_resized = main.preprocess_single_image(file)
        file.seek(0)  # Reset file pointer

        # Predict class
        if class_type == "SVM":
            prediction = main.svm_model.predict(hog_features)
        else:
            prediction = main.rf_model.predict(hog_features)

        class_names = {0: "Cat", 1: "Dog"}
        result = class_names[prediction[0]]

        # Generate occlusion sensitivity heatmap
        if class_type == "SVM":
            heatmap_base64 = main.occlusion_sensitivity(file, main.svm_model, main.preprocess_single_image)
        else:
            heatmap_base64 = main.occlusion_sensitivity(file, main.rf_model, main.preprocess_single_image)
        file.seek(0)  # Reset file pointer again
        
        # Generate HOG feature visualization
        hog_viz_base64 = main.visualize_hog_features(file)

        return jsonify({
            "result": result,
            "heatmap": heatmap_base64,
            "hog_visualization": hog_viz_base64
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)