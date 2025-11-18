import pytest
from app.sudoku import generator, solver

@pytest.mark.parametrize("difficulty,min_clues", [
    ("easy", 34),
    ("medium", 28),
    ("hard", 22),
])
def test_generate_unique_solution_and_clues(difficulty, min_clues):
    puzzle = generator.generate_puzzle(difficulty)
    # ensure uniqueness
    assert solver.count_solutions(puzzle, limit=2) == 1
    # ensure minimum expected clues roughly match difficulty (allow some variance)
    clues = sum(1 for r in puzzle for v in r if v != 0)
    assert clues >= min_clues, f"{difficulty} produced too few clues: {clues}"