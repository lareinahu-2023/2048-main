import pytest
from unittest.mock import Mock
from game.controller import GameController
from utils.config import GameConfig


class TestGame:
    @pytest.fixture
    def game(self, monkeypatch):
        # Mock Display and GameMetrics
        mock_display = Mock()
        mock_metrics = Mock()

        def mock_display_class():
            return mock_display

        def mock_metrics_class():
            return mock_metrics

        # Patch the Display and GameMetrics classes
        monkeypatch.setattr("game.controller.Display", mock_display_class)
        monkeypatch.setattr("game.controller.GameMetrics", mock_metrics_class)

        config = GameConfig(board_size=4, win_score=2048)
        return GameController(config)

    def test_game_initialization(self, game):
        """Test that game initializes correctly."""
        game.start_game()
        # After initialization, board should have exactly two non-zero tiles
        non_zero_count = sum(1 for row in game.board.grid for cell in row if cell != 0)
        assert non_zero_count == 2

    def test_win_condition(self, game):
        """Test that game recognizes win condition."""
        game.start_game()
        # Set up a winning board state
        game.board.grid = [
            [2048, 2, 4, 8],
            [16, 32, 64, 128],
            [256, 512, 1024, 4],
            [2, 4, 8, 16],
        ]
        # Simulate a move that would trigger win check
        assert game._check_win() == True

    def test_game_over_condition(self, game):
        """Test that game recognizes game over condition."""
        game.start_game()
        # Set up a game over board state (no valid moves possible)
        game.board.grid = [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]]
        assert game.board.is_game_over() == True

    def test_invalid_move_handling(self, game):
        """Test that invalid moves are handled correctly."""
        game.start_game()
        with pytest.raises(Exception):
            game.handle_move("invalid")

    def test_score_tracking(self, game):
        """Test that score is tracked correctly."""
        game.start_game()
        initial_score = game.board.score
        # Set up a board where a merge will happen
        game.board.grid = [[2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        game.handle_move("left")
        # After merging two 2s, score should increase by 4
        assert game.board.score == initial_score + 4
