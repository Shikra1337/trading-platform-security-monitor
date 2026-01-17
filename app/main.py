from app.detection import process_event
from app.logging_utils import load_alerts, log_alert, log_event
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Trading Platform Security Monitor")


class Event(BaseModel):
    event: str
    user: str | None = None
    ip: str | None = None
    success: bool | None = None


ALERTS: list[dict] = load_alerts()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/event")
def ingest_event(e: Event):
    event = e.model_dump()
    log_event({"type": "event_received", "event": event})

    alert = process_event(event)
    alert_created = False
    if alert:
        log_alert({"type": "alert_created", "alert": alert})
        ALERTS.append(alert)
        alert_created = True

    return {"received": True, "event": event, "alert_created": alert_created}


@app.get("/alerts")
def get_alerts(
    user: str | None = None,
    ip: str | None = None,
    alert_type: str | None = None,
    severity: str | None = None,
):
    filtered = [
        alert
        for alert in ALERTS
        if (user is None or alert.get("user") == user)
        and (ip is None or alert.get("ip") == ip)
        and (alert_type is None or alert.get("alert_type") == alert_type)
        and (severity is None or alert.get("severity") == severity)
    ]
    return {"count": len(filtered), "alerts": filtered}

