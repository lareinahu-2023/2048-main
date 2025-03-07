import time
from dataclasses import dataclass
from typing import Dict
from prometheus_client import Counter, Gauge, Histogram


@dataclass
class GameMetrics:
    moves_counter = Counter("game_moves_total", "Total number of moves", ["direction"])
    score_gauge = Gauge("game_score", "Current game score")
    game_duration = Histogram("game_duration_seconds", "Game duration in seconds")
    errors_counter = Counter("game_errors_total", "Total number of errors", ["type"])
    tiles_spawned = Counter("game_tiles_spawned", "Tiles spawned by value", ["value"])

    def __init__(self):
        self.start_time = None

    def record_game_start(self):
        self.start_time = time.time()

    def record_game_end(self, result: str):
        if self.start_time:
            duration = time.time() - self.start_time
            self.game_duration.observe(duration)

    def record_move(self, direction: str):
        self.moves_counter.labels(direction=direction).inc()

    def record_score(self, score: int):
        self.score_gauge.set(score)

    def record_error(self, error_type: str):
        self.errors_counter.labels(type=error_type).inc()

    def record_tile_spawn(self, value: int):
        self.tiles_spawned.labels(value=str(value)).inc()
