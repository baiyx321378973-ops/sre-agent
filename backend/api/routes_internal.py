from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from backend.services.observability_service import build_metrics_snapshot

router = APIRouter(prefix="/internal", tags=["internal"])


@router.get("/metrics")
def internal_metrics():
    return {
        "service": "sre-agent",
        "metrics": build_metrics_snapshot(),
    }


@router.get("/prometheus", response_class=PlainTextResponse)
def prometheus_metrics():
    metrics = build_metrics_snapshot()
    lines = [
        "# HELP sre_agent_request_total Total number of handled HTTP requests.",
        "# TYPE sre_agent_request_total counter",
        f"sre_agent_request_total {metrics['request_count']}",
        "# HELP sre_agent_success_rate_pct Successful request ratio in percentage.",
        "# TYPE sre_agent_success_rate_pct gauge",
        f"sre_agent_success_rate_pct {metrics['success_rate_pct']}",
        "# HELP sre_agent_avg_response_time_ms Average response time in milliseconds.",
        "# TYPE sre_agent_avg_response_time_ms gauge",
        f"sre_agent_avg_response_time_ms {metrics['avg_response_time_ms']}",
        "# HELP sre_agent_p95_response_time_ms P95 response time in milliseconds.",
        "# TYPE sre_agent_p95_response_time_ms gauge",
        f"sre_agent_p95_response_time_ms {metrics['p95_response_time_ms']}",
    ]
    return "\n".join(lines) + "\n"
