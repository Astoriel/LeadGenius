# Project Status

**Status:** Portfolio reference implementation  
**Snapshot date:** 2026-03-23  
**Primary audience:** RevOps/data engineers evaluating a transparent lead scoring pipeline pattern.

`LeadGenius` demonstrates a B2B lead scoring and routing system built around FastAPI ingestion, enrichment, rules-as-code scoring, dbt transformations, and an Evidence dashboard. Mock mode is a deliberate evaluation path, not a claim that every third-party enrichment connector works out of the box.

## Current Confidence

- Working: webhook ingestion, enrichment manager, rule-driven scoring flow, dbt models, activation tests, demo dashboard pipeline.
- Planned: deeper CRM connector hardening, stricter secrets handling, fuller dbt docs/tests, more integration tests around live APIs.
- Not claimed: production Clearbit/MadKudu replacement, hosted RevOps SaaS, guaranteed live third-party enrichment coverage.

