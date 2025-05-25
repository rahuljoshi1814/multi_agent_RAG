#  Multi-Agent RAG System for Natural Language Querying of a Relational Database

##  Objective

This project implements a **Multi-Agent Retrieval-Augmented Generation (RAG)** system that allows users to ask **natural language questions**, which are interpreted, translated into **SQL queries**, executed on a **PostgreSQL database**, and returned as **human-readable answers**.

##  Features

-  Natural language question answering over structured relational data
-  Multi-Agent architecture:
  - **Schema Agent** – Detects relevant tables
  - **SQL Generator Agent** – Builds SQL queries from questions
  - **Retriever Agent** – Executes SQL and fetches data
  - **Synthesizer Agent** – Converts raw results into readable answers
  - **Vector Fallback Agent** – Uses semantic search if SQL fails
-  Supports filtering, aggregation, joins, and temporal queries
-  FastAPI backend with web UI and `/docs` interface
-  Hybrid RAG: Structured (SQL) + Unstructured (Vector) handling
-  Secure `.env` and production-ready deployment with `render.yaml`
-  Hosted on Render with PostgreSQL from Railway

---

##  System Architecture

```text
User → Web/API → Schema Agent → SQL Agent → Retriever → Synthesizer → Answer
                                            ↓
                                  (if SQL fails)
                                            ↓
                              Vector Agent → Synthesizer → Answer
```

---

##  Database Schema

PostgreSQL schema includes 5 interrelated tables:

- `customers(id, name, email, created_at)`
- `products(id, name, category, price)`
- `employees(id, name, role, department, hire_date)`
- `projects(id, name, description, start_date, end_date)`
- `sales(id, customer_id, product_id, employee_id, amount, sale_date)`

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/rahuljoshi1814/multi_agent_RAG.git
cd multi_agent_RAG
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure PostgreSQL

- Create a PostgreSQL DB (e.g., using Railway or pgAdmin)
- Run `init_db.sql` to initialize schema

### 4. Add `.env` File

Create a `.env` file in the root with:

```env
DATABASE_URL=postgres://your_user:your_pass@your_host:5432/your_db
```

### 5. Populate Database

```bash
python populate_mock_data.py
```

### 6. Run the App Locally

```bash
uvicorn app.main:app --reload
```

Visit: [http://localhost:8000](http://localhost:8000)  
Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

##  API Usage

### Endpoint

```http
POST /ask
```

### Sample Request

```json
{
  "question": "Who spent the most last year?"
}
```

### Sample Response

```json
{
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
```

---

##  Vector Fallback Mode (ChromaDB)

If the schema agent cannot find matching tables, the system falls back to **semantic similarity** using `SentenceTransformer` and `ChromaDB`.

### Example

```json
{
  "question": "Who spent the most in Q1?"
}
```

### Response (Fallback)

```json
{
  "answer": "Alice Smith spent the most in Q1 2023, totaling $15,000.",
  "fallback": true
}
```

---

##  Sample Queries

###  SQL-Based Queries

- What is the total sales?
- What was the total sales last year?
- Who are the top customers last year?
- What department had the lowest sales?
- List top 5 products by revenue.

###  Vector Fallback Queries

- Who spent the most in Q1?
- Which category dropped in Q4 2023?
- Who is the top customer in electronics?
- What was the biggest expense in 2022?
- Tell me about Q1 sales behavior.

---

##  Error Handling

- Schema not found → fallback triggered
- Invalid SQL → graceful failure message
- No records found → “No data found.”

---

##  Environment Variables

Set these in `.env` (locally) or in Render environment settings:

```env
DATABASE_URL=postgres://your_user:your_pass@your_host:5432/your_db
```

---

##  Live Demo

You can test the live version here:

 **[https://multi-agent-rag.onrender.com](https://multi-agent-rag.onrender.com)**  
 API Docs: [https://multi-agent-rag.onrender.com/docs](https://multi-agent-rag.onrender.com/docs)

---

##  Author

**Rahul Joshi**  
GitHub: [@rahuljoshi1814](https://github.com/rahuljoshi1814)
