import time
import logging
import random

def retry_with_backoff(func, retries=5, base_delay=2):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            logging.warning(f"Attempt {attempt+1} failed: {e}. Retrying in {delay:.2f}s")
            time.sleep(delay)
    raise Exception(f"Function failed after {retries} retries")
