// This file contains JavaScript code for client-side interactivity, handling user input and updating the game state.

document.addEventListener('DOMContentLoaded', () => {
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

    // Function to submit the board
    const submitBoard = () => {
        const boardState = Array.from(cells).map(cell => cell.value || 0);
        // Send the board state to the server for validation or solving
        fetch('/api/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ board: boardState }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.solution) {
                // Update the board with the solution
                for (let i = 0; i < cells.length; i++) {
                    cells[i].value = data.solution[i] || '';
                }
            } else {
                alert('No solution found!');
            }
        })
        .catch(error => console.error('Error:', error));
    };

    // Attach submit event listener
    document.getElementById('submit-button').addEventListener('click', submitBoard);
});