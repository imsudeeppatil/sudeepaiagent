from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Union
import re

from database import SessionLocal, init_db
from models import AgentRequest, AgentResponse, ErrorResponse
from tools import tool_calculate, tool_save_memory, tool_get_memory

app = FastAPI(title="Sudeep's Baarez Agent")
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def parse_math(text):
    text = text.lower()
    text = text.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("x", "*")
    text = re.sub(r"[^0-9+\-*/().]", " ", text)  # keep only math symbols
    text = re.sub(r"\s+", " ", text).strip()
    return text if text else None


def parse_save(text):
    text = text.lower()
    if "remember my" in text and " is " in text:
        part = text.split("remember my")[1]
        key, value = part.split(" is ", 1)
        return key.strip(), value.strip()
    return None, None

def parse_get(text):
    text = text.lower()
    if "what is my" in text:
        key = text.split("what is my")[1]
        return key.replace("?", "").strip()
    return None


@app.post("/agent/query", response_model=Union[AgentResponse, ErrorResponse])
def agent_query(req: AgentRequest, db: Session = Depends(get_db)):
    p = req.prompt.lower()

    if "remember" in p or "save" in p:
        key, val = parse_save(req.prompt)
        return AgentResponse(
            original_prompt=req.prompt,
            chosen_tool="memory_write",
            tool_input=f"{key} = {val}",
            response=tool_save_memory(db, key, val)
        )

    if "what is my" in p or "recall" in p:
        key = parse_get(req.prompt)
        return AgentResponse(
            original_prompt=req.prompt,
            chosen_tool="memory_read",
            tool_input=key,
            response=tool_get_memory(db, key)
        )

    if "what is" in p or "calculate" in p:
        expr = parse_math(req.prompt)
        return AgentResponse(
            original_prompt=req.prompt,
            chosen_tool="calculator",
            tool_input=expr,
            response=tool_calculate(expr)
        )

    return ErrorResponse(error="I do not have a tool for that.")
