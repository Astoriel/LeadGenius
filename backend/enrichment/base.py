from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseProvider(ABC):
    """
    Abstract Base Class for all Enrichment Providers.
    Defines the standard interface for fetching firmographic/technographic data.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the provider (e.g., 'Apollo', 'LLM_Scraper')"""
        pass

    @abstractmethod
    def enrich(self, email: str, domain: str) -> Dict[str, Any]:
        """
        Enrich a lead given their email and/or domain.
        Returns a dictionary with the extracted fields.
        Standard keys expected:
        - company_name: str
        - employee_count: int
        - industry: str
        - job_title: str
        - estimated_revenue: float
        - uses_salesforce: bool
        - is_b2b_from_llm: bool
        """
        pass
