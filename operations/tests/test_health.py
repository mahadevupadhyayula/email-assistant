from unittest.mock import patch

import pytest
from django.urls import reverse


def test_live_health_does_not_depend_on_services(client) -> None:  # type: ignore[no-untyped-def]
    response = client.get(reverse("health-live"))
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
def test_ready_health_reports_dependencies(client, settings) -> None:  # type: ignore[no-untyped-def]
    settings.CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
    response = client.get(reverse("health-ready"))
    assert response.status_code == 200
    assert response.json()["checks"] == {"database": "ok", "redis": "ok"}


@pytest.mark.django_db
def test_ready_health_exposes_redis_failure(client) -> None:  # type: ignore[no-untyped-def]
    with patch("operations.views.cache.set", side_effect=ConnectionError):
        response = client.get(reverse("health-ready"))
    assert response.status_code == 503
    assert response.json()["checks"]["redis"] == "unavailable"


@pytest.mark.django_db
def test_ready_health_reports_redis_read_failure(client) -> None:  # type: ignore[no-untyped-def]
    with (
        patch("operations.views.cache.set"),
        patch("operations.views.cache.get", return_value=None),
    ):
        response = client.get(reverse("health-ready"))

    assert response.status_code == 503
    assert response.json() == {
        "status": "unavailable",
        "checks": {"database": "ok", "redis": "unavailable"},
    }
