from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse


def live(request):  # type: ignore[no-untyped-def]
    return JsonResponse({"status": "ok"})


def ready(request):  # type: ignore[no-untyped-def]
    checks: dict[str, str] = {}
    status = 200
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "unavailable"
        status = 503

    try:
        cache.set("healthcheck", "ok", timeout=5)
        checks["redis"] = "ok" if cache.get("healthcheck") == "ok" else "unavailable"
        if checks["redis"] == "unavailable":
            status = 503
    except Exception:
        checks["redis"] = "unavailable"
        status = 503

    payload = {"status": "ok" if status == 200 else "unavailable", "checks": checks}
    return JsonResponse(payload, status=status)
