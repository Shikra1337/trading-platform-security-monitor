from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

WINDOW_SECONDS = 30
THRESHOLD = 5
_FAILURES: Dict[Tuple[str, str], List[datetime]] = {}


def process_event(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if event.get("event") != "login_attempt":
        return None
    if event.get("success") is not False:
        return None

    user = event.get("user")
    ip = event.get("ip")
    if user is None or ip is None:
        return None

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(seconds=WINDOW_SECONDS)

    key = (user, ip)
    failures = [t for t in _FAILURES.get(key, []) if t >= cutoff]
    failures.append(now)
    _FAILURES[key] = failures

    fail_count = len(failures)
    if fail_count == THRESHOLD:
        return {
            "alert_type": "brute_force_suspected",
            "severity": "high",
            "user": user,
            "ip": ip,
            "window_seconds": WINDOW_SECONDS,
            "threshold": THRESHOLD,
            "fail_count": fail_count,
        }

    return None
