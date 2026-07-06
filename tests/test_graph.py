from app.graph.travel_graph import travel_graph

state = {"budget_adjustment_attempted": False}

state = {
    "user_input":
    "Plan a 6 day trip to India from Frankfurt, from September 10 to September 16. my Budget is €4000. I love nature, food, culture and history. "
}

config = {
    "configurable": {
        "thread_id": "user_1"
    }
}

result = travel_graph.invoke(
    state,
    config=config
)

print(result)