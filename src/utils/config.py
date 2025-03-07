from dataclasses import dataclass
import yaml


@dataclass
class GameConfig:
    board_size: int = 4
    win_score: int = 2048
    animation_delay: float = 0.1

    @classmethod
    def from_yaml(cls, path: str) -> "GameConfig":
        with open(path, "r") as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)
