from typing import List
from . import solver

Grid = List[List[int]]

DIFFICULTY_CLUES = {
    "easy": 36,    # more clues
    "medium": 30,
    "hard": 24,
}

def generate_puzzle(difficulty: str = "easy") -> Grid:
    """
    Generate a puzzle for the requested difficulty and ensure it has exactly one solution.
    Strategy (simple): generate a full grid, remove cells until desired clue count reached,
    checking uniqueness after removals. This is not the fastest but ensures uniqueness.
    """
    difficulty = difficulty if difficulty in DIFFICULTY_CLUES else "easy"
    target_clues = DIFFICULTY_CLUES[difficulty]

    full = solver.generate_full_grid()  # must produce a completed 9x9 grid
    puzzle = [row[:] for row in full]

    # Naive removal order: random. Keep removing while ensuring uniqueness until clue count reached.
    import random
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    for r, c in cells:
        if sum(1 for row in puzzle for v in row if v != 0) <= target_clues:
            break
        saved = puzzle[r][c]
        puzzle[r][c] = 0
        # use solver.count_solutions: stop counting after 2 to speed up
        cnt = solver.count_solutions(puzzle, limit=2)
        if cnt != 1:
            # revert if removal makes puzzle non-unique
            puzzle[r][c] = saved

    return puzzle

class SudokuGenerator:
    def __init__(self, size=9):
        self.size = size
        self.board = [[0] * size for _ in range(size)]

    def generate(self):
        self.fill_values()
        self.remove_numbers()

    def fill_values(self):
        # Fill the board with a valid Sudoku configuration
        pass

    def remove_numbers(self):
        # Remove numbers from the board to create the puzzle
        pass

    def get_board(self):
        return self.board

    def is_valid(self, row, col, num):
        # Check if placing num at (row, col) is valid
        pass

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) for num in row))
