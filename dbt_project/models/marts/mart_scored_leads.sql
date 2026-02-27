with scored_leads as (
    select * from {{ ref('int_lead_scoring') }}
)

select
    lead_id,
    email,
    lead_name,
    source,
    company_name,
    domain,
    job_title,
    industry,
    calculated_score as lead_score,
    case
        when calculated_score >= 80 then 'Hot'
        when calculated_score >= 30 then 'Warm'
        else 'Cold'
    end as lead_tier,
    created_at,
    has_been_routed
from
    scored_leads
