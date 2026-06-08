from app.safety.maturity import check_maturity_gate


def test_internal_access_allowed_when_public_disabled(monkeypatch):
    monkeypatch.setenv("MICROGPT_PROJECT_MATURITY", "internal")
    monkeypatch.setenv("MICROGPT_ALLOW_PUBLIC_ACCESS", "false")
    decision = check_maturity_gate()
    assert decision.allowed is True
    assert decision.status == "internal"


def test_public_access_allowed_when_enabled(monkeypatch):
    monkeypatch.setenv("MICROGPT_PROJECT_MATURITY", "public")
    monkeypatch.setenv("MICROGPT_ALLOW_PUBLIC_ACCESS", "true")
    decision = check_maturity_gate()
    assert decision.allowed is True
    assert decision.status == "public"


def test_public_access_blocked_when_not_enabled(monkeypatch):
    monkeypatch.setenv("MICROGPT_PROJECT_MATURITY", "public")
    monkeypatch.setenv("MICROGPT_ALLOW_PUBLIC_ACCESS", "false")
    decision = check_maturity_gate()
    assert decision.allowed is False
