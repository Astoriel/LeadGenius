from typing import Dict, Any
from .base import BaseProvider

class TechStackProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "TechStack_API"

    def enrich(self, email: str, domain: str) -> Dict[str, Any]:
        """
        Simulates calling an API like BuiltWith / Wappalyzer to view the company's tech stack.
        """
        print(f"[{self.name}] Analyzing tech stack for {domain}")
        
        # MOCK IMPLEMENTATION
        # Look for heavy enterprise tools (Marketo, Salesforce) to imply budget.
        
        if domain == "tesla.com" or domain == "microsoft.com":
            return {
                "uses_salesforce": True
            }
        elif domain == "notion.so":
            return {
                "uses_salesforce": False, # Startups might use HubSpot or similar initially
                # could add "uses_hubspot": True if we tracked it in the DB
            }
            
        return {}
