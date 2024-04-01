import requests
import os

url = "https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app"
access_token = os.getenv("ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

payload = {
    "source_language": "Luganda",
    "target_language": "English",
    "text": "Yakoma mu S.4 era agamba talina buzibu nabuyigirize bwa musajja.",
}

response = requests.post(f"{url}/tasks/translate", headers=headers, json=payload)

if response.status_code == 200:
    translated_text = response.json()["text"]
    print("Translate text:", translated_text)
else:
    print("Error:", response.status_code, response.text)
