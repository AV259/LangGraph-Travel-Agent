from pydantic import BaseModel


class BudgetRecommendation(BaseModel):

    recommendation: str

    reason: str