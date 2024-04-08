import requests

# Define the data to be sent in the POST request
data = {
    "symbol": "AAPL",
    "price": 150.25,
    "volume": 1000.0
}

# Define the URL of your FastAPI application
url = "http://127.0.0.1:8000/webhook"  # Update with your server's URL

# Send the POST request
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    print("Webhook successfully sent")
else:
    print("Failed to send webhook. Status code:", response.status_code)
    print("Response content:", response.text)
