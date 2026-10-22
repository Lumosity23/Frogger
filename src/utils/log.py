import time

_start = time.perf_counter()                      # le moment où le programme démarre
LEVELS = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40}
_min_level = LEVELS["DEBUG"]                      # état partagé par tous les fichiers

def set_level(name):
    global _min_level                              # on modifie la variable du MODULE
    _min_level = LEVELS[name]

def _emit(level, msg):
    if LEVELS[level] >= _min_level:                # on filtre selon le niveau choisi
        print(f"[{time.perf_counter() - _start:8.3f}] {level:<5} {msg}")

def info(msg):  _emit("INFO", msg)
def debug(msg): _emit("DEBUG", msg)
