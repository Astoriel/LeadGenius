import os
from dotenv import load_dotenv

load_dotenv() # Load from .env

from backend.enrichment.scraper import LLMScraperProvider

print("Testing OpenRouter Scraping...")
provider = LLMScraperProvider()
result = provider.enrich("hello@anthropic.com", "anthropic.com")
print(f"Result: {result}")
