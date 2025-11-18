class SudokuBoard:
    def __init__(self, board=None):
        if board is None:
            self.board = [[0 for _ in range(9)] for _ in range(9)]
        else:
            self.board = board

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False

        return True

    def place_number(self, row, col, num):
        if self.is_valid(row, col, num):
            self.board[row][col] = num
            return True
        return False

    def remove_number(self, row, col):
        self.board[row][col] = 0

    def is_complete(self):
        return all(all(cell != 0 for cell in row) for row in self.board)

    def get_board(self):
        return self.board

    def set_board(self, board):
        self.board = board