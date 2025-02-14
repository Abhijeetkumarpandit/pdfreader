from flask import Flask, request, jsonify
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import io
from sentence_transformers import SentenceTransformer, util
import json
import os

app = Flask(__name__)

# Load SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Field mappings for data extraction
field_mappings = {
    "Business Legal Name": ["Business Legal Name", "LEGAL/CORPORATE NAME:", "Legal/Corporate Name:", "Applicant:"],
    "DBA": ["DBA (Doing Business as)", "Business D/B/A Name"],
    "Business Physical Address": ["Business Address"],
    "City": ["Business City"],
    "State": ["Business State"],
    "Zip": ["Business Zip"],
    "Business Mailing Address": ["Business email address"],
    "Mobile": ["Business Mobile Number", "Cell Phone #"],
    "Legal Entity": ["INC", "LLC"],
    "Established Date": ["business established Date"],
    "Product/Services Sold": ["service they provided"],
    "Federal Tax ID": ["federal tax id", "Federal State Tax #:", "Federal Tax ID #:"],
    "Principal(1) Full Name": ["first name and last name", "business owner", "owner name", "Applicant"],
    "Email": ["email id", "Email:"],
    "Home Address": ["home address", "Home Address:"],
    "Home City": ["home city", "City:"],
    "Home State": ["home state", "State:"],
    "Home Zip": ["home zip", "Zip:"],
    "SSN": ["SSN:", "SSN#:", "SS #:", "Social Security No:"],
    "Date of Birth": ["date of birth (dob)", "DOB:"],
    "Ownership %": ["ownership percentage"],
    "Home Mobile": ["home mobile number", "Cell Phone"],
    "Amount": ["Amount Requested", "Amont in"],
    "firstname": ["First Name", "Applicant", "Name:"],
    "lastname": ["Last Name"]
}

def extract_data(text):
    """Extract structured data from OCR text using SentenceTransformers"""
    extracted_data = {key: "" for key in field_mappings}
    sentences = text.split('\n')
    
    if not sentences:
        return extracted_data
    
    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
    
    for field, variations in field_mappings.items():
        variation_embeddings = model.encode(variations, convert_to_tensor=True)
        similarity_scores = util.cos_sim(variation_embeddings, sentence_embeddings)
        
        best_match_idx = similarity_scores.max(dim=1).values.argmax().item()
        best_match_sentence = sentences[best_match_idx]
        
        extracted_value = best_match_sentence.split(':', 1)[-1].strip() if ':' in best_match_sentence else ""
        extracted_data[field] = extracted_value if extracted_value else ""
    
    return extracted_data

@app.route('/process', methods=['POST'])
def process_pdf():
    """API Endpoint to process PDF and extract structured data"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    pdf_bytes = file.read()
    
    try:
        images = convert_from_bytes(pdf_bytes, dpi=300)
        extracted_text = []
        
        for img in images:
            text = pytesseract.image_to_string(img)
            extracted_text.append(text)
        
        combined_text = '\n'.join(extracted_text)
        extracted_data = extract_data(combined_text)
        
        return jsonify(extracted_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
