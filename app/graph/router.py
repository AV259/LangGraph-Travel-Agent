from app.state.travel_state import TravelState

def should_continue(state: TravelState):
    
    if state["missing_fields"]:
       return "need more info"
    return "continue"
