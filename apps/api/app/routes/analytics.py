from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary")
def analytics_summary() -> dict[str, object]:
    return {
        "active_agents": 4,
        "tasks_completed_today": 27,
        "automation_hours_saved": 68,
        "campaign_roi_signal": "+18% projected uplift",
        "focus_market": "Nepal telecom",
    }
