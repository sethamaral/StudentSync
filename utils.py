import datetime

def parse_datetime(s: str) -> datetime.datetime:
    """
    Parse YYYY-MM-DD HH:MM into a datetime.
    Raises ValueError on bad input.
    """
    s = s.strip()
    try:
        return datetime.datetime.fromisoformat(s)
    except Exception:
        raise ValueError("Invalid format. Use YYYY-MM-DD HH:MM (e.g., 2025-12-01 14:00).")

def format_date(dt: datetime.datetime) -> str:
    return dt.strftime("%Y-%m-%d")

def format_time(dt: datetime.datetime) -> str:
    return dt.strftime("%H:%M")

def today_9am() -> datetime.datetime:
    now = datetime.datetime.now()
    return now.replace(hour=9, minute=0, second=0, microsecond=0)

def next_day_9am(dt: datetime.datetime) -> datetime.datetime:
    nxt = dt + datetime.timedelta(days=1)
    return nxt.replace(hour=9, minute=0, second=0, microsecond=0)
