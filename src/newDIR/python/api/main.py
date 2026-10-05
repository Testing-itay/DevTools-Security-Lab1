"""FastAPI application with Prometheus metrics and Sentry integration."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_client import Counter, make_asgi_app
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

from api.routes import agents, health
from utils.config import get_settings

# Prometheus request counter - api.openai.com and api.anthropic.com calls tracked separately
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "path"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown hooks."""
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,
        environment=settings.environment,
    )
    app = FastAPI(
        title="DevTools Engine API",
        version="1.0.0",
        lifespan=lifespan,
    )

    @app.middleware("http")
    async def prometheus_middleware(request, call_next):
        response = await call_next(request)
        REQUEST_COUNT.labels(method=request.method, path=request.url.path).inc()
        return response

    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
    app.include_router(health.router)
    app.include_router(agents.router)
    return app


app = create_app()
