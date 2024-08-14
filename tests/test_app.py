import pytest

from src.app import create_app


@pytest.fixture
def client():
    return create_app().test_client()


def test_health_is_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_version_reports_build_info(client, monkeypatch):
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.setenv("GIT_SHA", "abc1234")
    body = client.get("/version").get_json()
    assert body["environment"] == "staging"
    assert body["commit"] == "abc1234"


def test_index_shows_configured_message(client, monkeypatch):
    monkeypatch.setenv("APP_MESSAGE", "Deployed by git")
    response = client.get("/")
    assert response.status_code == 200
    assert b"Deployed by git" in response.data
