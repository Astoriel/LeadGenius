---
title: LeadGenius RevOps Dashboard
---

Welcome to the **LeadGenius** Revenue Operations command center. 
This dashboard visualizes the throughput and effectiveness of our automated scoring and enrichment engine.

```sql leads
select * from leadgenius.mart_scored_leads
```

## 1. Lead Pipeline Funnel
How many leads are Hot, Warm, or Cold?

```sql funnel
select 
  lead_tier,
  count(*) as volume
from ${leads}
group by 1
order by 
  case when lead_tier = 'Hot' then 1 
       when lead_tier = 'Warm' then 2 
       else 3 end
```

<BarChart 
  data={funnel} 
  x="lead_tier" 
  y="volume"
  title="Lead Tier Distribution"
  fillColor="#4ade80"
/>

---

## 2. Lead Score Distribution
Histogram of the calculated lead scores across the entire database.

```sql score_hist
select 
  cast(lead_score / 10 as int) * 10 as score_bucket,
  count(*) as volume
from ${leads}
group by 1
order by 1
```

<BarChart 
  data={score_hist} 
  x="score_bucket" 
  y="volume" 
  title="Lead Score Histogram (Buckets of 10)"
/>

---

## 3. Enrichment Fill Rate (Waterfall Efficacy)
What percentage of ingested leads successfully retrieved Firmographic data?

```sql fill_rate
select
  count(case when industry is not null then 1 end) * 100.0 / nullif(count(*), 0) as industry_fill_rate,
  count(case when is_b2b then 1 end) * 100.0 / nullif(count(*), 0) as b2b_fill_rate
from ${leads}
```

<Value 
  data={fill_rate} 
  column="industry_fill_rate" 
  title="Industry Identification Rate" 
  fmt="0.0'x%'"
/>

<Value 
  data={fill_rate} 
  column="b2b_fill_rate" 
  title="B2B Identification Rate" 
  fmt="0.0'%'"
/>

---

## 4. Latest Hot Leads (SQLs)
Ready for Sales.

```sql hot_leads
select lead_name, company_name, job_title, email, lead_score
from ${leads}
where lead_tier = 'Hot'
order by lead_score desc
limit 10
```

<DataTable data={hot_leads} />
