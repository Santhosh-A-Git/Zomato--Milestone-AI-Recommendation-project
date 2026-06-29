import time
import logging
from groq import Groq, APIConnectionError, RateLimitError, APITimeoutError

logger = logging.getLogger(__name__)

class GroqProvider:
    def __init__(self, api_key: str, model: str):
        if not api_key:
            raise ValueError("Groq API key is required")
        # Increase default timeout to handle potential API delays
        self.client = Groq(api_key=api_key, timeout=30.0)
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
        """
        Generate a response from Groq LLM with exponential backoff for rate limits.
        """
        max_retries = 3
        backoff_factor = 2
        delay = 1

        for attempt in range(max_retries):
            try:
                logger.info(f"Sending prompt to Groq model: {self.model} (Attempt {attempt + 1}/{max_retries})")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format={"type": "json_object"},
                )
                
                # Log token usage
                if hasattr(response, 'usage') and response.usage:
                    logger.info(
                        f"Token usage - Prompt: {response.usage.prompt_tokens}, "
                        f"Completion: {response.usage.completion_tokens}, "
                        f"Total: {response.usage.total_tokens}"
                    )
                
                return response.choices[0].message.content
                
            except (APIConnectionError, RateLimitError, APITimeoutError) as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed after {max_retries} attempts: {e}")
                    raise
                logger.warning(f"Groq API error ({type(e).__name__}): {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= backoff_factor
            except Exception as e:
                logger.error(f"Unexpected error calling Groq: {e}")
                raise
