#  Multi-Agent RAG System for Natural Language Querying of a Relational Database

###  Objective
This project implements a **Multi-Agent Retrieval-Augmented Generation (RAG)** system that allows users to ask **natural language questions**, translates them to **PostgreSQL SQL queries**, and returns human-readable answers via a web interface and API.

---

##  Features
- Natural language question answering over a structured PostgreSQL database
- Modular multi-agent pipeline:
  - **Schema Agent** → Identifies relevant tables
  - **SQL Generator Agent** → Generates SQL based on patterns
  - **Retriever Agent** → Executes SQL and fetches results
  - **Synthesizer Agent** → Converts rows into a readable answer
  - **Vector Fallback Agent** → Uses semantic search if SQL path fails
- Web interface + FastAPI docs
- Hybrid RAG: combines SQL and Vector Retrieval
- Secure `.env` usage and render-ready `render.yaml`
- Deployed on Render with PostgreSQL on Railway

##  System Architecture

User Question
↓
+--------------------+
| Web/API Layer |
+--------------------+
↓
Schema Agent → SQL Generator → Retriever → Synthesizer → Answer
↓
[if failed]
↓
Vector Retriever → Synthesizer → Answer


## 🗃️ Database Schema

PostgreSQL schema includes 5 interrelated tables:
- `customers(id, name, email, created_at)`
- `products(id, name, category, price)`
- `employees(id, name, role, department, hire_date)`
- `projects(id, name, description, start_date, end_date)`
- `sales(id, customer_id, product_id, employee_id, amount, sale_date)`

##  Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/multi-agent-rag.git
cd multi-agent-rag

### 2. Create the PostgreSQL database
Run the schema file: 
- Create a new DB (e.g., in pgAdmin or Railway)
- Run init_db.sql to create tables


### 3. Install dependencies
- pip install -r requirements.txt

### 4. Create .env file
- DATABASE_URL=postgres://your_user:your_pass@your_host:5432/your_db

### 5. Populate with fake data
- python populate_mock_data.py

### 6. Start the FastAPI server
uvicorn app.main:app --reload

### 7. Visit the web interface
Go to: http://localhost:8000

### 8. API Endpoint
POST /ask
Input: {
  "question": "Who spent the most last year?"
}

Output: {
  "answer": "Answer: Alice Smith, 15000.50",
  "intermediate_steps": {
    "schema": ["customers", "sales"],
    "sql_query": "...",
    "result": {
      "columns": ["name", "total"],
      "rows": [["Alice Smith", 15000.50]]
    }
  }
}

## Vector Fallback Mode

Example:
{
  "question": "Who spent the most in Q1?"
}

Returns from fallback document:
"Alice Smith spent the most in Q1 2023, totaling $15,000."


When the system can't determine relevant schema, it falls back to ChromaDB vector search using sentence-transformer embeddings

## Error Handling
- Unknown schema → Schema agent returns empty
- Invalid SQL → Catch and display message
- No results → “No data found.”

## Environment Variables Required

Set in .env (locally) or render.yaml (for Render deployment)::

```env
DATABASE_URL=postgres://your_user:your_pass@your_host:5432/your_db
 
 ## Live Demo
 - https://multi-agent-rag.onrender.com 
 Test the /ask endpoint or try your questions in the web interface.

