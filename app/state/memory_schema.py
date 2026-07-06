from pydantic import BaseModel


class MemoryDecision(BaseModel):

    should_store: bool

    memory_text: str