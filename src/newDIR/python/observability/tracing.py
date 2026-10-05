"""OpenTelemetry tracing configuration."""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def setup_tracer(service_name: str = "devtools-engine", use_console: bool = True):
    """Configure TracerProvider and set global tracer."""
    provider = TracerProvider()
    if use_console:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name, "1.0.0")


def get_current_span():
    """Get current active span from context."""
    return trace.get_current_span()
