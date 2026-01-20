<h1 align="center">
  <br>
  🚀 LeadGenius
  <br>
</h1>

<h4 align="center">The Open-Source, Self-Hosted B2B Lead Scoring & Routing Engine</h4>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.104-009688.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/dbt-PostgreSQL-FF694B.svg" alt="dbt">
  <img src="https://img.shields.io/badge/Evidence.dev-BI-brightgreen.svg" alt="Evidence">
  <img src="https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF.svg" alt="GitHub Actions">
</p>

<p align="center">
  <a href="#the-problem-why-leadgenius">The Problem</a> •
  <a href="#how-it-works-architecture">Architecture</a> •
  <a href="#live-dashboard--mock-mode">Live Dashboard & Mock Mode</a> •
  <a href="#crm-integrations">CRM Integrations</a> •
  <a href="#quick-start">Quick Start</a>
</p>

---

## 📈 View Live RevOps Dashboard

The analytics artifacts are automatically built via CI/CD and hosted on GitHub Pages:
👉 **[Live Evidence BI Dashboard](https://astoriel.github.io/LeadGenius/)** 👈

## The Problem: Why LeadGenius?

If you run a B2B SaaS, your landing pages get hit with hundreds of sign-ups a day. A few are enterprise whales, but the majority are students, personal emails, or B2C noise.

Enterprise Revenue Operations (RevOps) teams buy tools like **Clearbit Reveal**, **MadKudu**, or **ZoomInfo** to enrich these emails, score them, and route the good ones to Sales. 

**The catch?** These tools cost upwards of **$20,000/year** and often operate as complete "black boxes" (nobody knows exactly *why* a lead got 90 points).

**LeadGenius** offers a transparent, $0/month open-source alternative.

---

## How it Works: Architecture

LeadGenius solves B2B data routing across 4 modular layers: Ingestion, Waterfall Enrichment, Rules-as-Code Scoring, and Reverse ETL.

```mermaid
graph TD
    %% Ingestion %%
    subgraph Layer 1: Ingestion
    A[Frontend/Zapier] -->|POST JSON Payload| B(FastAPI Webhook)
    B -->|Save Raw Lead| C[(PostgreSQL)]
    end

    %% Enrichment %%
    subgraph Layer 2: Waterfall Enrichment
    B -.->|Background Task| D{Enrichment Manager}
    D -->|1. Try Fast APIs| E[Apollo / Hunter]
    E -.->|If No Data| F[LLM Scraper Fallback]
    F -->|Analyze Homepage B2B/B2C| G[OpenAI/Anthropic]
    G -.->|Fallback| H[TechStack / SEO Metrics]
    D -->|Update Appended Data| C
    end

    %% Scoring %%
    subgraph Layer 3: dbt Scoring
    I[rules.yml Configuration] -->|Parsed by Python| J(dbt: int_lead_scoring.sql)
    C --> K{dbt run}
    J --> K
    K -->|Create View| L[(mart_scored_leads)]
    end

    %% Activation %%
    subgraph Layer 4: Activation
    M((APScheduler 60s)) --> N[Activation Manager]
    N -->|Query Top Tiers| L
    N -->|Route 1| O[Slack Webhook ALERT]
    N -->|Route 2| P[HubSpot CRM PATCH]
    end

    %% Observability %%
    subgraph Layer 5: Observability
    L -->|Automated CSV Export| Q[Evidence BI]
    Q -->|GitHub Actions| R[Live Dashboards]
    end

    %% Styling %%
    classDef primary fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef secondary fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef db fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    class A,B,D,K,N,I primary;
    class E,F,G,H,O,P secondary;
    class C,L,Q db;
```

## Live Dashboard & Mock Mode

To make it easy to evaluate and test this project without needing active API keys for Apollo/Hunter/LLMs, this repository includes a robust **Mock Mode Generator**.

1. Start the cluster with `TEST_MODE="true"` in your `.env` file.
2. The FastAPI Server will automatically spin up a background data seeder.
3. It will push 20 highly-realistic mock leads (e.g., Stripe, Vercel, Anthropic) into the webhook.
4. The `EnrichmentManager` intercepts these domains and injects rich deterministic mock firmographics (Employee counts, Job Titles, Industry).
5. The downstream dbt pipeline parses your `rules.yml` file, generates the SQL models, and assigns beautiful `Hot`/`Warm`/`Cold` tiers to your mock leads, producing a portfolio-ready dataset.

All of this happens invisibly during GitHub Actions CI/CD to power the public-facing [Evidence RevOps Dashboard](https://astoriel.github.io/LeadGenius/).

## CRM Integrations

LeadGenius doesn't just alert you; it actively patches your existing workspace:

*   **HubSpot**: Includes a native `HubSpotDestination` module. It searches the HubSpot Contacts API by email and performs a `PATCH` request to update custom properties (`leadgenius_score`, `leadgenius_tier`).
*   **Slack**: Real-time "Hot Lead" alerts in a dedicated channel.
*   **[Extendable]**: The modular `ActivationManager` makes writing a new Salesforce or Pipedrive integration a 10-line python class.

## Transparent YAML Scoring

Define what matters to you in plain English (`rules.yml`). LeadGenius dynamically generates the SQL.

```yaml
scoring_rules:
  - description: "Sales or Exec gets +30"
    sql_condition: "lower(job_title) like '%ceo%' or lower(job_title) like '%vp%'"
    points: 30
  - description: "Confirmed B2B"
    sql_condition: "is_b2b_from_llm = true"
    points: 20
```

## Quick Start

### Prerequisites
*   Docker & Docker Compose
*   Python 3.11+

### Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/Astoriel/LeadGenius.git
cd LeadGenius

# 2. Configure environment (Mock data is enabled by default in the example!)
cp .env.example .env

# 3. Spin up the cluster (Postgres + FastAPI + CRON Scheduler + Mock Seeder)
docker-compose up -d --build
```

Watch the terminal (`docker-compose logs -f api`) to see the engine execute the Waterfall, trigger `dbt run`, and route the lead!
