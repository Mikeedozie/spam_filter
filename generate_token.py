from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes (permissions your app needs)
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Use the default redirect URI
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',
    SCOPES,
    redirect_uri='http://localhost:8080/'
)

# Run the OAuth flow
auth_url, _ = flow.authorization_url(prompt='consent')
print('Please go to this URL and authorize the app:')
print(auth_url)

# Get the authorization code from the user
print('\nAfter granting permissions, you will be redirected to a localhost URL.')
print('Copy the "code" parameter from the URL and paste it below.')
code = input('Enter the authorization code: ')

# Exchange the authorization code for tokens
flow.fetch_token(code=code)

# Save the credentials to token.json
with open('token.json', 'w') as token:
    token.write(flow.credentials.to_json())

print("token.json file created successfully!")