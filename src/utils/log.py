import time

_start = time.perf_counter()  # le moment où le programme démarre
LEVELS = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40}
_min_level = LEVELS["DEBUG"]  # état partagé par tous les fichiers


def set_level(name: str):
    global _min_level  # on modifie la variable du MODULE
    _min_level = LEVELS[name]


def _emit(level: str, msg: str):
    if LEVELS[level] >= _min_level:  # on filtre selon le niveau choisi
        print(f"[{time.perf_counter() - _start:8.3f}] {level:<5} {msg}")


def info(msg: str):
    _emit("INFO", msg)


def debug(msg: str):
    _emit("DEBUG", msg)


def error(msg: str):
    _emit("ERROR", msg)


def warn(msg: str):
    _emit("WARN", msg)
