from app.state.travel_state import (
    TravelState
)

from app.state.budget_advisor_schema import (
    BudgetRecommendation
)

from app.services.gemini_service import (
    llm
)


def budget_advisor_agent(
    state: TravelState
):

    structured_llm = (
        llm.with_structured_output(
            BudgetRecommendation
        )
    )

    response = structured_llm.invoke(
        f"""
You are an expert travel budget advisor.

Traveler Budget:
{state.get("budget")}

Budget Analysis:
{state.get("budget_summary")}

Available Savings Suggestions:
{state.get("budget_suggestions")}

TASK:

If the trip is within budget:

- congratulate the traveler
- explain why the trip fits comfortably within budget

If the trip is over budget:

- choose the BEST budget adjustment
- recommend only ONE option
- explain why it is the best tradeoff

Prioritize:

1. preserving traveler experience
2. minimizing budget overrun
3. maintaining value for money

Return structured output.
"""
    )

    state[
        "budget_recommendation"
    ] = response.model_dump()

    return state