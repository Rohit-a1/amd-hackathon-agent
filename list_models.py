import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("FIREWORKS_API_KEY")

if not API_KEY or API_KEY == "YAHAN_APNI_KEY_PASTE_KAREIN":
    print("API Key is missing or invalid.")
    exit(1)

url = "https://api.fireworks.ai/inference/v1/models"
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {API_KEY}"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    models = response.json().get("data", [])
    print(f"Total models found: {len(models)}")
    print("\n--- List of Available Models ---")
    for m in models:
        # Print only a few relevant ones or all
        name = m.get("id")
        if "llama" in name.lower() or "kimi" in name.lower() or "minimax" in name.lower() or "qwen" in name.lower():
            print(name)
else:
    print(f"Failed to fetch models. Status Code: {response.status_code}")
    print(response.text)
