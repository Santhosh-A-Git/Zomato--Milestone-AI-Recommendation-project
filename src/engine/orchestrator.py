import logging
import pandas as pd
from src.config import settings
from src.data.ingestion import get_dataset
from src.models.schemas import UserPreferences, RecommendationResponse
from src.filters.restaurant_filter import filter_restaurants
from src.llm.groq_provider import GroqProvider
from src.llm.prompt_builder import get_system_prompt, build_user_prompt, parse_llm_response

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        """Initialize the recommendation engine with the LLM provider and dataset."""
        self.llm_provider = GroqProvider(
            api_key=settings.groq_api_key,
            model=settings.llm_model
        )
        
        try:
            logger.info("Initializing RecommendationEngine and loading dataset...")
            self.dataset = get_dataset()
        except Exception as e:
            logger.error(f"Failed to initialize dataset: {e}")
            self.dataset = pd.DataFrame()

    def get_recommendations(self, prefs: UserPreferences) -> RecommendationResponse:
        """
        Orchestrates the entire recommendation flow:
        1. Filters dataset based on preferences.
        2. Constructs system and user prompts.
        3. Calls Groq LLM.
        4. Parses and validates the JSON response.
        """
        if self.dataset.empty:
            return RecommendationResponse(
                recommendations=[],
                summary="The restaurant database is currently unavailable. Please try again later."
            )

        try:
            # Step 1: Filter dataset
            logger.info(f"Filtering dataset for location: {prefs.location}")
            filtered_df = filter_restaurants(self.dataset, prefs)
            
            # Fast return for empty states
            if filtered_df.empty:
                logger.info("Filtering yielded 0 results.")
                return RecommendationResponse(
                    recommendations=[],
                    summary=f"Unfortunately, we couldn't find any restaurants in '{prefs.location}' matching your criteria."
                )

            # Extract names for hallucination checking
            candidate_names = filtered_df['restaurant_name'].tolist()

            # Step 2: Build prompts
            system_prompt = get_system_prompt()
            user_prompt = build_user_prompt(prefs, filtered_df)

            # Step 3: Call LLM
            logger.info("Requesting recommendations from Groq LLM...")
            llm_response_text = self.llm_provider.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens
            )

            # Step 4: Parse response
            response_obj = parse_llm_response(llm_response_text, candidate_names)
            
            # Handle case where parser stripped everything out due to hallucinations
            if not response_obj.recommendations:
                return RecommendationResponse(
                    recommendations=[],
                    summary="We found some matches, but our AI couldn't confidently recommend them based on your strict preferences."
                )
                
            return response_obj

        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return RecommendationResponse(
                recommendations=[],
                summary="An unexpected error occurred while generating your recommendations. Please try again in a moment."
            )
