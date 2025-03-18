from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)
CORS(app)   

@app.route('/classify-image', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Läs in bilden från requesten
        image = Image.open(io.BytesIO(file.read()))
        
        # Använd din klassificeringsfunktion (förutsatt att den tar en PIL bild)
        result = your_classification_script.classify(image)

        # Skicka tillbaka resultatet (t.ex. om det är en hund eller katt)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)