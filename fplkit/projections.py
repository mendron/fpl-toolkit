from __future__ import annotations
from typing import Dict, Any, List, Tuple

POS_MAP = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}

def _fixture_difficulty(fixt: dict, team_id: int) -> int:
    if fixt["team_h"] == team_id:
        return int(fixt["team_h_difficulty"])
    if fixt["team_a"] == team_id:
        return int(fixt["team_a_difficulty"])
    return 3

def _avg_future_difficulty(fixtures: List[dict], team_id: int, gw: int, horizon: int = 2) -> float:
    future = [f for f in fixtures if int(f["event"] or 0) >= gw and (f["team_h"] == team_id or f["team_a"] == team_id)]
    future = sorted(future, key=lambda x: (x["event"] or 99))[:horizon]
    if not future:
        return 3.0
    vals = [_fixture_difficulty(f, team_id) for f in future]
    return sum(vals) / len(vals)

def project_player(p: Dict[str, Any], fixtures: List[dict], gw: int) -> float:
    try:
        form = float(p.get("form") or 0.0)
    except ValueError:
        form = 0.0
    try:
        ppg = float(p.get("points_per_game") or 0.0)
    except ValueError:
        ppg = 0.0

    base = 0.6 * form + 0.4 * ppg

    team_id = int(p.get("team") or 0)
    fdr = _avg_future_difficulty(fixtures, team_id, gw, horizon=2)
    adj = 1.0 + (3 - fdr) * 0.075  # 1 fácil:+15%, 3 neutro, 5 difícil:-15%
    return round(base * adj, 3)

def rank_players(bootstrap: Dict[str, Any], fixtures: List[dict], gw: int, pos: str, n: int = 10) -> List[Tuple[str, float]]:
    pos = pos.upper()
    pos_id = {v: k for k, v in POS_MAP.items()}[pos]
    results = []
    for p in bootstrap.get("elements", []):
        if int(p["element_type"]) != pos_id:
            continue
        if int(p.get("minutes", 0)) < 90:
            continue
        score = project_player(p, fixtures, gw)
        name = f'{p["first_name"]} {p["second_name"]}'
        results.append((name, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:n]
