from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text

from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.api import auth, generations, materials, search
from app.db.session import SessionLocal
from app.middleware.auth import AuthMiddleware
from app.services.cache import CacheService

# ── Structured logging ────────────────────────────────────────────────────────
setup_logging(debug=settings.DEBUG)
log = get_logger("app.main")

# ── Prometheus metrics ────────────────────────────────────────────────────────
try:
    from prometheus_client import (
        Counter,
        Histogram,
        generate_latest,
        CONTENT_TYPE_LATEST,
        REGISTRY,
    )

    REQUEST_COUNT = Counter(
        "http_requests_total",
        "Total HTTP requests",
        ["method", "endpoint", "status_code"],
    )
    REQUEST_LATENCY = Histogram(
        "http_request_duration_seconds",
        "HTTP request latency",
        ["endpoint"],
    )
    _PROMETHEUS_AVAILABLE = True
except ImportError:
    _PROMETHEUS_AVAILABLE = False

# ── Rate limiter ──────────────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Al-Hashadeh Educational Material Generator",
    description="Production-ready system for generating educational materials using the Al-Hashadeh methodology",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Set up CORS – origins come from CORS_ORIGINS env var (comma-separated)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add authentication middleware
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(generations.router, prefix="/generations", tags=["generations"])
app.include_router(materials.router, prefix="/materials", tags=["materials"])
app.include_router(search.router, prefix="/search", tags=["search"])


@app.get("/")
async def root():
    return {"message": "Welcome to Al-Hashadeh Educational Material Generator"}


@app.get("/health")
async def health_check():
    """
    Full health check — verifies DB and Redis connectivity.
    Returns 200 even when components are degraded so load-balancers can decide.
    """
    result: dict = {"status": "healthy", "components": {}}

    # Database
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        result["components"]["database"] = "healthy"
    except Exception as exc:
        result["components"]["database"] = f"unhealthy: {exc}"
        result["status"] = "degraded"

    # Redis
    try:
        cache = CacheService()
        result["components"]["redis"] = "healthy" if cache.available else "unavailable"
    except Exception as exc:
        result["components"]["redis"] = f"unhealthy: {exc}"

    # Gemini API key presence (not connectivity — avoids API cost on every health check)
    result["components"]["gemini_key"] = "configured" if settings.GEMINI_API_KEY else "missing"

    log.info("health_check", status=result["status"])
    return result


@app.get("/metrics")
async def metrics():
    """Prometheus-compatible metrics endpoint."""
    if not _PROMETHEUS_AVAILABLE:
        return Response("# prometheus-client not installed\n", media_type="text/plain")
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)
