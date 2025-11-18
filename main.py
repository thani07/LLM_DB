# main.py
import os
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# load env
load_dotenv()

# LLM imports (same as your original file)
from langchain_groq import ChatGroq

# DB imports
from database import SessionLocal, engine, Base
import models, crud, schemas

# create tables if missing
Base.metadata.create_all(bind=engine)

# initialize LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY not set. LLM calls may fail.")

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.7
)

app = FastAPI(title="Chatbot + History API")

# CORS (adjust origins as needed for your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origin(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency - DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Root
@app.get("/")
def root():
    return {"message": "Welcome to Chatbot API with History"}


# Chat endpoint (saves history)
@app.post("/chat")
async def chat_endpoint(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    user_msg = request.user_input
    # call LLM
    response = llm.invoke(user_msg)
    # save to history
    crud.create_history(db=db, query=user_msg, response=str(response), endpoint="chat")
    return {"response": response}


# Summarize (saves history)
@app.post("/summarize")
async def summarize_endpoint(request: schemas.SummaryRequest, db: Session = Depends(get_db)):
    user_msg = request.text
    prompt = f"Summarize the following text clearly and concisely:\n\n{user_msg}"
    response = llm.invoke(prompt)
    crud.create_history(db=db, query=user_msg, response=str(response), endpoint="summarize")
    return {"summary": response}


# Translate (saves history)
@app.post("/translate")
async def translate_endpoint(request: schemas.TranslationRequest, db: Session = Depends(get_db)):
    user_msg = request.text
    target_language = request.target_Language
    prompt = f"Translate the following text to {target_language}:\n\n{user_msg}"
    response = llm.invoke(prompt)
    crud.create_history(db=db, query=user_msg, response=str(response), endpoint=f"translate:{target_language}")
    return {"translation": response}


# Sentiment (saves history)
@app.post("/sentiment")
async def sentiment_endpoint(request: schemas.SentimentRequest, db: Session = Depends(get_db)):
    user_msg = request.text
    prompt = f"Analyze the sentiment of the following text and respond with Positive, Negative, or Neutral:\n\n{user_msg}"
    response = llm.invoke(prompt)
    crud.create_history(db=db, query=user_msg, response=str(response), endpoint="sentiment")
    return {"sentiment": response}


# History endpoints
@app.get("/history", response_model=list[schemas.HistoryItem])
def read_history(limit: int = Query(20, ge=1, le=200), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    items = crud.get_history(db=db, limit=limit, offset=offset)
    return items

@app.get("/history/{item_id}", response_model=schemas.HistoryItem)
def read_history_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_history_by_id(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/history/{item_id}")
def delete_history_item(item_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_history(db=db, item_id=item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"deleted": True}
