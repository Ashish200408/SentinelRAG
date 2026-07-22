import requests
import json
import time

URL = "http://127.0.0.1:8000/api/v1/chat/query"

print("1. Empty question:")
resp = requests.post(URL, json={"question": "   "})
print(resp.status_code, resp.json())
print()

print("2. Irrelevant query:")
resp = requests.post(URL, json={"question": "What is the capital of Mars?"})
print(resp.status_code, resp.json())
print()

print("3. Valid query (assuming there's a document indexed):")
resp = requests.post(URL, json={"question": "What are the features of SentinelRAG?"})
print(resp.status_code, resp.json())
print()

