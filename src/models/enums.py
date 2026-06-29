from enum import Enum

class BudgetLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def max_cost(self) -> float:
        """Maximum cost for two people (INR) for this budget level."""
        if self == BudgetLevel.LOW:
            return 500.0
        elif self == BudgetLevel.MEDIUM:
            return 1500.0
        return float('inf')
        
    @property
    def min_cost(self) -> float:
        """Minimum cost for two people (INR) for this budget level."""
        if self == BudgetLevel.MEDIUM:
            return 501.0
        elif self == BudgetLevel.HIGH:
            return 1501.0
        return 0.0
