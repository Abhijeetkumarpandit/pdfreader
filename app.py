import os
import pytesseract
from flask import Flask, request, jsonify
from flask_cors import CORS
from pdf2image import convert_from_bytes

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route("/extract_text", methods=["POST"])
def extract_text():
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400

    pdf_file = request.files["pdf"].read()
    images = convert_from_bytes(pdf_file)  # Convert PDF to images

    extracted_text = ""
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        extracted_text += f"\n--- Page {i+1} ---\n{text}"

    return jsonify({"text": extracted_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
