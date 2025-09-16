import os
import io
import html
import json
import time
import datetime
import requests
import webbrowser
import urllib.parse
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build



def retrieve_history(date_iso):

    # Retrieve page
    selected_date = datetime.date.fromisoformat(date_iso)
    url = (
        "https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/"
        + selected_date.strftime("%B")
    )
    headers = {
        'User-Agent': 'DailyBulletinUWCAC/1.0 (https://albertttan.github.io/daily-bulletin-uwcac/) python-requests/2.31.0'
    }
    soup = BeautifulSoup(requests.get(url, headers=headers, timeout=10).text, "html.parser")
    date_name = soup.find_all("a", title=selected_date.strftime("%B %-d"))[0 if selected_date.day == 1 else 1].parent.parent
    date_history = date_name.find_next("ul").find_all("li")

    # Clean results
    for element in date_history:
        for link in element.find_all("a"):
            link["href"] = "https://en.wikipedia.org" + link["href"]
        for italics in element.find_all("i"):
            if italics.text.startswith("("):
                italics.decompose()

    return date_history


def google_credentials():
    creds = None
    SCOPES = ["https://www.googleapis.com/auth/documents.readonly", 
              "https://www.googleapis.com/auth/drive.readonly", 
              "https://www.googleapis.com/auth/drive.metadata.readonly"]

    # Retrieve credentials from file
    if os.path.exists("google-auth/token.json"):
        with open("google-auth/token.json") as file:
            token = json.load(file)
        creds = Credentials.from_authorized_user_info(token)
    
    # Log in and save credentials if invalid
    if not creds or not creds.valid:
        try:
            creds.refresh(Request())
        except: 
            os.system("defaultbrowser safari")
            time.sleep(5)
            flow = InstalledAppFlow.from_client_secrets_file(
                "google-auth/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            os.system("defaultbrowser firefox")
        with open("google-auth/token.json", "w") as token:
            token.write(creds.to_json())
    
    return creds


def retrieve_news_ap():

    # Retrieve page
    url = "https://apnews.com/world-news"
    soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
    output = []

    # Locate headings
    for element in soup.find_all("div", class_="PagePromo-content"):
        heading = element.find("h3")
        if heading and heading.find("a"):
            output.append(heading.find("a"))
    
    # Clean results
    for element in output:
        del element["class"]
        element.find("span").unwrap()

    output.append(False)
    return output


def retrieve_news(document_id="1ChvbzaBUOMUft4mUmKghzQpI_VnBbOUsBHGxbfyed4w"):
    creds = google_credentials()
    service = build("drive", "v3", credentials=creds)

    # Check if file is up-to-date
    with open("google-auth/timestamp.txt") as file:
        last_timestamp = file.read()
    current_timestamp = service.files().get(fileId=document_id, fields="modifiedTime").execute()["modifiedTime"]
    if current_timestamp == last_timestamp:
        return retrieve_news_ap()

    # Retrieve document content as HTML
    request = service.files().export_media(fileId=document_id, mimeType="text/html")
    soup = BeautifulSoup(request.execute().decode('utf-8'), "html.parser")
    
    # Clean formatting
    output = []
    for element in soup.find("ul"):
        del element["style"]
        element.find("span").unwrap()
        link = element.find("a")
        if link:
            del link["style"]
            link["href"] = urllib.parse.parse_qs(urllib.parse.urlparse(link.get("href", "")).query).get("q", [""])[0]
        output += element.contents
    
    output.append(current_timestamp)
    return output
