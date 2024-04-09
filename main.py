import sqlite3
from fastapi import FastAPI

# Create an instance of FastAPI
app = FastAPI()

# Create a connection to the SQLite database
DATABASE_FILE = "./test.db"

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
async def receive_webhook(payload: dict):
    with sqlite3.connect(DATABASE_FILE) as connection:
        cursor = connection.cursor()
        # Execute SQL query to insert payload into the database
        cursor.execute("INSERT INTO webhook_data (payload) VALUES (?)", (str(payload),))
        connection.commit()
    return {"message": "Payload saved successfully"}
