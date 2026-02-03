from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from deep_translator import GoogleTranslator
from langdetect import detect
import nltk

# Ensure necessary NLTK corpora are downloaded
nltk.download('punkt')

# Initialize Flask app
app = Flask(__name__)

# Load a pretrained model for offensive language detection
classifier = pipeline("text-classification", model="unitary/toxic-bert")
translator = GoogleTranslator(source='auto', target='en')

# Function to detect offensive language
def detect_offensive(text):
    try:
        # Detect language
        lang_detected = detect(text)

        # Translate to English if needed
        if lang_detected == 'hi':
            text = translator.translate(text)

        # Get classification result
        result = classifier(text)
        label = result[0]['label']
        score = result[0]['score']

        # Determine response
        return {
            "original_text": text,
            "language_detected": lang_detected,
            "prediction": "Offensive" if label == "toxic" and score > 0.6 else "Normal",
            "confidence": round(score * 100, 2)  # Convert confidence to percentage
        }

    except Exception as e:
        return {"error": str(e)}

# Serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')  # Make sure index.html is in 'templates' folder

# API route for POST requests
@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.is_json:
            data = request.get_json()
            text = data.get("text", "").strip()

            if text:
                result = detect_offensive(text)
                return jsonify(result), 200

            return jsonify({"error": "No text provided"}), 400

        return jsonify({"error": "Invalid JSON"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)

