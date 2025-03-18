from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)
CORS(app)   

@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        "message": "Dog"
    })

if __name__ == "__main__":
    app.run(debug=True, port=8080)