"""Prometheus metrics for application observability."""

from prometheus_client import Counter, Histogram, Gauge, generate_latest


REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API requests",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "api_request_duration_seconds",
    "Request latency in seconds",
    ["endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0],
)
ACTIVE_AGENTS = Gauge(
    "active_agents",
    "Number of active orchestration agents",
)


def get_metrics_output() -> bytes:
    """Return Prometheus metrics in text format."""
    return generate_latest()
