# AI Agent Brain – FastAPI POC

## Setup

python -m venv venv  
venv\Scripts\activate  
pip install -r requirements.txt  

## Run API

uvicorn main:app --reload

Open: http://127.0.0.1:8000/docs

## Test Prompts

POST /agent/query

1) Calculator
{
 "prompt": "What is 10 plus 5"
}

2) Save Memory
{
 "prompt": "Remember my cat's name is Fluffy"
}

3) Recall Memory
{
 "prompt": "What is my cat's name?"
}

## Security Note
Calculator avoids eval() and uses Python AST parsing to prevent arbitrary code execution.
