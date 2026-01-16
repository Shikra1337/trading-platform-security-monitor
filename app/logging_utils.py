import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

LOG_DIR = Path("logs")
EVENT_LOG = LOG_DIR / "events.jsonl"
ALERT_LOG = LOG_DIR / "alerts.jsonl"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_event(record: Dict[str, Any]) -> None:
    """
    record: JSON'a çevrilebilir dict.
    JSONL formatında (her satır 1 JSON) hem dosyaya yazar hem ekrana basar.
    """
    LOG_DIR.mkdir(exist_ok=True)

    out = dict(record)
    out["ts"] = _now_iso()

    line = json.dumps(out, ensure_ascii=False)

    # terminal
    print(line)

    # dosya
    with EVENT_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def log_alert(record: Dict[str, Any]) -> None:
    LOG_DIR.mkdir(exist_ok=True)

    out = dict(record)
    out["ts"] = _now_iso()

    line = json.dumps(out, ensure_ascii=False)

    # terminal
    print(line)

    # dosya
    with ALERT_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
