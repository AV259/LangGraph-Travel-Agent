from app.agents.trip_intake_agent import trip_intake_agent

state = {
    'user_input': "I want to go to Austria for 5 days in december from frankfurt. My budget is 2000 dollars and I am interested in skiing and museums."

}

result = trip_intake_agent(state)

print(result)
