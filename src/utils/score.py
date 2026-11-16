# Score :
# -   10pts --> pour avancer ( 0, -1 )
# -   50pts --> par chicken sauver
# - 1000pts --> pour les 5 chickens sauvees
# -   10pts --> par seconde non utiliser par round

import json
from dataclasses import dataclass
from typing import Any

MAX_SAVE = 5
TABLE: dict[str, int] = {
    "FOWARD": 10,
    "CHICKEN_SAVE": 50,
    "ALL_SAVE": 1000,
    "TIME_LEFT": 10,
}


@dataclass
class score:
    path_file: str

    def __post_init__(self):
        self.rounds: list[int] = []
        self.current_score: int = 0
        self.load_scores: dict[int, dict[str, Any]] = {}
        self.leaderboard: list[int] = []
        with open(self.path_file) as f:
            self.load_scores = json.load(f)
        self.leaderboard = sorted([score for score in self.load_scores])

    @property
    def score(self) -> int:
        return sum(self.rounds)

    @property
    def lowest_score(self) -> int:
        return min(self.leaderboard)

    @property
    def is_better(self) -> bool:
        return self.score > self.lowest_score

    def next_round(self):
        self.rounds.append(self.current_score)
        self.current_score = 0

    def save_score(self, name: str, seed: int):
        if len(self.leaderboard) <= MAX_SAVE or self.is_better:
            new_score = {"name": name, "seed": seed}
            self.load_scores[self.score] = new_score

    def get_leaderboard(self) -> dict[int, dict[str, str]]:
        """
        Leaderboard --> :
            [int] : {
            "score" : "1234"
            "name"  : "Ju"
            "seed"  : "12532"
            }
        """
        leaderboard: dict[int, dict[str, str]] = {}
        for score, i in enumerate(self.leaderboard):
            place = self.load_scores[score]
            place["score"] = score
            leaderboard[i + 1] = place

        return leaderboard

    def update(self, action: str, iteration: int = 1):
        """Add a score action with times ( iteration )"""
        self.current_score += TABLE.get(action, 0) * iteration
