# Score :
# -   10pts --> pour avancer ( 0, -1 )
# -   50pts --> par chicken sauver
# - 1000pts --> pour les 5 chickens sauvees
# -   10pts --> par seconde non utiliser par round

import json
import logging
import os
import tempfile
from dataclasses import dataclass
from typing import Any

log = logging.getLogger(__name__)

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
            # JSON transforme les clés en str : on les reconvertit en int
            self.load_scores = {int(k): v for k, v in json.load(f).items()}
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

    def _write_score(self):
        directory = os.path.dirname(os.path.abspath(self.path_file))
        try:
            # Écriture dans un fichier temporaire puis remplacement atomique,
            # pour ne jamais laisser un fichier de scores tronqué
            fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
            with os.fdopen(fd, "w") as f:
                json.dump(self.load_scores, f, indent=2)
            os.replace(tmp_path, self.path_file)

        except (OSError, TypeError, ValueError) as e:
            log.error("Échec de l'écriture des scores dans %s : %s", self.path_file, e)
            if "tmp_path" in locals() and os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _next_game(self):
        self.rounds = []
        self.current_score = 0

    def next_round(self):
        self.rounds.append(self.current_score)
        self.current_score = 0

    def save_score(self, name: str, seed: int):
        final = self.score
        if len(self.leaderboard) <= MAX_SAVE or final > min(self.load_scores):
            self.load_scores[final] = {"score": final, "name": name, "seed": seed}
            best = sorted(self.load_scores, reverse=True)[:MAX_SAVE]
            self.load_scores = {k: self.load_scores[k] for k in best}
            self.leaderboard = sorted(self.load_scores)
            self._write_score()
        self._next_game()

    def get_leaderboard(self) -> dict[int, dict[str, str]]:
        """
        Leaderboard --> :
            [int] : {
            "score" : "1234"
            "name"  : "Ju"
            "seed"  : "12532"
            }
        """
        leaderboard: dict[int, dict[str, Any]] = {}
        # Le meilleur score est en place 1
        for rank, key in enumerate(sorted(self.leaderboard, reverse=True), start=1):
            leaderboard[rank] = self.load_scores[key]

        return leaderboard

    def update(self, action: str, iteration: int = 1):
        """Add a score action with times ( iteration )"""
        self.current_score += TABLE.get(action, 0) * iteration
