from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class Signal(Base):
    __tablename__ = "signals"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    price = Column(Float)
    volume = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

class WebhookData(BaseModel):
    symbol: str
    price: float
    volume: float

@app.post('/webhook')
async def webhook(data: WebhookData):
    db = SessionLocal()
    try:
        signal = Signal(symbol=data.symbol, price=data.price, volume=data.volume)
        db.add(signal)
        db.commit()
        db.refresh(signal)
    finally:
        db.close()
    return {"message": "Webhook received successfully"}

@app.get("/")
async def read_root():
    db = SessionLocal()
    signals = db.query(Signal).all()
    db.close()
    return signals

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
