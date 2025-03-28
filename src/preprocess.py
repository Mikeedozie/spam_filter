import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download NLTK stopwords
nltk.download('stopwords')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize
    words = text.split()
    # Remove stopwords
    words = [word for word in words if word not in stopwords.words('english')]
    # Stemming
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    return ' '.join(words)

def preprocess_data(input_file, output_file):
    # Load dataset
    data = pd.read_csv(input_file)
    # Preprocess text
    data['text'] = data['text'].apply(preprocess_text)
    # Save processed data
    data.to_csv(output_file, index=False)

if __name__ == "__main__":
    preprocess_data('../data/spam_dataset.csv', '../data/processed_data.csv')