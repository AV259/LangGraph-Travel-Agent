from app.state.travel_state import TravelState
from app.memory.memory_store import retrieve_memory

def memory_agent(state: TravelState):
    query = state['user_input']

    memories = retrieve_memory(query)

    state["memory_context"] = memories

    return state

