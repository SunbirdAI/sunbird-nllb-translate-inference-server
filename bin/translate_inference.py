import requests
import os
from pprint import PrettyPrinter

pprint = PrettyPrinter(indent=2)


# URL for the endpoint
ENDPOINT = os.getenv("ENDPOINT_ID")
url = f"https://api.runpod.ai/v2/{ENDPOINT}/runsync"

# Authorization token (replace 'RUNPOD_API_KEY' with your actual token)
token = os.getenv("RUNPOD_API_KEY")

# Data to be sent in the request body
data = {
    "input": {
        "source_language": "lug",
        "target_language": "eng",
        "text": "Ekibiina ekiddukanya omuzannyo gw’emisinde mu ggwanga ekya Uganda Athletics Federation kivuddeyo nekitegeeza nga lawundi esooka eyemisinde egisunsulamu abaddusi abanakiika mu mpaka ezenjawulo ebweru w’eggwanga egya National Athletics Trials nga bwegisaziddwamu.",
    }
}

# Headers with authorization token
headers = {"Authorization": f"{token}", "Content-Type": "application/json"}

# Sending POST request
response = requests.post(url, headers=headers, json=data)

# Checking response status
if response.status_code == 200:
    print("Request successful")
    print("Response:")
    pprint.pprint((response.json()))  # Print response content
else:
    print("Request failed with status code:", response.status_code)
    print("Response:")
    print(response.text)  # Print error message
