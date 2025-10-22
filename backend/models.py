from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float
from sqlalchemy.sql import func
from .database import Base

class Lead(Base):
    __tablename__ = "raw_leads"

    id = Column(Integer, primary_key=True, index=True)
    
    # Ingestion Data
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    source = Column(String, nullable=True)
    
    # Enrichment Data (JSON could be used, but flat columns are easier for dbt initially)
    company_name = Column(String, nullable=True)
    domain = Column(String, nullable=True)
    employee_count = Column(Integer, nullable=True)
    industry = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    estimated_revenue = Column(Float, nullable=True)
    uses_salesforce = Column(Boolean, default=False)
    is_b2b_from_llm = Column(Boolean, nullable=True)
    
    # Status
    score = Column(Integer, nullable=True)
    has_been_routed = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
