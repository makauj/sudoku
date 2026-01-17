from flask import Blueprint, render_template, request, jsonify
from .sudoku.solver import SudokuSolver
from .sudoku.generator import SudokuGenerator

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        puzzle = request.json.get('puzzle')
        solver = SudokuSolver(puzzle)
        solution = solver.solve()
        return jsonify(solution=solution)
    return render_template('game.html')

@bp.route('/generate', methods=['POST'])
def generate():
    generator = SudokuGenerator()
    puzzle = generator.generate()
    return jsonify(puzzle=puzzle)

@bp.route('/solve', methods=['POST'])
def solve():
    puzzle = request.json.get('puzzle')
    solver = SudokuSolver(puzzle)
    solution = solver.solve()
    return jsonify(solution=solution)

@bp.route('/validate', methods=['POST'])
def validate():
    puzzle = request.json.get('puzzle')
    row = request.json.get('row')
    col = request.json.get('col')
    num = request.json.get('num')
    solver = SudokuSolver(puzzle)
    is_valid = solver.is_valid(row, col, num)
    return jsonify(valid=is_valid)

@bp.route('/hint', methods=['POST'])
def hint():
    puzzle = request.json.get('puzzle')
    solver = SudokuSolver(puzzle)
    hint = solver.get_hint(puzzle)
    return jsonify(hint=hint)

@bp.route('/register', methods=['POST'])
def register():
    user_data = request.json
    
    # Placeholder for user registration logic
    # e.g., save user_data to database
    return jsonify(status="success", message="User registered successfully")