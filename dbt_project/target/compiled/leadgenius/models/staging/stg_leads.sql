with source as (
    select * from raw_leads
)

select
    id as lead_id,
    email,
    name as lead_name,
    source,
    company_name,
    domain,
    employee_count,
    industry,
    job_title,
    estimated_revenue,
    uses_salesforce,
    is_b2b_from_llm,
    has_been_routed,
    created_at,
    updated_at
from source