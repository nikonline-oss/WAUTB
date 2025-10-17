# app/templating.py
from __future__ import annotations

from datetime import datetime, date, timezone
from fastapi.templating import Jinja2Templates

_templates: Jinja2Templates | None = None

def _rusdate(value):
    if isinstance(value, (datetime, date)):
        return value.strftime("%d.%m.%Y")
    try:
        # если пришла строка 'YYYY-MM-DD'
        return datetime.fromisoformat(str(value)).strftime("%d.%m.%Y")
    except Exception:
        return value

def get_templates() -> Jinja2Templates:
    global _templates
    if _templates is None:
        t = Jinja2Templates(directory="app/templates")
        t.env.globals["now"] = lambda: datetime.now(timezone.utc)
        t.env.filters["rusdate"] = _rusdate
        _templates = t
    return _templates