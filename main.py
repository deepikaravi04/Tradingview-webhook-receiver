from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = FastAPI()

# SQLite database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a model for the received payloads
class WebhookPayload(Base):
    __tablename__ = "webhook_payloads"

    id = Column(Integer, primary_key=True, index=True)
    payload = Column(String, index=True)
    received_at = Column(DateTime, default=datetime.utcnow)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

@app.post("/webhook")
async def receive_webhook(payload: str):
    try:
        # Store the received payload in the database
        db = SessionLocal()
        db_payload = WebhookPayload(payload=payload)
        db.add(db_payload)
        db.commit()
        db.refresh(db_payload)
        db.close()

        # Print the received payload
        print("Received webhook payload:", payload)
        return {"message": "Webhook received and stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
