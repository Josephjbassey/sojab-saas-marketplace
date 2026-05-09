import time
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.conf import settings

# Simple uptime tracking
START_TIME = time.time()

def health_live(request):
    """Liveness probe - checks if the application process is up."""
    return JsonResponse({
        "status": "ok",
        "app": "running",
        "timestamp": time.time()
    })

def health_ready(request):
    """Readiness probe - checks if the application can serve traffic (DB/Redis)."""
    db_ok = True
    try:
        connections['default'].cursor()
    except OperationalError:
        db_ok = False

    redis_ok = "not_configured"
    if hasattr(settings, 'CACHES') and 'default' in settings.CACHES:
        try:
            # Safely try to import django_redis, if not available use raw redis if needed
            from django_redis import get_redis_connection
            conn = get_redis_connection("default")
            conn.ping()
            redis_ok = "ok"
        except ImportError:
            # Fallback for when django-redis is not installed
            redis_ok = "library_missing"
        except Exception:
            redis_ok = "error"

    status = "ok" if db_ok and redis_ok in ["ok", "not_configured", "library_missing"] else "error"

    return JsonResponse({
        "status": status,
        "database": "ok" if db_ok else "error",
        "redis": redis_ok,
        "timestamp": time.time()
    }, status=200 if status == "ok" else 503)

def health_status(request):
    """Combined health status with more metadata."""
    db_ok = True
    try:
        connections['default'].cursor()
    except OperationalError:
        db_ok = False

    redis_ok = "not_configured"
    if hasattr(settings, 'CACHES') and 'default' in settings.CACHES:
        try:
            from django_redis import get_redis_connection
            conn = get_redis_connection("default")
            conn.ping()
            redis_ok = "ok"
        except ImportError:
            redis_ok = "library_missing"
        except Exception:
            redis_ok = "error"

    status = "ok" if db_ok and redis_ok in ["ok", "not_configured", "library_missing"] else "error"
    uptime = time.time() - START_TIME

    return JsonResponse({
        "status": status,
        "app": "running",
        "database": "ok" if db_ok else "error",
        "redis": redis_ok,
        "uptime": f"{uptime:.2f}s",
        "timestamp": time.time(),
        "version": getattr(settings, 'APP_VERSION', '1.0.0')
    }, status=200 if status == "ok" else 503)
