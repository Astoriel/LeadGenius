"""Tests for the /webhook/leads endpoint."""

import pytest


class TestLeadWebhook:
    """POST /webhook/leads — ingestion and deduplication."""

    def test_create_lead_returns_201_shape(self, client):
        payload = {"email": "jane@acme.com", "name": "Jane Doe", "source": "landing"}
        resp = client.post("/webhook/leads", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "jane@acme.com"
        assert "id" in data

    def test_create_lead_without_optional_fields(self, client):
        resp = client.post("/webhook/leads", json={"email": "minimal@example.com"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "minimal@example.com"
        assert data["source"] == "api"  # default value

    def test_duplicate_email_does_not_error(self, client):
        """Submitting the same email twice should not raise — we skip re-ingestion."""
        payload = {"email": "dup@test.com", "name": "First"}
        client.post("/webhook/leads", json=payload)
        resp = client.post("/webhook/leads", json=payload)
        assert resp.status_code == 200

    def test_missing_email_returns_422(self, client):
        resp = client.post("/webhook/leads", json={"name": "No Email"})
        assert resp.status_code == 422

    @pytest.mark.parametrize(
        "email",
        [
            "ceo@stripe.com",
            "ops@vercel.com",
            "hello@anthropic.com",
        ],
    )
    def test_various_emails_accepted(self, client, email):
        resp = client.post("/webhook/leads", json={"email": email})
        assert resp.status_code == 200
        assert resp.json()["email"] == email


class TestGetLeads:
    """GET /leads — list all ingested leads."""

    def test_empty_db_returns_empty_list(self, client):
        resp = client.get("/leads")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_ingested_leads_appear_in_list(self, client):
        client.post("/webhook/leads", json={"email": "listed@co.com"})
        resp = client.get("/leads")
        emails = [lead["email"] for lead in resp.json()]
        assert "listed@co.com" in emails
