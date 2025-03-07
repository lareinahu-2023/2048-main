#!/usr/bin/env python3
import curses
import argparse
from game import GameController
from utils import GameConfig, setup_logger
from game.display import Display
from monitoring.start_prometheus import init_metrics_exporter


def parse_args():
    parser = argparse.ArgumentParser(description="2048 Game")
    parser.add_argument("--config", type=str, help="Path to config file")
    parser.add_argument("--log-file", type=str, help="Path to log file")
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level",
    )
    return parser.parse_args()


def load_config(config_path=None):
    if config_path:
        return GameConfig.from_yaml(config_path)
    return GameConfig()


def main(stdscr):
    # Hide cursor
    curses.curs_set(0)

    # Parse arguments
    args = parse_args()

    # Setup logging
    setup_logger(args.log_level, args.log_file)

    # Initialize metrics exporter
    init_metrics_exporter()

    # Load config
    config = load_config(args.config)

    # Initialize display and game
    display = Display()
    display.stdscr = stdscr  # Use the main window from curses.wrapper
    display._init_colors()  # Initialize colors

    game = GameController(config)
    game.display = display  # Update display reference
    game.start_game()

    # Game loop
    while True:
        key = stdscr.getch()

        if key == ord("q"):
            break

        direction = None
        if key == curses.KEY_UP:
            direction = "up"
        elif key == curses.KEY_DOWN:
            direction = "down"
        elif key == curses.KEY_LEFT:
            direction = "left"
        elif key == curses.KEY_RIGHT:
            direction = "right"

        if direction:
            game.handle_move(direction)


if __name__ == "__main__":
    curses.wrapper(main)
