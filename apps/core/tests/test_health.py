import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_health_endpoint_is_public(client):
    response = client.get(reverse("health"))

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "carpet-commerce-backend",
    }
    assert response["X-Request-ID"]


@pytest.mark.django_db
def test_health_preserves_request_id(client):
    response = client.get(reverse("health"), HTTP_X_REQUEST_ID="trace-123")

    assert response.status_code == 200
    assert response["X-Request-ID"] == "trace-123"


@pytest.mark.django_db
def test_readiness_checks_database_and_cache(client):
    response = client.get(reverse("readiness"))

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "checks": {
            "database": True,
            "cache": True,
        },
    }
