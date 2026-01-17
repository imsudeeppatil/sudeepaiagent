import ast
import operator
from sqlalchemy.orm import Session
from database import Memory

# ---------- MEMORY TOOLS ----------

def tool_save_memory(db: Session, key: str, value: str) -> dict:
    item = db.query(Memory).filter(Memory.key == key).first()
    if item:
        item.value = value
    else:
        item = Memory(key=key, value=value)
        db.add(item)
    db.commit()
    return {"message": "Memory saved", "key": key, "value": value}

def tool_get_memory(db: Session, key: str) -> dict:
    item = db.query(Memory).filter(Memory.key == key).first()
    if not item:
        return {"error": "No memory found for this key"}
    return {"key": key, "value": item.value}

# ---------- CALCULATOR TOOL ----------

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def safe_eval(expr):
    def eval_node(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.BinOp):
            return ALLOWED_OPERATORS[type(node.op)](
                eval_node(node.left),
                eval_node(node.right)
            )
        raise ValueError("Invalid expression")

    tree = ast.parse(expr, mode='eval')
    return eval_node(tree.body)

def tool_calculate(expression: str) -> dict:
    try:
        result = safe_eval(expression)
        return {"result": result}
    except Exception:
        return {"error": "Invalid expression"}
