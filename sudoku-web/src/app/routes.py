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
        solver = SudokuSolver()
        solution = solver.solve(puzzle)
        return jsonify(solution=solution)
    return render_template('game.html')

@bp.route('/generate', methods=['POST'])
def generate():
    generator = SudokuGenerator()
    puzzle = generator.generate()
    return jsonify(puzzle=puzzle)