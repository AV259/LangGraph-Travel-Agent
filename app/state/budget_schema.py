from pydantic import BaseModel
from typing import List, Dict


class BudgetSuggestion(BaseModel):

    type: str

    savings: float

    option: Dict


class BudgetSummary(BaseModel):

    total_cost: float

    remaining_budget: float

    budget_status: str

    suggestions: List[BudgetSuggestion]