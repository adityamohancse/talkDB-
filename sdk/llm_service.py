# sdk/llm_service.py

import time
import logging
from sdk.providers import PROVIDERS
from config import DEFAULT_PROVIDER, DEFAULT_MODEL, MAX_RETRIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def llm_task(system_prompt, provider=DEFAULT_PROVIDER, model=DEFAULT_MODEL,
             max_retries=MAX_RETRIES, fallback_providers=None):
    """
    Central decorator. ALL LLM calls go through this.
    
    Handles:
    - Retries with exponential backoff
    - Provider fallback
    - Logging
    - Latency tracking
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Step 1: Get user input from the decorated function
            user_input = func(*args, **kwargs)

            # Step 2: Build list of providers to try
            providers_to_try = [provider]
            if fallback_providers:
                providers_to_try += fallback_providers

            # Step 3: Try each provider
            for current_provider in providers_to_try:
                llm_function = PROVIDERS[current_provider]

                # Step 4: Retry loop
                for attempt in range(max_retries):
                    logger.info(
                        f"[{func.__name__}] provider={current_provider} "
                        f"attempt={attempt + 1}/{max_retries}"
                    )

                    response = llm_function(system_prompt, user_input, model)

                    # Step 5: Success — return the text
                    if response.success:
                        logger.info(
                            f"[{func.__name__}] ✅ completed in {response.latency:.2f}s"
                        )
                        return response.text

                    # Step 6: Failed — retry with backoff
                    logger.warning(
                        f"[{func.__name__}] ❌ attempt {attempt + 1} failed: {response.error}"
                    )
                    if attempt < max_retries - 1:
                        wait = 2 ** attempt
                        logger.info(f"  Waiting {wait}s before retry...")
                        time.sleep(wait)

                # All retries failed for this provider
                logger.error(
                    f"[{func.__name__}] {current_provider} exhausted after {max_retries} attempts"
                )

            # Step 7: All providers failed
            raise Exception(
                f"[{func.__name__}] All providers failed: {providers_to_try}"
            )

        return wrapper
    return decorator