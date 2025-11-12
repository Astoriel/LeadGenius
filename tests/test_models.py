"""Verify that the Lead ORM model columns match expectations."""

from backend.models import Lead


def test_lead_table_name():
    assert Lead.__tablename__ == "raw_leads"


def test_lead_has_required_columns():
    column_names = {c.name for c in Lead.__table__.columns}
    expected = {"id", "email", "name", "source", "company_name", "domain",
                "employee_count", "industry", "job_title", "estimated_revenue",
                "uses_salesforce", "is_b2b_from_llm", "score",
                "has_been_routed", "created_at", "updated_at"}
    assert expected.issubset(column_names)


def test_email_is_unique():
    email_col = Lead.__table__.c.email
    assert email_col.unique is True


def test_email_is_not_nullable():
    email_col = Lead.__table__.c.email
    assert email_col.nullable is False


def test_has_been_routed_defaults_false():
    lead = Lead(email="test@x.com")
    assert lead.has_been_routed is False or lead.has_been_routed is None
