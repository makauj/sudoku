def validate_board(board):
    # Basic shape/type checks
    if not isinstance(board, list) or len(board) != 9:
        return False
    for row in board:
        if not isinstance(row, list) or len(row) != 9:
            return False
        if not all(isinstance(num, int) and 0 <= num <= 9 for num in row):
            return False

    # Check rows, columns, and 3x3 squares for duplicates (only track non-zero values)
    for i in range(9):
        row_nums = set()
        col_nums = set()
        square_nums = set()

        for j in range(9):
            # Validate rows
            r_val = board[i][j]
            if r_val != 0:
                if r_val in row_nums:
                    return False
                row_nums.add(r_val)

            # Validate columns
            c_val = board[j][i]
            if c_val != 0:
                if c_val in col_nums:
                    return False
                col_nums.add(c_val)

            # Validate 3x3 squares
            square_row = 3 * (i // 3)
            square_col = 3 * (i % 3)
            s_val = board[square_row + j // 3][square_col + j % 3]
            if s_val != 0:
                if s_val in square_nums:
                    return False
                square_nums.add(s_val)

    return True

def format_board(board):
    # Convert the board into a string format for display
    return "\n".join(" ".join(str(num) for num in row) for row in board)
