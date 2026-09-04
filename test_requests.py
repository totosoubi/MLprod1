import requests


response = requests.post(
    "http://127.0.0.1:8000/predict",
    json={"size": 120, "nb_rooms": 3, "garden": 1},
    timeout=10,
)
response.raise_for_status()
print(response.json())
