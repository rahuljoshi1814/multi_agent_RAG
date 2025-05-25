from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.agents.schema_agent import extract_schema_info
from app.agents.sql_generator_agent import generate_sql
from app.agents.retriever_agent import execute_query
from app.agents.synthesizer_agent import synthesize_answer
from app.vector_agent import fallback_answer  # ✅ Fallback RAG
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Query(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
def ask(query: Query):
    question = query.question

    # Step 1: Schema Agent
    schema = extract_schema_info(question)

    # Step 2: Fallback if no schema match at all
    if not schema:
        answer = fallback_answer(question)
        return {
            "answer": answer,
            "intermediate_steps": {
                "schema": [],
                "sql_query": None,
                "result": None,
                "fallback": True,
                "fallback_reason": "no_schema_match"
            }
        }

    try:
        # Step 3: SQL Generator
        sql_query = generate_sql(question, schema)

        # Step 4: Retriever
        result = execute_query(sql_query)

        # Step 5: Check if result is empty
        if not result.get("rows"):
            raise ValueError("Empty result from SQL")

        # Step 6: Synthesizer
        answer = synthesize_answer(question, result)

        return {
            "answer": answer,
            "intermediate_steps": {
                "schema": schema,
                "sql_query": sql_query,
                "result": result,
                "fallback": False
            }
        }

    except Exception as e:
        # Step 7: Final fallback
        answer = fallback_answer(question)
        return {
            "answer": answer,
            "intermediate_steps": {
                "schema": schema,
                "sql_query": sql_query if 'sql_query' in locals() else None,
                "result": result if 'result' in locals() else None,
                "fallback": True,
                "fallback_reason": str(e)
            }
        }
