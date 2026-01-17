from pydantic import BaseModel

class AgentRequest(BaseModel):
    prompt: str

class AgentResponse(BaseModel):
    original_prompt: str
    chosen_tool: str
    tool_input: str
    response: dict

class ErrorResponse(BaseModel):
    error: str
