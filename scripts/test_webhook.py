import requests

url = "http://localhost:8000/webhook/leads"
payload = {
    "email": "hello@anthropic.com",
    "name": "Anthropic AI",
    "source": "website"
}
response = requests.post(url, json=payload)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

url_get = "http://localhost:8000/leads"
response_get = requests.get(url_get)
print("\n--- All Leads ---")
print(response_get.json())
