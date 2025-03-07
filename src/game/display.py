import curses

from .board import Board


class Display:
    def __init__(self):
        self.stdscr = None  # Will be set from main.py
        self.color_pairs = {
            0: 1,  # Default (white on black)
            2: 2,  # Green on black
            4: 3,  # Yellow on black
            8: 4,  # Red on black
            16: 5,  # Magenta on black
            32: 6,  # Blue on black
            64: 7,  # Cyan on black
            128: 2,  # Green on black
            256: 3,  # Yellow on black
            512: 4,  # Red on black
            1024: 5,  # Magenta on black
            2048: 6,  # Blue on black
        }
        self._init_colors()

    def _init_colors(self):
        """Initialize color pairs for curses."""
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)

    def show_board(self, board: Board):
        """Display the current state of the board."""
        self.stdscr.clear()

        # Display score
        self.stdscr.addstr(
            0, 0, f"Score: {board.score}", curses.color_pair(1) | curses.A_BOLD
        )

        # Calculate starting position to center the board
        start_y = 2
        start_x = 0

        # Draw the board
        for i, row in enumerate(board.grid):
            # Draw top border for each row
            self.stdscr.addstr(start_y + i * 3, start_x, "+" + "-------+" * board.size)

            # Draw cells
            for j, num in enumerate(row):
                # Draw vertical borders and number
                x_pos = start_x + j * 8
                if num == 0:
                    self.stdscr.addstr(start_y + i * 3 + 1, x_pos, "|       ")
                else:
                    self.stdscr.addstr(start_y + i * 3 + 1, x_pos, "|")
                    num_str = f"{num:^7}"
                    self.stdscr.addstr(
                        start_y + i * 3 + 1,
                        x_pos + 1,
                        num_str,
                        curses.color_pair(self.color_pairs.get(num, 1)) | curses.A_BOLD,
                    )

                # Draw last vertical border of the row
                if j == len(row) - 1:
                    self.stdscr.addstr(start_y + i * 3 + 1, x_pos + 7, "|")

            # Draw bottom border for last row
            if i == len(board.grid) - 1:
                self.stdscr.addstr(
                    start_y + i * 3 + 2, start_x, "+" + "-------+" * board.size
                )

        self.stdscr.refresh()

    def show_game_over(self, score: int):
        """Display game over message."""
        height, width = self.stdscr.getmaxyx()
        msg = "Game Over!"
        score_msg = f"Final Score: {score}"

        self.stdscr.addstr(
            height // 2,
            (width - len(msg)) // 2,
            msg,
            curses.color_pair(4) | curses.A_BOLD,
        )
        self.stdscr.addstr(
            height // 2 + 1,
            (width - len(score_msg)) // 2,
            score_msg,
            curses.color_pair(1) | curses.A_BOLD,
        )
        self.stdscr.refresh()

    def show_win(self, score: int):
        """Display win message."""
        height, width = self.stdscr.getmaxyx()
        msg = "Congratulations! You've reached 2048!"
        score_msg = f"Score: {score}"

        self.stdscr.addstr(
            height // 2,
            (width - len(msg)) // 2,
            msg,
            curses.color_pair(2) | curses.A_BOLD,
        )
        self.stdscr.addstr(
            height // 2 + 1,
            (width - len(score_msg)) // 2,
            score_msg,
            curses.color_pair(1) | curses.A_BOLD,
        )
        self.stdscr.refresh()
