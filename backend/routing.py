from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
from .activation import ActivationManager

def check_and_route_leads(db: Session):
    """
    queries the dbt mart table for hot leads that havent been routed yet
    triggers the ActivationManager, and updates the db status like a boss
    """
    print("[Routing] Checking for newly scored leads...")
    
    try:
        query = text('''
            SELECT lead_id, email, lead_name, company_name, job_title, 
                   lead_score, lead_tier
            FROM mart_scored_leads
            WHERE has_been_routed = False
        ''')
        
        results = db.execute(query).fetchall()
        
        if not results:
            return
            
        print(f"[Routing] Found {len(results)} un-routed leads.")
        
        activation_manager = ActivationManager()
        
        for row in results:
            lead_id = row[0]
            lead_data = {
                "lead_id": row[0],
                "email": row[1],
                "lead_name": row[2],
                "company_name": row[3],
                "job_title": row[4],
                "lead_score": row[5],
                "lead_tier": row[6]
            }
            
            if lead_data['lead_tier'] == 'Hot':
                activation_manager.route_lead(lead_data)
            else:
                # Cold / Warm leads might go to a mailing list (e.g., Mailchimp)
                print(f"[Routing] {lead_data['lead_tier']} Lead {lead_data['email']} queued for Nurturing Sequence.")
            
            # Mark as routed back in the raw_leads table so dbt updates mart_scored_leads on next run
            update_q = text("UPDATE raw_leads SET has_been_routed = True WHERE id = :id")
            db.execute(update_q, {"id": lead_id})
            
        db.commit()
            
    except Exception as e:
        print(f"[Routing] Error querying dbt mart: {e}")
        db.rollback()
