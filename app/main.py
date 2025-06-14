import csv
import datetime

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from app.rag_pipeline import answer_query
from app.loader import load_documents, split_documents
from app.embeddings import create_vectorstore
from pathlib import Path
import uvicorn

app = FastAPI()

UPLOAD_DIR  = Path("data/docs")

class QueryRequest(BaseModel):
    query: str

class FeedbackRequest(BaseModel):
    query: str
    answer: str
    correct: str
    comment: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = UPLOAD_DIR / file.filename
    with open(file_location, "wb") as f:
        f.write(await file.read())

    docs = load_documents(str(UPLOAD_DIR))
    chunks = split_documents(docs)
    create_vectorstore(chunks)

    return {"message": "File Uploaded and embedded successfully",
            "filename": file.filename}

@app.post("/ask")
async def ask_query(request: QueryRequest):
    response = answer_query(request.query)
    return {
        "answer": response['result'],
        "sources": [doc.metadata for doc in response['source_documents']]
    }

@app.post("/feedback")
async def feedback(request: FeedbackRequest):
    with open("feedback.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.datetime.now().isoformat(),
            request.query,
            request.answer,
            request.correct,
            request.comment,
        ])
        return {"message":"Feedback saved successfully"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
