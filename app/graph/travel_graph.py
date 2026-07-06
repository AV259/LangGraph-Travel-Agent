from app.agents.activity_agent import activity_agent
from app.agents.restaurant_agent import restaurant_agent
from app.agents.trip_intake_agent import trip_intake_agent
from app.state.travel_state import TravelState
from app.graph.router import should_continue
from app.agents.follow_up_agent import follow_up_agent
from langgraph.checkpoint.memory import MemorySaver
from app.agents.memory_agent import memory_agent
from app.agents.destination_agent import destination_agent
from app.agents.destination_display_agent import destination_display_agent
from app.agents.flight_agent import flight_agent
from app.agents.flight_advisor_agent import flight_advisor_agent
from app.agents.flight_selection_agent import flight_selection_agent
from app.agents.hotel_agent import hotel_agent
from app.agents.hotel_selection_agent import hotel_selection_agent
from app.agents.hotel_advisor_agent import hotel_advisor_agent
from app.agents.multi_destination_hotel_agent import multi_destination_hotel_agent
from app.agents.transport_suggestion_agent import transport_suggestion_agent
from app.agents.budget_agent import budget_agent
from app.agents.budget_decision_agent import budget_decision_agent
from app.agents.budget_advisor_agent import budget_advisor_agent
from app.graph.budget_status_router import budget_status_router
from app.agents.budget_update_agent import budget_update_agent
from app.agents.itinerary_agent import itinerary_agent
from app.agents.itinerary_formatter_agent import itinerary_formatter_agent


from langgraph.graph import StateGraph, START, END

memory = MemorySaver()
graph_builder = StateGraph(TravelState)

graph_builder.add_node(
    "trip_intake",
    trip_intake_agent
)
graph_builder.add_edge(
    START,
    "trip_intake"
)
graph_builder.add_node(
    "follow_up",
    follow_up_agent
)
graph_builder.add_node(
    "memory",
    memory_agent
)
graph_builder.add_node(
    "destination",
    destination_agent
)
graph_builder.add_node(
    "activity",
    activity_agent
)
graph_builder.add_node(
    "restaurant",
    restaurant_agent
)
graph_builder.add_node(
    "destination_display",
    destination_display_agent
)
graph_builder.add_node(
    "flight",
    flight_agent
)
graph_builder.add_node(
    "flight_advisor",
    flight_advisor_agent
)
graph_builder.add_node(
    "flight_selection",
    flight_selection_agent
)
graph_builder.add_node(
    "hotel",
    hotel_agent
)
graph_builder.add_node(
    "hotel_selection",
    hotel_selection_agent
)
graph_builder.add_node(
    "hotel_advisor",
    hotel_advisor_agent
)
graph_builder.add_node(
    "multi_destination_hotel",
    multi_destination_hotel_agent
)
graph_builder.add_node(
    "transport_suggestion",
    transport_suggestion_agent
)
graph_builder.add_node(
    "budget",
    budget_agent
)
graph_builder.add_node(
    "budget_decision",
    budget_decision_agent
)
graph_builder.add_node(
    "budget_advisor",
    budget_advisor_agent
)
graph_builder.add_node(
    "budget_update",
    budget_update_agent
)
graph_builder.add_node(
    "itinerary",
    itinerary_agent
)
graph_builder.add_node(
    "itinerary_formatter",
    itinerary_formatter_agent
)

graph_builder.add_conditional_edges(
    "trip_intake",
    should_continue,
    {
        "need more info": "follow_up",
        "continue": "memory"
    }
)
graph_builder.add_edge(
    "follow_up",
    "trip_intake"
)

graph_builder.add_edge(
    "memory",
    "destination"
)

graph_builder.add_edge(
    "destination",
    "activity"
)

graph_builder.add_edge(
    "activity",
    "restaurant"
)

graph_builder.add_edge(
    "restaurant",
    "destination_display"
)

graph_builder.add_edge(
    "destination_display",
    "flight"
)

graph_builder.add_edge(
    "flight",
    "flight_advisor"
)

graph_builder.add_edge(
    "flight_advisor",
    "flight_selection"
)

graph_builder.add_edge(
    "flight_selection",
     "hotel"
)

graph_builder.add_edge(
    "hotel",
    "hotel_advisor"
)

graph_builder.add_edge(
    "hotel_advisor",
    "hotel_selection"
)

graph_builder.add_edge(
    "hotel_selection",
    "multi_destination_hotel"
)

graph_builder.add_edge(
    "multi_destination_hotel",
    "transport_suggestion"
)

graph_builder.add_edge(
    "transport_suggestion",
    "budget"
)

graph_builder.add_edge(
    "budget",
    "budget_advisor"
)

graph_builder.add_conditional_edges(
    "budget_advisor",
    budget_status_router,
    {
        "itinerary": "itinerary",
        "budget_decision": "budget_decision"
    }
)

graph_builder.add_edge(
    "budget_decision",
    "budget_update"
)

graph_builder.add_edge(
    "budget_update",
    "budget"
)

graph_builder.add_edge(
    "itinerary",
    "itinerary_formatter"
)

graph_builder.add_edge(
    "itinerary_formatter",
    END
)

travel_graph = graph_builder.compile(checkpointer = memory)

