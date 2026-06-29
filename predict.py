import sys
import logging
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv    

# Load env variables (including Groq API key)
load_dotenv()

# pyrefly: ignore [missing-import]
from src.models.schemas import UserPreferences   
# pyrefly: ignore [missing-import]
from src.models.enums import BudgetLevel
# pyrefly: ignore [missing-import]
from src.engine.orchestrator import RecommendationEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("Initializing Recommendation Engine...")
    engine = RecommendationEngine()
    
    prefs = UserPreferences(
        location="Bellandur",
        min_rating=4.2,
        budget=BudgetLevel.MEDIUM,
    )
    
    print("\nFetching recommendations from Groq LLM...")
    response = engine.get_recommendations(prefs)
    
    print("\n" + "="*60)
    print("TOP 5 RESTAURANT RECOMMENDATIONS")
    print("="*60)
    
    if not response.recommendations:
        print("\nNo recommendations found.")
        print(f"Summary: {response.summary}")
        return

    for rec in response.recommendations:
        print(f"#{rec.rank} - {rec.restaurant_name} (Match Score: {rec.match_score}/10)")
        print(f"  Cuisine: {rec.cuisine}")
        print(f"  Rating: {rec.rating}")
        print(f"  Cost for Two: Rs. {rec.cost_for_two}")
        print(f"  Why: {rec.explanation}\n")
        
    print("-" * 60)
    print(f"Summary: {response.summary}")
    print("="*60)

if __name__ == "__main__":
    main()
