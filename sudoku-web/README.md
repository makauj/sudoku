# Sudoku Web Application

This is a web-based Sudoku game application built with Python. The application allows users to play Sudoku puzzles, generate new puzzles, and solve existing ones.

## Project Structure

```python
sudoku-web
├── src
│   ├── app
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   └── sudoku
│   │       ├── solver.py
│   │       ├── generator.py
│   │       └── utils.py
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── game.html
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   └── js
│   │       └── app.js
│   └── tests
│       ├── test_solver.py
│       └── test_api.py
├── requirements.txt
├── Dockerfile
├── Procfile
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd sudoku-web
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   python src/app/main.py
   ```

5. **Access the application:**
   Open your web browser and go to `http://localhost:5000`.

## Requirements

- Python 3.11
- See pinned deps in requirements.txt

## Environment

Create a local .env from `.env.example` and set:

- SECRET_KEY — required for session security
- FLASK_ENV — development or production
- RATELIMIT_DEFAULT — e.g. "100/hour"

Use python-dotenv locally; production should provide env vars via your deployment platform.

## Features

- Generate new Sudoku puzzles.
- Solve existing puzzles.
- Interactive game interface.
- Responsive design for various devices.

## Testing

To run the tests, ensure you have installed the dependencies and then execute:

```bash
pytest src/tests
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
