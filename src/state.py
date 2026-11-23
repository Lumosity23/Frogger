from enum import Enum, auto
from typing import Callable


class GameState(Enum):
    MENU = auto()
    PLAY = auto()
    PAUSE = auto()
    GAME_OVER = auto()
    LEADERBOARD = auto()


class StateManager:
    def __init__(self, initial: GameState = GameState.MENU) -> None:
        self._current: GameState = initial
        self._listeners: list[Callable[[GameState, GameState], None]] = []

    @property
    def current(self) -> GameState:
        return self._current

    def subscribe(self, callback: Callable[[GameState, GameState], None]) -> None:
        """Enregistre une fonction callback(new_state, old_state) appelée à chaque changement."""
        self._listeners.append(callback)

    def set(self, new_state: GameState) -> None:
        """Modifie l'état et prévient tout le monde immédiatement."""
        if new_state != self._current:
            old_state = self._current
            self._current = new_state
            for callback in self._listeners:
                callback(new_state, old_state)
