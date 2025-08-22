import math
from fplkit.projections import project_player, _avg_future_difficulty

def test_projection_basic_scales_with_form_and_ppg():
    player = {"form": "3.0", "points_per_game": "5.0", "team": 1, "minutes": 180}
    fixtures = [{"event": 2, "team_h": 1, "team_a": 2, "team_h_difficulty": 3, "team_a_difficulty": 3}]
    score = project_player(player, fixtures, gw=2)
    assert math.isclose(score, 3.8, rel_tol=1e-9)

def test_avg_future_difficulty_window_and_perspective():
    fixtures = [
        {"event": 10, "team_h": 1, "team_a": 2, "team_h_difficulty": 2, "team_a_difficulty": 4},
        {"event": 11, "team_h": 3, "team_a": 1, "team_h_difficulty": 4, "team_a_difficulty": 2},
        {"event": 12, "team_h": 4, "team_a": 5, "team_h_difficulty": 5, "team_a_difficulty": 5},
    ]
    fdr = _avg_future_difficulty(fixtures, team_id=1, gw=10, horizon=2)
    assert math.isclose(fdr, 2.0, rel_tol=1e-12)
