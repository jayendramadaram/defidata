import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()
url = os.getenv('API_CALL_URL')

resp = requests.get(url)
json_object = json.dumps(json.loads(resp.text), indent=4)
with open('data.json', 'w') as file:
    file.write(json_object)
