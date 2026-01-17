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
    """
    _fill_grid: Fill the grid using randomized backtracking.
      grid: partially filled 9x9 grid (list-of-lists), modified in-place
    """
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
    """
    Small helper class wrapping the module solver utilities.
    Provides:
    - is_valid(row,col,num): check placement on current board
    - find_empty(): returns (r,c) or None
    - solve(puzzle=None): if puzzle provided, returns solved Grid or None; if no puzzle, solves self.board in-place and returns solved grid or None
    - solved_grid(): returns a copy of the solved board (or None)
    - is_valid_solution(grid): validate a completed solution grid
    """
    def __init__(self, board: Grid):
        # expect a 9x9 list-of-lists; operate in-place on a copy if needed
        self.board: Grid = board

    def is_valid(self, row: int, col: int, num: int) -> bool:
        # row check (skip the target cell)
        for j in range(9):
            if j != col and self.board[row][j] == num:
                return False
        # col check
        for i in range(9):
            if i != row and self.board[i][col] == num:
                return False
        # 3x3 block check
        br, bc = (row // 3) * 3, (col // 3) * 3
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if (i != row or j != col) and self.board[i][j] == num:
                    return False
        return True

    def find_empty(self) -> Optional[Tuple[int, int]]:
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def _solve_inplace(self) -> bool:
        """Backtracking solver operating on self.board in-place. Returns True if solved."""
        loc = self.find_empty()
        if loc is None:
            return True
        r, c = loc
        for v in range(1, 10):
            if self.is_valid(r, c, v):
                self.board[r][c] = v
                if self._solve_inplace():
                    return True
                self.board[r][c] = 0
        return False

    @staticmethod
    def _initial_board_valid(board: Grid) -> bool:
        """Return False if the initial (possibly partial) board contains duplicate non-zero entries."""
        # rows
        for r in range(9):
            seen = set()
            for v in board[r]:
                if v == 0:
                    continue
                if v in seen:
                    return False
                seen.add(v)
        # cols
        for c in range(9):
            seen = set()
            for r in range(9):
                v = board[r][c]
                if v == 0:
                    continue
                if v in seen:
                    return False
                seen.add(v)
        # blocks
        for br in (0, 3, 6):
            for bc in (0, 3, 6):
                seen = set()
                for i in range(br, br + 3):
                    for j in range(bc, bc + 3):
                        v = board[i][j]
                        if v == 0:
                            continue
                        if v in seen:
                            return False
                        seen.add(v)
        return True

    def solve(self, puzzle: Optional[Grid] = None) -> Optional[Grid]:
        """
        If puzzle is provided, attempt to solve it and return a solved grid or None.
        If puzzle is None, attempt to solve self.board in-place and return solved grid or None.
        """
        if puzzle is not None:
            # defensive copy
            board_copy = [row[:] for row in puzzle]
            if not SudokuSolver._initial_board_valid(board_copy):
                return None
            solver = SudokuSolver(board_copy)
            if solver._solve_inplace():
                return solver.board
            return None
        else:
            if not SudokuSolver._initial_board_valid(self.board):
                return None
            if self._solve_inplace():
                return self.board
            return None

    def solved_grid(self) -> Optional[Grid]:
        board_copy = [row[:] for row in self.board]
        solver = SudokuSolver(board_copy)
        if solver._solve_inplace():
            return solver.board
        return None

    @staticmethod
    def is_valid_solution(grid: Grid) -> bool:
        """Validate a completed solution grid: all rows/cols/blocks contain digits 1..9 exactly once."""
        # shape check
        if not (isinstance(grid, list) and len(grid) == 9 and all(isinstance(r, list) and len(r) == 9 for r in grid)):
            return False
        required = set(range(1, 10))
        # rows
        for r in grid:
            if set(r) != required:
                return False
        # cols
        for c in range(9):
            col = {grid[r][c] for r in range(9)}
            if col != required:
                return False
        # blocks
        for br in (0, 3, 6):
            for bc in (0, 3, 6):
                block = set()
                for i in range(br, br + 3):
                    for j in range(bc, bc + 3):
                        block.add(grid[i][j])
                if block != required:
                    return False
        return True

    @staticmethod
    def from_existing_board(board: Grid) -> 'SudokuSolver':
        solver = SudokuSolver(board)
        return solver

    @staticmethod
    def from_puzzle_string(puzzle_string: str) -> 'SudokuSolver':
        board = [[int(puzzle_string[i * 9 + j]) if puzzle_string[i * 9 + j] != '.' else 0 for j in range(9)] for i in range(9)]
        return SudokuSolver(board)
    
    @staticmethod
    def get_hint(puzzle: Grid) -> Optional[Tuple[int, int, int]]:
        """
        Given a puzzle, return a hint as (row, col, num) for an empty cell,
        or None if no hint is available (e.g., puzzle is already complete or unsolvable).
        """
        solver = SudokuSolver(puzzle)
        loc = solver.find_empty()
        if loc is None:
            return None
        r, c = loc
        for v in range(1, 10):
            if solver.is_valid(r, c, v):
                return (r, c, v)
        return None
