from app.sudoku import solver

def pretty(grid):
    for r in grid:
        print(" ".join(str(v or ".") for v in r))

g = solver.generate_full_grid()
print("Generated full grid:")
pretty(g)

# create a puzzle by blanking some cells
puzzle = [row[:] for row in g]
for i in range(0, 9, 2):
    puzzle[i][i] = 0
print("\nPuzzle sample:")
pretty(puzzle)

cnt = solver.count_solutions(puzzle, limit=10)
print(f"\nSolutions found (<=10): {cnt}")