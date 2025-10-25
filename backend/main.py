from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from . import models
from .database import get_db, engine, SessionLocal
from .enrichment.manager import EnrichmentManager

# create the tables (TODO: migrate to alembic later when we have time tbh)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LeadGenius", description="B2B Lead Scoring & Routing Engine")

# Initialize the modular Enrichment Manager
enrichment_mgr = EnrichmentManager()

# Pydantic Schemas
class LeadCreate(BaseModel):
    email: str
    name: Optional[str] = None
    source: Optional[str] = "api"

class LeadResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    source: Optional[str]
    
    class Config:
        from_attributes = True

def trigger_enrichment(lead_id: int):
    """
    Background Task executing the Waterfall enrichment flow.
    We create a new DB session since this runs independently of the request context.
    """
    db = SessionLocal()
    try:
        db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
        if not db_lead:
            return
            
        print(f"[Worker] Starting enrichment cascade for lead {lead_id} -> {db_lead.email}...")
        enriched_data = enrichment_mgr.enrich_lead(db_lead.email)
        
        if enriched_data:
            print(f"[Worker] Successful enrichment. Saving data to DB...")
            # Update columns if they exist in the DB schema
            for key, value in enriched_data.items():
                if hasattr(db_lead, key):
                    setattr(db_lead, key, value)
            
            db.commit()
            print("[Worker] Finished enrichment successfully.")
        else:
            print("[Worker] Waterfall enrichment yielded no usable data.")
            
    finally:
        db.close()

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .routing import check_and_route_leads
import subprocess
import os

@app.on_event("startup")
def start_scheduler():
    if os.getenv("TEST_MODE", "false").lower() == "true":
        print("[Startup] TEST_MODE is enabled. Spinning up background Mock Data Seeder...")
        base_dir = os.path.dirname(os.path.dirname(__file__))
        seed_script = os.path.join(base_dir, "scripts", "seed_demo_data.py")
        subprocess.Popen(["python", seed_script]) # Run in background without blocking

    scheduler = BackgroundScheduler()
    
    def job_run_dbt_and_route():
        print("[Scheduler] Starting periodic dbt run...")
        
        # 0. generate dbt model from rules.yml (hacky but it works for now)
        base_dir = os.path.dirname(os.path.dirname(__file__))
        script_path = os.path.join(base_dir, "scripts", "generate_scoring_model.py")
        try:
            subprocess.run(["python", script_path], capture_output=True, text=True)
            print("[Scheduler] Generated scoring model from rules.yml")
        except Exception as e:
            print(f"[Scheduler] Failed to generate scoring model: {e}")
            
        # 1. Run dbt (In production, use Airflow/Dagster, but for this self-contained demo we run via subprocess)
        dbt_dir = os.path.join(base_dir, "dbt_project")
        try:
            # We use dbt run in the background
            result = subprocess.run(["dbt", "run"], cwd=dbt_dir, capture_output=True, text=True)
            if result.returncode == 0:
                print("[Scheduler] dbt run successful.")
            else:
                print(f"[Scheduler] dbt run failed: {result.stdout}")
        except Exception as e:
            print(f"[Scheduler] Failed to execute dbt subprocess: {e}")
            
        # 2. Route the output
        db = SessionLocal()
        try:
            check_and_route_leads(db)
        finally:
            db.close()
            
    # Run every 60 seconds for demo purposes
    scheduler.add_job(
        job_run_dbt_and_route,
        trigger=IntervalTrigger(seconds=60),
        id='dbt_and_routing_job',
        name='Run dbt models and route leads',
        replace_existing=True
    )
    scheduler.start()
    print("[Scheduler] APScheduler started.")

@app.post("/webhook/leads", response_model=LeadResponse)
def ingest_lead(lead: LeadCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Check if lead exists to prevent duplicates
    db_lead = db.query(models.Lead).filter(models.Lead.email == lead.email).first()
    if db_lead:
        # we could update intsead, but for now just pass lol
        # raise HTTPException(status_code=400, detail="Lead already existssss")
        pass
    else:    
        # Create new lead
        db_lead = models.Lead(
            email=lead.email,
            name=lead.name,
            source=lead.source
        )
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
    
    # Enqueue Enrichment
    background_tasks.add_task(trigger_enrichment, db_lead.id)
    
    return db_lead

@app.get("/leads", response_model=list[LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    return db.query(models.Lead).all()
