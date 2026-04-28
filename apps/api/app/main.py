import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("devex-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Developer Experience Hub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics/dora")
def get_dora_metrics():
    return {
        "deployment_frequency": "12.4 / week",
        "lead_time_for_changes": "1.2 days",
        "change_failure_rate": "4.2%",
        "time_to_restore_service": "45 mins",
        "rating": "Elite"
    }

@app.get("/metrics/flow")
def get_flow_metrics():
    return {
        "flow_efficiency": "64%",
        "active_wip_per_dev": 2.4,
        "avg_pr_cycle_time": "14h",
        "bottleneck_alerts": 2
    }

@app.get("/platform/adoption")
def get_platform_adoption():
    return [
        {"tool": "Service Catalog", "adoption": "92%", "trend": "up"},
        {"tool": "Kubernetes Self-Service", "adoption": "74%", "trend": "up"},
        {"tool": "CI Templates", "adoption": "88%", "trend": "stable"}
    ]

@app.get("/surveys/results")
def get_survey_results():
    return {
        "overall_satisfaction": 4.2,
        "participation_rate": "84%",
        "top_friction_points": ["Jira configuration", "Wait for security review"]
    }

@app.get("/scores/summary")
def get_scores_summary():
    return {
        "global_devex_index": 0.882,
        "productivity_score": 0.91,
        "satisfaction_score": 0.84,
        "retention_risk": "LOW"
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_active_engineers": 450,
        "onboarding_velocity": "4 days to first PR",
        "platform_roi_est": "$1.2M / year",
        "engineering_flow_state": "OPTIMAL"
    }
