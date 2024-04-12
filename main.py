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
    cursor.execute("CREATE TABLE IF NOT EXISTS endpoint_urls (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, desktop_url TEXT)")

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


@app.post("/endpoint_webhook")
async def receive_endpoint_webhook(background_tasks: BackgroundTasks, payload: dict):
    print("Received endpoint webhook payload:", payload)
    # Background task to save endpoint URLs to the database
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()
        # Execute SQL query to insert payload into the database
        cursor.execute("INSERT INTO endpoint_urls (username, desktop_url) VALUES (?, ?)", (str(payload.get("username")), str(payload.get("desktop_url"))))
        connection.commit()
    return {"message": "Endpoint URL saved successfully"}




# Function to send a response to all URLs stored in the database
def send_response(payload):
    # Retrieve all URLs from the database
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT desktop_url FROM endpoint_urls")
        urls = cursor.fetchall()

    # Iterate over each URL and send a POST request
    for url in urls:
        forward_url = url[0] + "/desktop_webhook" # Extract URL from the tuple
        response = requests.post(forward_url, json=payload)
        if response.status_code == 200:
            print(f"Response sent successfully to {forward_url}")
        else:
            print(f"Failed to send response to {forward_url}. Status code:", response.status_code)
