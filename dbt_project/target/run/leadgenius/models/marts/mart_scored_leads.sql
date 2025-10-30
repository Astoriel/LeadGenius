
  
    

  create  table "leadgenius"."public"."mart_scored_leads__dbt_tmp"
  
  
    as
  
  (
    with  __dbt__cte__int_lead_scoring as (
-- This file is an initial hardcoded version. In Phase 5, we will dynamically template this using rules.yml
with staged_leads as (
    select * from "leadgenius"."public"."stg_leads"
),

scoring as (
    select
        *,
        -- Base score
        0 
        -- Rule 1: Sales or Exec gets +20
        + case 
            when lower(job_title) like '%ceo%' or lower(job_title) like '%vp%' then 30
            when lower(job_title) like '%director%' then 20
            else 0 
          end
        -- Rule 2: Company Size
        + case
            when employee_count > 1000 then 40
            when employee_count > 100 then 20
            else 0
          end
        -- Rule 3: Tech Stack (Enterprise Tool Usage)
        + case
            when uses_salesforce = true then 50
            else 0
          end
        -- Rule 4: LLM B2B Check
        + case
            when is_b2b_from_llm = true then 20
            when is_b2b_from_llm = false then -50
            else 0
          end
        as calculated_score
    from staged_leads
)

select * from scoring
), scored_leads as (
    select * from __dbt__cte__int_lead_scoring
)

select
    lead_id,
    email,
    lead_name,
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
  );
  