# Known Limitations

**Snapshot date:** 2026-03-23

- Mock mode exists to make the demo reproducible without paid API keys.
- Live enrichment behavior depends on third-party credentials and API availability.
- Generated dbt artifacts should be produced by CI/local runs instead of committed to source control.
- CRM and Slack activation paths should be tested against each target workspace before production use.
- The Evidence dashboard is a reporting layer for the demo, not the system of record.

