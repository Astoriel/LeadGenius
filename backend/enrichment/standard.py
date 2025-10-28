from typing import Dict, Any
import os
from .base import BaseProvider

class ApolloProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "Apollo"

    def enrich(self, email: str, domain: str) -> Dict[str, Any]:
        # In a real environment, you'd use os.getenv("APOLLO_API_KEY") and the requests library.
        api_key = os.getenv("APOLLO_API_KEY")
        
        # MOCK IMPLEMENTATION FOR DEMO/PORTFOLIO
        # This guarantees the project works perfectly even without an active subscription
        print(f"[{self.name}] Attempting to enrich {email} / {domain}")
        
        if domain == "tesla.com":
            return {
                "company_name": "Tesla Motors",
                "employee_count": 120000,
                "industry": "Automotive",
                "job_title": "CEO" if "elon" in email.lower() else "Engineer",
                "estimated_revenue": 80000000000.0
            }
        elif domain == "microsoft.com":
            return {
                "company_name": "Microsoft",
                "employee_count": 220000,
                "industry": "Software",
                "job_title": "Executive",
                "estimated_revenue": 200000000000.0
            }
        
        # Simulate an API failure or lack of data
        return {}

class HunterProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "Hunter.io"

    def enrich(self, email: str, domain: str) -> Dict[str, Any]:
        # Fallback Mock logic
        print(f"[{self.name}] Attempting to enrich {email} / {domain}")
        
        if domain == "stripe.com":
            return {
                "company_name": "Stripe",
                "employee_count": 7000,
                "industry": "Financial Services",
                "estimated_revenue": 14000000000.0
            }
            
        return {}
