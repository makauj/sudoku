// This file contains JavaScript code for client-side interactivity, handling user input and updating the game state.

document.addEventListener('DOMContentLoaded', () => {
    // Render a 9x9 Sudoku board as input elements
    function renderBoard() {
        const board = document.getElementById('sudoku-board');
        board.innerHTML = '';
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                const input = document.createElement('input');
                input.type = 'text';
                input.maxLength = 1;
                input.className = 'cell';
                input.dataset.row = i;
                input.dataset.col = j;
                board.appendChild(input);
            }
        }
    }
    renderBoard();

    const board = document.getElementById('sudoku-board');
    const cells = board.getElementsByTagName('input');

    // Function to handle cell input
    const handleCellInput = (event) => {
        const value = event.target.value;
        if (value && (value < 1 || value > 9)) {
            alert('Please enter a number between 1 and 9');
            event.target.value = '';
        }
    };

    // Attach input event listeners to each cell
    for (let cell of cells) {
        cell.addEventListener('input', handleCellInput);
    }

    // Function to submit the board (solve)
    const submitBoard = () => {
        const boardState = [];
        for (let i = 0; i < 9; i++) {
            const row = [];
            for (let j = 0; j < 9; j++) {
                const idx = i * 9 + j;
                const val = parseInt(cells[idx].value) || 0;
                row.push(val);
            }
            boardState.push(row);
        }
        // Send the board state to the server for solving
        fetch('/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ puzzle: boardState }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.solution) {
                // Update the board with the solution
                for (let i = 0; i < 9; i++) {
                    for (let j = 0; j < 9; j++) {
                        const idx = i * 9 + j;
                        cells[idx].value = data.solution[i][j] || '';
                    }
                }
            } else {
                alert('No solution found!');
            }
        })
        .catch(error => console.error('Error:', error));
    };

    // Function to reset the board
    const resetBoard = () => {
        for (let cell of cells) {
            cell.value = '';
        }
    };

    // Attach event listeners to buttons
    document.getElementById('solve-button').addEventListener('click', submitBoard);
    document.getElementById('reset-button').addEventListener('click', resetBoard);
});