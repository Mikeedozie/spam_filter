import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import joblib

def train_model():
    # Load processed data
    data = pd.read_csv('../data/processed_data.csv')
    texts = data['text']
    labels = data['label']  # 0 for ham, 1 for spam

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(texts)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

    # Train model
    model = MultinomialNB()
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save model and vectorizer
    joblib.dump(model, '../models/spam_model.pkl')
    joblib.dump(vectorizer, '../models/tfidf_vectorizer.pkl')

if __name__ == "__main__":
    train_model()