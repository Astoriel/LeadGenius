import os
import csv
from sqlalchemy import create_engine, text

def export_dbt_marts_to_csv():
    # Target directory for Evidence BI data sources
    # Evidence expects data in the `dashboard/sources/` directory (or wherever configured)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dashboard_sources_dir = os.path.join(base_dir, "dashboard", "sources", "leadgenius")
    os.makedirs(dashboard_sources_dir, exist_ok=True)
    
    csv_path = os.path.join(dashboard_sources_dir, "mart_scored_leads.csv")
    
    db_url = os.getenv("DATABASE_URL", "postgresql://leaduser:leadpassword@localhost:5435/leadgenius")
    engine = create_engine(db_url)
    
    print(f"[Export] Connecting to DB to export mart_scored_leads...")
    try:
        with engine.connect() as conn:
            # We want all columns from the mart
            result = conn.execute(text("SELECT * FROM mart_scored_leads"))
            rows = result.fetchall()
            keys = result.keys()
            
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(keys)
                for row in rows:
                    writer.writerow(row)
                    
        print(f"[Export] Successfully exported {len(rows)} leads to {csv_path}")
    except Exception as e:
        print(f"[Export] Failed to export data: {e}")

if __name__ == "__main__":
    export_dbt_marts_to_csv()
