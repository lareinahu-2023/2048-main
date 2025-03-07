import pytest
from game.board import Board


class TestBoard:
    @pytest.fixture
    def board(self):
        return Board(4)

    def test_move_left(self, board):
        board.grid = [[2, 2, 0, 0], [0, 2, 2, 0], [0, 0, 2, 2], [2, 0, 0, 2]]
        board.move("left")
        assert board.grid == [[4, 0, 0, 0], [4, 0, 0, 0], [4, 0, 0, 0], [4, 0, 0, 0]]

    def test_game_over(self, board):
        board.grid = [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]]
        assert board.is_game_over() == True

    def test_move_right(self, board):
        board.grid = [[2, 2, 0, 0], [0, 2, 2, 0], [0, 0, 2, 2], [2, 0, 0, 2]]
        board.move("right")
        assert board.grid == [[0, 0, 0, 4], [0, 0, 0, 4], [0, 0, 0, 4], [0, 0, 0, 4]]

    def test_move_up(self, board):
        board.grid = [[2, 0, 0, 2], [2, 0, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0]]
        board.move("up")
        assert board.grid == [[4, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def test_move_down(self, board):
        board.grid = [[2, 0, 0, 2], [2, 0, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0]]
        board.move("down")
        assert board.grid == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [4, 0, 0, 4]]

    def test_invalid_move(self, board):
        with pytest.raises(Exception):
            board.move("invalid")
