import random
from typing import List, Optional, Tuple

Grid = List[List[int]]

def _find_empty(grid: Grid) -> Optional[Tuple[int, int]]:
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None

def _is_valid(grid: Grid, r: int, c: int, val: int) -> bool:
    # row/col check
    if any(grid[r][j] == val for j in range(9)):
        return False
    if any(grid[i][c] == val for i in range(9)):
        return False
    # 3x3 block
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if grid[i][j] == val:
                return False
    return True

def _solve_count(grid: Grid, limit: int, counter: List[int]) -> None:
    loc = _find_empty(grid)
    if loc is None:
        counter[0] += 1
        return
    r, c = loc
    for v in range(1, 10):
        if counter[0] >= limit:
            return
        if _is_valid(grid, r, c, v):
            grid[r][c] = v
            _solve_count(grid, limit, counter)
            grid[r][c] = 0
            if counter[0] >= limit:
                return

def count_solutions(puzzle: Grid, limit: int = 2) -> int:
    """
    Count solutions for `puzzle`. Stops and returns as soon as count reaches `limit`.
    Uses backtracking; returns integer count (<= limit).
    """
    grid_copy = [row[:] for row in puzzle]
    counter = [0]
    _solve_count(grid_copy, limit, counter)
    return counter[0]

def _fill_grid(grid: Grid) -> bool:
    loc = _find_empty(grid)
    if loc is None:
        return True
    r, c = loc
    nums = list(range(1, 10))
    random.shuffle(nums)
    for v in nums:
        if _is_valid(grid, r, c, v):
            grid[r][c] = v
            if _fill_grid(grid):
                return True
            grid[r][c] = 0
    return False

def generate_full_grid() -> Grid:
    """
    Generate a completed 9x9 sudoku grid using randomized backtracking.
    """
    grid: Grid = [[0] * 9 for _ in range(9)]
    success = _fill_grid(grid)
    if not success:
        # retry once if unlucky (should rarely happen)
        grid = [[0] * 9 for _ in range(9)]
        _fill_grid(grid)
    return grid

class SudokuSolver:
    def __init__(self, board):
        self.board = board

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
