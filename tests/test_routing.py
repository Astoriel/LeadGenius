"""Tests for the activation / routing layer."""

from unittest.mock import patch, MagicMock

from backend.activation import (
    ActivationManager,
    SlackDestination,
    HubSpotDestination,
)


class TestSlackDestination:
    def test_skips_when_no_webhook_url(self):
        dest = SlackDestination()
        with patch.dict("os.environ", {}, clear=True):
            result = dest.route(_sample_lead())
        assert result is False

    @patch("backend.activation.requests.post")
    def test_sends_alert_when_url_configured(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200)
        dest = SlackDestination()
        with patch.dict("os.environ", {"SLACK_WEBHOOK_URL": "https://hooks.slack.com/fake"}):
            result = dest.route(_sample_lead())
        assert result is True
        mock_post.assert_called_once()


class TestHubSpotDestination:
    def test_mock_mode_when_no_api_key(self):
        dest = HubSpotDestination()
        with patch.dict("os.environ", {}, clear=True):
            result = dest.route(_sample_lead())
        # Should succeed in mock mode
        assert result is True


class TestActivationManager:
    def test_routes_to_all_destinations(self):
        manager = ActivationManager()
        lead = _sample_lead()
        # Should not raise — destinations gracefully handle missing env vars
        manager.route_lead(lead)

    def test_has_slack_and_hubspot(self):
        manager = ActivationManager()
        names = [d.name for d in manager.destinations]
        assert "Slack" in names
        assert "HubSpot CRM" in names


# ── helpers ──────────────────────────────────────────

def _sample_lead():
    return {
        "lead_id": 1,
        "email": "ceo@bigcorp.com",
        "lead_name": "Alice",
        "company_name": "BigCorp",
        "job_title": "CEO",
        "lead_score": 95,
        "lead_tier": "Hot",
    }
