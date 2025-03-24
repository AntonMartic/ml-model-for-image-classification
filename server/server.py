from flask import Flask, request, jsonify
from flask_cors import CORS
import main  # Importerar din klassificeringslogik
import time
import gc
import tracemalloc
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/api/home', methods=['GET'])
def home():
    return jsonify({"message": "API Online"})

@app.route('/classify-image', methods=['POST'])
def classify_image():
    # Start memory tracking
    tracemalloc.start()
    try: 
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        class_type = (request.form.get("type") or "SVM").strip().upper()  # SVM or RF

        # Extract HOG features
        hog_viz_base64, img_resized, hog_features = main.preprocess_single_image(file)
        file.seek(0)  # Reset file pointer

        # Predict class
        if class_type == "SVM":
            prediction = main.svm_model.predict(hog_features)
        else:
            prediction = main.rf_model.predict(hog_features)

        class_names = {0: "Cat", 1: "Dog"}
        result = class_names[prediction[0]]
        
        start = time.perf_counter()
        # Generate occlusion sensitivity heatmap
        if class_type == "SVM":
            heatmap_base64 = main.occlusion_sensitivity(main.svm_model, hog_features, prediction[0], img_resized, class_type)
        else:
            heatmap_base64 = main.occlusion_sensitivity(main.rf_model, hog_features, prediction[0], img_resized, class_type)
        end = time.perf_counter()

        # Log memory usage
        current, peak = tracemalloc.get_traced_memory()
        logger.info(f"Current memory usage: {current / 10**6:.2f} MB")
        logger.info(f"Peak memory usage: {peak / 10**6:.2f} MB")

        # Log processing time
        logger.info(f"Function took {end - start:.3f} seconds to run.")


        # Prepare response
        response = jsonify({
            "result": result,
            "heatmap": heatmap_base64,
            "hog_visualization": hog_viz_base64
        })

        del result, heatmap_base64, hog_viz_base64, hog_features, img_resized
        gc.collect()
        
        logger.info(f"Current memory usage: {current / 10**6:.2f} MB")
        tracemalloc.stop()
        return response
    
    except Exception as e:
        logger.error(f"Classification error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
    finally:
        # Ensure memory is cleaned up
        gc.collect()
    
if __name__ == '__main__':
    gc.enable()
    app.run(debug=True, port=8080)