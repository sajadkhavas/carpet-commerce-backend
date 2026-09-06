from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class HealthView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @never_cache
    def get(self, request):
        return JsonResponse(
            {
                "status": "ok",
                "service": "carpet-commerce-backend",
            }
        )


class ReadinessView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @never_cache
    def get(self, request):
        checks = {
            "database": self._database_ready(),
            "cache": self._cache_ready(),
        }
        ready = all(checks.values())
        return JsonResponse(
            {
                "status": "ready" if ready else "not_ready",
                "checks": checks,
            },
            status=200 if ready else 503,
        )

    @staticmethod
    def _database_ready() -> bool:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        except Exception:
            return False
        return True

    @staticmethod
    def _cache_ready() -> bool:
        key = "system:readiness"
        try:
            cache.set(key, "ok", timeout=5)
            value = cache.get(key)
            cache.delete(key)
        except Exception:
            return False
        return value == "ok"
