import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# Google API Scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

def authenticate_google():
    """Authenticate and create the Google API service."""
    
    # Load credentials from environment variables
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not credentials_json:
        raise ValueError("Google credentials not found in the environment variable")
    
    # Parse the JSON string into a Python dictionary
    credentials_dict = json.loads(credentials_json)
    
    # Save the dictionary into a temporary file (can delete after auth)
    with open("credentials.json", "w") as f:
        json.dump(credentials_dict, f)
    
    creds = None
    if os.path.exists('token.json'):
        # Load the credentials from the token file (if it exists)
        with open('token.json', 'r') as token:
            creds = json.load(token)
    
    # If no valid credentials are available, let the user log in.
    if not creds or not creds.get("token"):
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        
        # Specify the port as 8084 to match the configured redirect URI
        creds = flow.run_local_server(port=5280, open_browser=False)  # Disable automatic browser launch
        
        # Print the URL for manual login in case the automatic browser cannot be launched
        print("Please visit the following URL to authenticate: ")
        print(flow.authorization_url()[0])
        
        # You will need to manually open the printed URL in a browser, sign in, and paste the code back into the console.
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            json.dump(creds, token)
    
    # Return the authenticated service
    service = build('gmail', 'v1', credentials=creds)
    return service

def authenticate_slack():
    slack_token = os.getenv("SLACK_API_TOKEN")
    if not slack_token:
        raise ValueError("Slack API token not found in the environment variable")
    
    client = WebClient(token=slack_token)
    return client
