import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
import os
import json
import openai
from .base import BaseProvider

class LLMScraperProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "LLM_Web_Scraper"

    def enrich(self, email: str, domain: str) -> Dict[str, Any]:
        """
        Scrapes the domain homepage and uses an LLM to classify the firm.
        """
        llm_api_key = os.getenv("LLM_API_KEY")
        if not llm_api_key or llm_api_key.startswith("sk-..."):
            print(f"[{self.name}] Skipping real LLM call (missing or default API key).")
            # MOCK IMPLEMENTATION FOR PORTFOLIO
            if domain == "dbtlabs.com":
                return {"company_name": "dbt Labs", "industry": "Data Infrastructure", "is_b2b_from_llm": True}
            elif domain == "nike.com":
                return {"company_name": "Nike", "industry": "Retail / Apparel", "is_b2b_from_llm": False}
            return {}

        print(f"[{self.name}] Attempting to scrape and analyze: https://{domain}")
        
        try:
            response = requests.get(f"https://{domain}", timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.content, "html.parser")
            body_text = soup.get_text(separator=' ', strip=True)[:3000] # Grab first 3k chars
        except Exception as e:
            print(f"[{self.name}] Scrape failed for {domain}: {e}")
            return {}

        try:
            client = openai.OpenAI(
                api_key=llm_api_key,
                base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
            )
            
            prompt = f"""
Analyze the following website text from {domain}. 
Return a strict JSON object with these exact keys:
- "company_name" (string or null)
- "industry" (string or null)
- "is_b2b_from_llm" (boolean, true if they sell to other businesses, false if consumers)

Website Text:
{body_text}
"""
            model = os.getenv("LLM_MODEL", "gpt-4o-mini")
            
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a data enrichment assistant. Return ONLY valid JSON, no markdown blocks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )
            
            result_str = completion.choices[0].message.content.strip()
            # Clean up potential markdown formatting
            if result_str.startswith("```json"):
                result_str = result_str[7:-3]
            elif result_str.startswith("```"):
                result_str = result_str[3:-3]
                
            data = json.loads(result_str)
            print(f"[{self.name}] Successfully analyzed {domain} with LLM: {data}")
            return data
            
        except Exception as e:
            print(f"[{self.name}] LLM analysis failed: {e}")
            return {}
