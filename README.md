<h1 align="center">
  <br>
  🚀 LeadGenius
  <br>
</h1>

<h4 align="center">The Open-Source, Self-Hosted B2B Lead Scoring & Routing Engine</h4>

<p align="center">
  <a href="#the-problem-why-leadgenius">The Problem</a> •
  <a href="#the-solution-how-it-works">How It Works</a> •
  <a href="#key-features">Features</a> •
  <a href="#crm-integrations">CRM Integrations</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#built-with">Built With</a>
</p>

---

## The Problem: Why LeadGenius?

If you run a B2B SaaS, your Typeform, Webflow, or custom landing pages get hit with hundreds of sign-ups a day. A few are enterprise whales, but the majority are students, personal emails, or B2C noise.

Enterprise Revenue Operations (RevOps) teams buy tools like **Clearbit Reveal**, **MadKudu**, or **ZoomInfo** to enrich these emails, score them, and route the good ones to Sales. 

**The catch?** These tools cost upwards of **$20,000/year** and often operate as complete "black boxes" (nobody knows exactly *why* a lead got 90 points).

## The Solution: How It Works

**LeadGenius** offers a transparent, $0/month open-source alternative:

1. **Ingest (FastAPI)**: A lightweight webhook endpoint catches incoming leads from your frontend or Zapier.
2. **Enrich (The Waterfall)**: Combines standard firmographic APIs (Apollo.io/Hunter.io) with a fallback **LLM Web Scraper**. If standard APIs fail, LeadGenius visits the lead's website and uses AI (OpenAI/Anthropic via OpenRouter) to read the homepage and extract precise B2B intent.
3. **Score (dbt + Postgres)**: Uses **Configuration-as-Code** (a simple `rules.yml` file) to calculate Lead Scores via dbt SQL. 100% transparent. 100% customized to your ICP.
4. **Activate & Route (Reverse ETL)**: An internal orchestrator queries the database for "Hot" leads, alerts your team on Slack, and syncs the exact score back into your CRM.

## Key Features

*   🌊 **Waterfall Enrichment**: Never pay for empty API pings. Tries cheap APIs first, falls back to intelligent LLM Scraping.
*   🧠 **LLM Web Scraper Module**: Built-in BeautifulSoup + OpenAI integration. Analyzes a company's homepage to extract hidden data (Industry, B2B/B2C, Audience).
*   ⚙️ **Transparent YAML Scoring**: Define what matters to you (e.g., `role: CEO -> +50 points`) in plain English. LeadGenius dynamically generates the SQL.
*   📊 **Evidence BI Dashboard Ready**: Includes an automated GitHub Actions pipeline that generates a beautiful RevOps dashboard (Funnel, Missing Data Fill Rates, Score Histograms) every night.

## CRM Integrations

LeadGenius doesn't just alert you; it actively patches your existing workspace:

*   **HubSpot**: Includes a native `HubSpotDestination` module. It uses the `HUBSPOT_API_KEY` to search the HubSpot Contacts API by email and perform a `PATCH` request to update custom properties (`leadgenius_score`, `leadgenius_tier`).
*   **Slack**: Real-time "Hot Lead" alerts in a dedicated channel.
*   [Extendable] Modular `ActivationManager` makes writing a new Salesforce or Pipedrive integration a 10-line python class.

## Quick Start

### Prerequisites
*   Docker & Docker Compose
*   Python 3.11+

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/Astoriel/Job-Bodyguard-1.git leadgenius
cd leadgenius

# 2. Configure environment
cp .env.example .env
# Fill in your OpenRouter / Apollo / HubSpot / Slack keys

# 3. Define your rules
nano rules.yml

# 4. Spin up the cluster (Postgres + FastAPI + Scheduler)
docker-compose up -d --build
```

### Ingesting a Lead

Send a POST request to your new engine:
```bash
curl -X POST http://localhost:8000/webhook/leads \
  -H "Content-Type: application/json" \
  -d '{"email":"sam@openai.com", "name":"Sam Altman", "source":"homepage"}'
```

Watch the terminal (`docker-compose logs -f api`) to see the engine execute the Waterfall, trigger `dbt run`, and route the lead!

## Built With

LeadGenius relies heavily on the modern data and backend stack:

*   **Python 3.11** & **FastAPI** - Core Server & Webhooks
*   **dbt (Data Build Tool)** - SQL-based Data Transformations & Scoring models
*   **PostgreSQL** - Central Data Warehouse
*   **Evidence BI** - RevOps Dashboard Visualization
*   **SQLAlchemy** & **Pydantic** - ORM and Type Validation
*   **APScheduler** - Background Task / CRON Management
*   **OpenRouter** / **OpenAI SDK** - LLM Fallback Web Scraping
*   **GitHub Actions** - CI/CD & Automated Mock Data Deployments
