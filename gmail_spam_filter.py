from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import joblib
import base64
from email import message_from_bytes
from email.policy import default

# Load model and vectorizer
model = joblib.load('spam_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

def extract_email_body(msg):
    # Extract the email payload
    payload = msg['payload']
    headers = payload.get('headers', [])
    parts = payload.get('parts', [])
    
    # Get the plain text body
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                body_data = part['body']['data']
                body = base64.urlsafe_b64decode(body_data).decode('utf-8')
                return body
    else:
        body_data = payload['body']['data']
        body = base64.urlsafe_b64decode(body_data).decode('utf-8')
        return body
    return ""

def process_emails():
    # Authenticate
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.modify'])
    service = build('gmail', 'v1', credentials=creds)

    # Fetch unread emails
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg_id = msg['id']
        msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        email_text = extract_email_body(msg_data)
        prediction = model.predict(vectorizer.transform([email_text]))[0]

        if prediction == 1:  # Spam
            service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'addLabelIds': ['SPAM'], 'removeLabelIds': ['INBOX']}
            ).execute()

if __name__ == "__main__":
    process_emails()