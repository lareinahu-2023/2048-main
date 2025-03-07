import logging

from monitoring.metrics import GameMetrics
from utils.config import GameConfig

from .board import Board
from .display import Display

logger = logging.getLogger(__name__)


class GameController:
    def __init__(self, config: GameConfig):
        self.config = config
        self.board = Board(config.board_size)
        self.display = Display()
        self.metrics = GameMetrics()
        self.game_won = False
        logger.info("Game controller initialized")

    def start_game(self):
        """Initializes and starts a new game."""
        self.board.add_new_tile()
        self.board.add_new_tile()
        self.display.show_board(self.board)
        self.metrics.record_game_start()

    def handle_move(self, direction: str) -> bool:
        """Handles a move in the specified direction."""
        try:
            if self.board.move(direction):
                self.board.add_new_tile()
                self.display.show_board(self.board)
                self.metrics.record_score(self.board.score)

                # Check for win condition
                if not self.game_won and self._check_win():
                    self.game_won = True
                    self.display.show_win(self.board.score)
                    self.metrics.record_game_end("win")
                    return False

                # Check for game over
                if self.board.is_game_over():
                    self.display.show_game_over(self.board.score)
                    self.metrics.record_game_end("loss")
                    logger.info("Game over!")
                    return False

                return True
            return True
        except Exception as e:
            logger.error(f"Error handling move: {e}")
            self.metrics.record_error("move_error")
            raise

    def _check_win(self) -> bool:
        """Check if any tile has reached the win score."""
        for row in self.board.grid:
            if self.config.win_score in row:
                logger.info("Game won!")
                return True
        return False
