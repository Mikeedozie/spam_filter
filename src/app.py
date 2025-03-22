from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load model and vectorizer
model = joblib.load('../models/spam_model.pkl')
vectorizer = joblib.load('../models/tfidf_vectorizer.pkl')

def preprocess_text(text):
    # Reuse the same preprocessing function
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [word for word in words if word not in stopwords.words('english')]
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    return ' '.join(words)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    email_text = data['text']
    processed_text = preprocess_text(email_text)
    features = vectorizer.transform([processed_text])
    prediction = model.predict(features)
    result = "Spam" if prediction[0] == 1 else "Ham"
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)