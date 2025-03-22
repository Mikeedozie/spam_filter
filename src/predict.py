import joblib

def predict_spam(email_text):
    # Load model and vectorizer
    model = joblib.load('../models/spam_model.pkl')
    vectorizer = joblib.load('../models/tfidf_vectorizer.pkl')
    # Preprocess input text
    processed_text = preprocess_text(email_text)  # Use the same preprocessing function
    # Vectorize
    features = vectorizer.transform([processed_text])
    # Predict
    prediction = model.predict(features)
    return "Spam" if prediction[0] == 1 else "Ham"

if __name__ == "__main__":
    email = input("Enter email text: ")
    print(predict_spam(email))