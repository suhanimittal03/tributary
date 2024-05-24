import requests as requests

data = {
    "engine_temperature": 0.2,
}

response = requests.post("http://tributary:8000/record", json=data)
print(response.content)
res = requests.post("http://tributary:8000/collect")
print(res)