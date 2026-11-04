"""Small deterministic research-task lifecycle primitive."""
from dataclasses import dataclass, field
from datetime import datetime, timezone

TASK_TRANSITIONS = {
    "queued": {"running", "cancelled"},
    "running": {"completed", "partial", "blocked", "failed", "cancelled"},
    "partial": {"running", "completed", "cancelled"},
    "blocked": {"running", "cancelled"},
    "failed": {"running", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}

@dataclass
class ResearchTask:
    research_task_id: str
    audit_id: str
    objective: str
    completion_criteria: tuple[str, ...]
    status: str = "queued"
    blocked_reason: str | None = None
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def transition(self, new_status: str, reason: str | None = None) -> None:
        if new_status not in TASK_TRANSITIONS:
            raise ValueError(f"Unknown research task status: {new_status}")
        if new_status not in TASK_TRANSITIONS[self.status]:
            raise ValueError(f"Invalid task transition: {self.status} -> {new_status}")
        if new_status in {"partial", "blocked", "failed"} and not reason:
            raise ValueError(f"{new_status} requires a reason")
        self.status = new_status
        self.blocked_reason = reason if new_status in {"partial", "blocked", "failed"} else None
        self.updated_at = datetime.now(timezone.utc).isoformat()
