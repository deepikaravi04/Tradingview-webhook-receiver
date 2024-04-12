import sqlite3
from fastapi import FastAPI, BackgroundTasks
import requests

# Create an instance of FastAPI
app = FastAPI()

# Create a connection to the SQLite database
DATABASE_FILE = "./test.db"

# Create a table for endpoint URLs if it doesn't exist
with sqlite3.connect(DATABASE_FILE) as connection:
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS endpoint_urls (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT)")

# Create a table if it doesn't exist
with sqlite3.connect(DATABASE_FILE) as connection:
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS webhook_data (id INTEGER PRIMARY KEY AUTOINCREMENT, payload TEXT)")

# Define a route for the /hello endpoint
@app.get("/")
async def read_root():
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()
        # Retrieve payloads from the database
        cursor.execute("SELECT payload FROM webhook_data")
        payloads = cursor.fetchall()
    return {"message": "Hello, FastAPI!", "payloads": payloads}

# Define a route to receive webhook requests
@app.post("/webhook")
async def receive_webhook(background_tasks: BackgroundTasks, payload: dict):
    print("Received webhook payload:", payload)
    # Background task to send a response to the sender of the webhook
    background_tasks.add_task(send_response, payload)
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()
        # Execute SQL query to insert payload into the database
        cursor.execute("INSERT INTO webhook_data (payload) VALUES (?)", (str(payload),))
        connection.commit()
    return {"message": "Payload saved successfully"}

# Function to send a response to the sender of the webhook
def send_response(payload):
    # Replace this URL with the endpoint you want to send the response to
    endpoint_url = "https://aac0-2409-40f4-1029-e0e5-25c5-27c0-cfd8-b0a1.ngrok-free.app/desktop_webhook"
    
    # Send a POST request with the payloadhttps://ee1d-2409-40f4-1029-e0ehttps://ee1d-2409-40f4-1029-e0e5-25c5-27c0-cfd8-b0a1.ngrok-free.app5-25c5-27c0-cfd8-b0a1.ngrok-free.app
    response = requests.post(endpoint_url, json=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        print("Response sent successfully")
    else:
        print("Failed to send response. Status code:", response.status_code)
