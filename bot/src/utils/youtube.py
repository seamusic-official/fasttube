import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Define the scopes required for accessing YouTube
flow = Flow.from_client_secrets_file(
    'client_secret_912264674877-01q28en311jfi4lkj7qao5225pobtlaq.apps.googleusercontent.com.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],
    redirect_uri='http://localhost:8000/callback'
)

def get_auth_url():
    # Generate the authorization URL
    auth_url, _ = flow.authorization_url(prompt='consent')
    return auth_url

def save_credentials(creds):
    # Save the credentials for future use
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

def load_credentials():
    # Load saved credentials
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
            return creds
    return None

def authenticate_user():
    creds = load_credentials()
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_912264674877-01q28en311jfi4lkj7qao5225pobtlaq.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        save_credentials(creds)
    return creds