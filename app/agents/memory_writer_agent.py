from app.memory.memory_store import save_memory
from app.services.gemini_service import llm
from app.state.memory_schema import MemoryDecision

def memory_writer_agent(user_message: str):
    structured_llm = llm.with_structured_output(MemoryDecision)
    result = structured_llm.invoke(
        f"""
        Decide whether this message contains
        a long-term user preference.

        Message:
        {user_message}

        Examples worth remembering:

        - travel preferences
        - food preferences
        - activity preferences
        - budget preferences

        Examples NOT worth remembering:

        - greetings
        - temporary requests
        - small talk
        """
    )
    if result.should_store:
        save_memory(result.memory_text)
        
    return result
    

    
