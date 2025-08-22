from __future__ import annotations
import json
from typing import Any, Dict, List
import requests

BASE = "https://fantasy.premierleague.com/api"

def fetch_bootstrap() -> Dict[str, Any]:
    r = requests.get(f"{BASE}/bootstrap-static/")
    r.raise_for_status()
    return r.json()

def fetch_fixtures() -> List[Dict[str, Any]]:
    r = requests.get(f"{BASE}/fixtures/")
    r.raise_for_status()
    return r.json()

def next_gw(bootstrap: Dict[str, Any]) -> int | None:
    for ev in bootstrap.get("events", []):
        if not ev.get("finished") and not ev.get("is_previous"):
            return int(ev["id"])
    return None

def players(bootstrap: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(bootstrap.get("elements", []))

def team_short_name(bootstrap: Dict[str, Any], team_id: int) -> str:
    teams = {t["id"]: t["short_name"] for t in bootstrap.get("teams", [])}
    return teams.get(team_id, "?")

def dump_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
