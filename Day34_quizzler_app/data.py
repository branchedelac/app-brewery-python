import requests

parameters = {"amount": 10,
              "type": "boolean",
              "category": 20}

url = f"https://opentdb.com/api.php"
response = requests.get(url, params=parameters)
response.raise_for_status()
question_data = response.json()["results"]