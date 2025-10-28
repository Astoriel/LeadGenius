from typing import Dict, Any, List
from .base import BaseProvider
from .standard import ApolloProvider, HunterProvider
from .scraper import LLMScraperProvider
from .techstack import TechStackProvider

class EnrichmentManager:
    """
    Manages the 'Waterfall' logic of Enrichment.
    """
    def __init__(self):
        # Order matters! Standard APIs are fast but specific, LLM is slow but catches edge cases.
        self.providers: List[BaseProvider] = [
            ApolloProvider(),
            HunterProvider(),
            LLMScraperProvider(),
            TechStackProvider()
        ]

    def enrich_lead(self, email: str) -> Dict[str, Any]:
        """
        Executes the waterfall, yielding a merged dictionary of enriched data.
        """
        domain = email.split('@')[-1] if '@' in email else None
        if not domain or domain in ["gmail.com", "yahoo.com", "hotmail.com"]:
            print(f"[EnrichManager] Cannot enrich free email domain for {email}.")
            return {}

        merged_data: Dict[str, Any] = {}
        
        for provider in self.providers:
            try:
                result = provider.enrich(email, domain)
                if result:
                    print(f"[{provider.name}] Returning Data: {result}")
                    # Update merged_data with new fields, without overwriting existing ones unless empty
                    for key, value in result.items():
                        if value is not None and value != "":
                            # Use dict.setdefault to keep the first non-null value (from higher priority provider)
                            if key not in merged_data:
                                merged_data[key] = value
            except Exception as e:
                print(f"[EnrichManager] Provider {provider.name} failed: {e}")
                # Waterfall continues despite one failure
                continue
                
        return merged_data
