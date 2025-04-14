import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
USERNAME = os.getenv("CONFLUENCE_USERNAME")
API_KEY = os.getenv("CONFLUENCE_API_KEY")

def fetch_confluence_pages():
    url = f"{BASE_URL}/rest/api/content?type=page&expand=body.storage"
    auth = (USERNAME, API_KEY)
    response = requests.get(url, auth=auth, headers={"Accept": "application/json"})

    if response.status_code != 200:
        print(f"Failed to fetch pages: {response.status_code}")
        return {}

    data = response.json()
    pages = {page['title']: page['body']['storage']['value'] for page in data.get('results', [])}
    return pages
