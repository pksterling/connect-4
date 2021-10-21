import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
WIN_COUNT = 4

def create_board():
  board = np.zeros((ROW_COUNT, COLUMN_COUNT))
  return board

def drop_piece(board, row, col, piece):
  board[row][col] = piece

def is_valid_location(board, col):
  return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
  for r in range(ROW_COUNT):
    if board[r][col] == 0:
      return r

def print_board(board):
  print(np.flip(board, 0))

def winning_move(board, piece):
  # Check horizontal locations for win
  for r in range(ROW_COUNT):
    for c in range(COLUMN_COUNT - 3):
      for p in range(WIN_COUNT):
        if board[r][c + p] == piece:
          if p == WIN_COUNT - 1:
            return True
          else:
            continue
        else:
          break

  # Check vertical locations for win
  for r in range(ROW_COUNT - WIN_COUNT + 1):
    for c in range(COLUMN_COUNT):
      for p in range(WIN_COUNT):
        if board[r + p][c] == piece:
          if p == WIN_COUNT - 1:
            return True
          else:
            continue
        else:
          break

  # Check positively sloped diagonals
  for r in range(ROW_COUNT - WIN_COUNT + 1):
    for c in range(COLUMN_COUNT - WIN_COUNT + 1):
      for p in range(WIN_COUNT):
        if board[r + p][c + p] == piece:
          if p == WIN_COUNT - 1:
            return True
          else:
            continue
        else:
          break
          break

  # Check negatively sloped diagonals
  for r in range(WIN_COUNT - 1, ROW_COUNT):
    for c in range(COLUMN_COUNT - WIN_COUNT + 1):
      for p in range(WIN_COUNT):
        if board[r - p][c + p] == piece:
          if p == WIN_COUNT - 1:
            return True
          else:
            continue
        else:
          break

board = create_board()
print_board(board)
game_over = False
turn = 0

player1 = input("Player 1, please enter your name:")
player2 = input("Player 2, please enter your name:")

while not game_over:
  # Ask for Player 1 Input
  if turn == 0:
    col = int(input("Player 1 Make your Selection (0-6):"))

    if is_valid_location(board, col):
      row = get_next_open_row(board, col)
      drop_piece(board, row, col, 1)

      if winning_move(board, 1):
        print("Player 1 Wins!!!")
        game_over = True

  # Ask for Player 2 Input
  else:
    col = int(input("Player 2 Make your Selection (0-6):"))

    if is_valid_location(board, col):
      row = get_next_open_row(board, col)
      drop_piece(board, row, col, 2)

      if winning_move(board, 1):
        print("Player 2 Wins!!!")
        game_over = True

  print_board(board)


  turn += 1
  turn = turn % 2
