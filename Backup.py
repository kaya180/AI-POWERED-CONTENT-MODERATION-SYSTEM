from flask import Flask, render_template, request
import pickle
import re
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')

app = Flask(__name__)

# Load stopwords and stemmer
stopwords_set = set(stopwords.words('english'))
stemmer = PorterStemmer()


# Load the trained model and vectorizer
with open("model.pkl", "rb") as model_file:
    clf = pickle.load(model_file)

with open("vectorizer.pkl", "rb") as vectorizer_file:
    cv = pickle.load(vectorizer_file)

# Define text cleaning function
def clean(text):
    text = str(text).lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    text = [word for word in text.split() if word not in stopwords_set]
    text = ' '.join(text)
    text = [stemmer.stem(word) for word in text.split()]
    return ' '.join(text)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        user_input = request.form.get("text")
        processed_text = clean(user_input)
        vectorized_text = cv.transform([processed_text])
        prediction = clf.predict(vectorized_text)[0]
    
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
