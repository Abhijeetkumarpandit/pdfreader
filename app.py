import os
import pytesseract
from flask import Flask, request, jsonify
from flask_cors import CORS
from pdf2image import convert_from_bytes

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route("/extract_text", methods=["POST"])
def extract_text():
    try:
        # Check if PDF file is in the request
        if "pdf" not in request.files:
            return jsonify({"error": "No PDF uploaded"}), 400

        # Get the PDF file from the request
        pdf_file = request.files["pdf"].read()

        # Convert the PDF to images
        images = convert_from_bytes(pdf_file)

        # Initialize extracted text
        extracted_text = ""

        # Extract text from each image using pytesseract
        for i, img in enumerate(images):
            text = pytesseract.image_to_string(img)
            extracted_text += f"\n--- Page {i+1} ---\n{text}"

        # Return the extracted text as JSON
        return jsonify({"text": extracted_text})

    except Exception as e:
        # Log any errors and return a 500 response with the error message
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the app on 0.0.0.0 and port 5000 (or adjust as necessary)
    app.run(host="0.0.0.0", port=5000)
