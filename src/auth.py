import os
import base64
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

def authenticate_google():
    creds_base64 = os.getenv("GOOGLE_CREDENTIALS_JSON")
    creds_json = base64.b64decode(creds_base64).decode("utf-8")
    with open("credentials.json", "w") as creds_file:
        creds_file.write(creds_json)
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service

def authenticate_slack():
    slack_token = os.getenv("SLACK_API_TOKEN")
    client = WebClient(token=slack_token)
    return client
