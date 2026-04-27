"""Domain model for authenticated session context."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class SessionEntity:
    """Core session domain representation."""

    token: str
    userid: str
    username: str
    login_timestamp: datetime
