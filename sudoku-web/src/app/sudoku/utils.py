def validate_board(board):
    # Check if the board is a valid Sudoku board
    for row in board:
        if len(row) != 9 or not all(isinstance(num, int) and 0 <= num <= 9 for num in row):
            return False

    # Check rows, columns, and 3x3 squares for duplicates
    for i in range(9):
        row_nums = set()
        col_nums = set()
        square_nums = set()

        for j in range(9):
            # Validate rows
            if board[i][j] != 0 and board[i][j] in row_nums:
                return False
            row_nums.add(board[i][j])

            # Validate columns
            if board[j][i] != 0 and board[j][i] in col_nums:
                return False
            col_nums.add(board[j][i])

            # Validate 3x3 squares
            square_row = 3 * (i // 3)
            square_col = 3 * (i % 3)
            if board[square_row + j // 3][square_col + j % 3] != 0:
                if board[square_row + j // 3][square_col + j % 3] in square_nums:
                    return False
                square_nums.add(board[square_row + j // 3][square_col + j % 3])

    return True

def format_board(board):
    # Convert the board into a string format for display
    return "\n".join(" ".join(str(num) for num in row) for row in board)