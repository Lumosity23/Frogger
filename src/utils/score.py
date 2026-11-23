# Score :
# -   10pts --> pour avancer ( 0, -1 )
# -   50pts --> par chicken sauver
# - 1000pts --> pour les 5 chickens sauvees
# -   10pts --> par seconde non utiliser par round

import json
import os
import tempfile
from dataclasses import dataclass
from typing import Any

from src.utils import log

MAX_SAVE = 5
TABLE: dict[str, int] = {
    "FOWARD": 10,
    "FORWARD": 10,
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
        self.saved: bool = False
        self._load()

    def _load(self) -> None:
        """Charge les scores depuis le fichier JSON/JSONC."""
        if not os.path.exists(self.path_file):
            self.load_scores = {}
            self.leaderboard = []
            return
        try:
            with open(self.path_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    raw_data = {}
                else:
                    # Ignore les lignes de commentaires commençant par //
                    lines = [
                        line
                        for line in content.splitlines()
                        if not line.strip().startswith("//")
                    ]
                    raw_data = json.loads("\n".join(lines))
            self.load_scores = {
                int(k): v
                for k, v in raw_data.items()
                if str(k).isdigit() and isinstance(v, dict)
            }
            self.leaderboard = sorted(
                [val["score"] for val in self.load_scores.values()], reverse=True
            )
            # log.debug(self.leaderboard)
        except Exception as e:
            log.error(f"Échec du chargement des scores depuis {self.path_file} : {e}")
            self.load_scores = {}
            self.leaderboard = []

    @property
    def score(self) -> int:
        """Score total accumulé (tous les rounds + round en cours)."""
        return sum(self.rounds) + self.current_score

    @property
    def lowest_score(self) -> int:
        """Score le plus bas du leaderboard actuel."""
        return min(self.leaderboard) if self.leaderboard else 0

    @property
    def highest_score(self) -> int:
        """Score le plus élevé du leaderboard actuel."""
        return max(self.leaderboard) if self.leaderboard else 0

    @property
    def is_better(self) -> bool:
        """Vérifie si le score actuel est éligible pour entrer dans le leaderboard (Top 5)."""
        if self.score <= 0:
            return False
        if len(self.leaderboard) < MAX_SAVE:
            return True
        return self.score > self.lowest_score

    @property
    def is_high_score(self) -> bool:
        """Vérifie si le score actuel bat le meilleur score (#1) du leaderboard."""
        if self.score <= 0:
            return False
        if not self.leaderboard:
            return True
        return self.score > self.highest_score

    def get_rank(self) -> int | None:
        if not self.is_better:
            return None
        if self.is_high_score:
            return 1

        for i, score in enumerate(self.leaderboard):
            if self.score > score:
                return i + 1

    def _write_score(self) -> None:
        """Écrit les scores de manière atomique."""
        directory = os.path.dirname(os.path.abspath(self.path_file))
        os.makedirs(directory, exist_ok=True)
        try:
            fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self.load_scores, f, indent=2)
            os.replace(tmp_path, self.path_file)
        except (OSError, TypeError, ValueError) as e:
            log.error("Échec de l'écriture des scores dans %s : %s", self.path_file, e)
            if "tmp_path" in locals() and os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _next_game(self) -> None:
        self.rounds = []
        self.current_score = 0
        self.saved = False

    def next_round(self) -> None:
        self.rounds.append(self.current_score)
        self.current_score = 0

    def save_score(self, name: str = "PLAYER", seed: int = 0) -> bool:
        """Enregistre le score dans le leaderboard s'il est éligible."""
        if self.saved:
            return False
        if self.current_score > 0:
            self.next_round()
        final = self.score
        if final <= 0:
            return False

        self._load()
        can_save = (len(self.leaderboard) < MAX_SAVE) or (final > min(self.leaderboard))
        if can_save:
            clean_name = str(name).strip()[:10] or "PLAYER"
            self.load_scores[self.get_rank()] = {
                "score": final,
                "name": clean_name,
                "seed": seed,
            }
            best_keys = sorted(self.load_scores.keys(), reverse=True)[:MAX_SAVE]
            self.load_scores = {k: self.load_scores[k] for k in best_keys}
            self.leaderboard = sorted(self.load_scores.keys())
            self._write_score()
            self.saved = True
            return True
        return False

    def get_leaderboard(self) -> dict[int, dict[str, str]]:
        """
        Leaderboard --> :
            [int] : {
            "score" : 1234,
            "name"  : "Ju",
            "seed"  : 12532
            }
        """
        # leaderboard: dict[int, dict[str, Any]] = {}
        # for rank, key in enumerate(sorted(self.leaderboard, reverse=True), start=1):
        #    leaderboard[rank] = self.load_scores[rank]
        return self.load_scores.copy()  # leaderboard

    def update(self, action: str, iteration: int = 1) -> None:
        """Add a score action with times ( iteration )"""
        self.current_score += TABLE.get(action, 0) * iteration
