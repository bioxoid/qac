import requests
import numpy as np

json = {
  "name": "orion",
  "description": "hero",
  "image": []
}

response = requests.post('http://localhost:8000/', json=json )
print(response.text)