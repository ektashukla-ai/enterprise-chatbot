# 🧠 Enterprise RAG Chatbot Microservice (LangChain + FAISS + FastAPI)

This project is a production-style Retrieval-Augmented Generation (RAG) microservice using:
- **LangChain** for chaining retrieval + generation
- **FAISS** as the vector database
- **OpenAI** for embedding + language model
- **FastAPI** for serving queries via API

Built and structured like a microservice that can scale to enterprise usage.

---

## ✅ Features

- 🗂️ Document ingestion and chunking
- 🔍 Vector search over embedded content (FAISS)
- 🤖 GPT-3.5-Turbo-based RAG response
- 🧾 Source citation in answers
- ⚙️ API-first architecture via FastAPI
- 📁 Local PDF upload and embedding endpoint
- 🗣️ Human feedback collection with /feedback
- 📊 Evaluation logging for every query

---

## 📌 Tech Stack

| Layer         | Tool/Library         |
|---------------|----------------------|
| LLM           | OpenAI GPT-3.5       |
| Embeddings    | OpenAI ADA v2        |
| Retrieval     | FAISS (local vector DB) |
| API Framework | FastAPI              |
| Infra         | Python 3.10+, Uvicorn |

---

## 🔁 Workflow Diagram

```text
User Query ➜ FastAPI ➜ Retrieve top-k chunks from FAISS ➜ Inject into Prompt ➜ OpenAI LLM ➜ Final Answer ➜ API Response with Sources

                    ┌───────────────┐
                    │   PDF Upload  │
                    └──────┬────────┘
                           ↓
                    ┌───────────────┐
                    │ Chunk + Embed │◄─────────────┐
                    └──────┬────────┘              │
                           ↓                       │
                   ┌──────────────┐                │
User Query ──────► │   FAISS DB   │ ── Top-K Match │
                   └─────┬────────┘                ↓
                         ↓                ┌────────────────┐
                     Inject in Prompt ──► │ GPT (OpenAI)   │
                                          └─────┬──────────┘
                                                ↓
                                          Final Answer
```

---

## 📥 API Endpoints

### 🔹 1. `/ask` – Ask a Question
```http
POST /ask
Content-Type: application/json

{
  "query": "What is retrieval-augmented generation?"
}
```
**Returns:**
```json
{
  "answer": "...",
  "sources": [{ "source": "page: 3", "file": "data_science_guide.pdf" }]
}
```

---

### 🔹 2. `/upload` – Upload and Embed New PDFs
```http
POST /upload
Content-Type: multipart/form-data

form-data:
  file: <your_pdf_file.pdf>
```
📍 Automatically:
- Saves to `data/docs/`
- Loads, chunks, embeds
- Appends to FAISS index

**Returns:**
```json
{
  "message": "File uploaded and embedded successfully.",
  "filename": "your_pdf_file.pdf"
}
```

---

### 🔹 3. `/feedback` – Submit User Feedback
```http
POST /feedback
Content-Type: application/json

{
  "query": "What is RAG?",
  "answer": "RAG stands for...",
  "correct": true,
  "comment": "Helpful but missing recent updates."
}
```
📁 Saves feedback to `feedback.csv`

---

## 📊 Evaluation Techniques

### 1. **Retrieval Logging**
- Logs `top_k` documents retrieved per query
- Metadata includes page number, source file

### 2. **Answer Traceability**
- Answer includes source document metadata
- Helps verify hallucinations and grounding

### 3. **Fallback Detection**
- If no relevant chunks, returns fallback answer or low-confidence message

### 4. **Manual Feedback Endpoint**
- Logged to `feedback.csv`
- Enables offline scoring + model improvement loop

---

## 🐳 Dockerfile (for local or cloud deployment)
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "app/main.py"]
```

Build and run:
```bash
docker build -t rag-bot .
docker run -p 8000:8000 rag-bot
```

---

## 🧠 Suggestions for Enterprise-Readiness

| Need                          | How to Add                         |
|-------------------------------|------------------------------------|
| 🔐 Auth for Upload/Query      | Add JWT + API Key auth             |
| 📈 Monitoring / Logs          | Integrate with Prometheus + Grafana|
| ⏱️ Rate Limiting              | Use FastAPI middleware             |
| 🧠 LLM Evaluation             | Add BLEU, ROUGE metrics on answers |
| 🗃️ Streaming Support          | Enable OpenAI stream=True          |
| 🧪 Testing / CI               | Add pytest + GitHub Actions        |
| 🐳 Deployment                 | Add Docker + Docker Compose        |

---

## 🔧 TODOs for Next Iteration
- [ ] Switch to `LlamaIndex` for modularity + hybrid search
- [ ] Host LLM using SageMaker endpoint
- [ ] Add persistent database (Postgres) for logging queries
- [ ] Support long-context documents (use chunk re-ranking)

---

## 🙌 Credits
Built with 💡 by [@ekta-shukla] — for GenAI microservices that scale.
