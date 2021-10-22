# Use NumPy to create and manipulate a matrix (to be used as the game board)
import numpy
# Use to convert Python dictionary to JSON and vice versa
import json

ROW_COUNT = 6
COLUMN_COUNT = 7
WIN_COUNT = 4

def load_scoreboard():
  try:
    with open('scoreboard.json') as json_file:
      scoreboard = json.load(json_file)
  except FileNotFoundError:
    scoreboard = {}

  return scoreboard

def update_scoreboard(scoreboard, winner):
  scoreboard[winner]["Won"] += 1
  scoreboard[player1]["Played"] += 1
  scoreboard[player2]["Played"] += 1

  # Overwrite scoreboard file
  with open('scoreboard.json', 'w') as file:
    json.dump(scoreboard, file, ensure_ascii=False)



def create_board():
  # Create a matrix of 0s, representing the board
  board = numpy.zeros((ROW_COUNT, COLUMN_COUNT))
  return board

def input_player_name(player):
  try:
    name = input(f"Player {player}, please enter your name: ")
  except:
    print("Invalid input!")
    name = input(f"Player {player}, please enter your name: ")

  return name
  
def process_player_name(player):
  name = input_player_name(player)

  if name in scoreboard:
    print(f"Welcome back {name}!")
  else:
    # Add new player to scoreboard
    scoreboard[name] = {}
    scoreboard[name]["Played"] = 0
    scoreboard[name]["Won"] = 0
    print(f"Welcome to Connect 4, {name}!")

  return name

def print_score(player):
  won = scoreboard[player]["Won"]
  played = scoreboard[player]["Played"]
  print(f"{player}, you've won {won} out of {played} games!")

def pretty_cell(value):
  if value == 1:
    return "O|"
  elif value == 2:
    return "X|"
  else:
    return "_|"

def print_board(board):
  pretty_board = "\n"

  # Add column number row
  for col in range(COLUMN_COUNT):
    pretty_board += f" {col}"

  # Add each location to printable board
  for row in range(ROW_COUNT):
    pretty_board += "\n|"
    for col in range(COLUMN_COUNT):
      pretty_board += pretty_cell(board[ROW_COUNT - row - 1][col])

  print(pretty_board)

def is_valid_location(board, col):
  # Check the top row of a column is empty
  return board[ROW_COUNT - 1][col] == 0
  
def player_move(board, player):
  selection = input(f"{player} Make your selection (0-{COLUMN_COUNT - 1}): ")

  # Convert input string to integer
  try:
    selection = int(selection)
  except:
    print("Invalid input!")
    selection = player_move(board, player)

  # Check selection is within range
  if selection < 0 or selection > COLUMN_COUNT - 1:
    print("Invalid selection!")
    selection = player_move(board, player)

  # Check location is free
  if not is_valid_location(board, selection):
    print("Column already full!")
    selection = player_move(board, player)

  return selection

def get_next_open_row(board, col):
  # Check each row of a column, returning the first empty location
  for row in range(ROW_COUNT):
    if board[row][col] == 0:
      return row

def drop_piece(board, row, col, piece):
  # Change the relevant board location, from '0' to '1'/'2'
  board[row][col] = piece

def winning_move(board, piece):
  # Check horizontal locations for win
  for row in range(ROW_COUNT):
    for col in range(COLUMN_COUNT - WIN_COUNT + 1):
      for step in range(WIN_COUNT):
        if board[row][col + step] == piece:
          if step == WIN_COUNT - 1:
            return True
          else:
            continue
        else:
          break

  # Check vertical locations for win
  for row in range(ROW_COUNT - WIN_COUNT + 1):
    for col in range(COLUMN_COUNT):
      for step in range(WIN_COUNT):
        if board[row + step][col] == piece:
          if step == WIN_COUNT - 1:
            return True
          else:
            continue
        else:
          break

  # Check positively sloped diagonals
  for row in range(ROW_COUNT - WIN_COUNT + 1):
    for col in range(COLUMN_COUNT - WIN_COUNT + 1):
      for step in range(WIN_COUNT):
        if board[row + step][col + step] == piece:
          if step == WIN_COUNT - 1:
            return True
          else:
            continue
        else:
          break
          break

  # Check negatively sloped diagonals
  for row in range(WIN_COUNT - 1, ROW_COUNT):
    for col in range(COLUMN_COUNT - WIN_COUNT + 1):
      for step in range(WIN_COUNT):
        if board[row - step][col + step] == piece:
          if step == WIN_COUNT - 1:
            return True
          else:
            continue
        else:
          break
  
def play_game(player1, player2):
  board = create_board()
  game_over = False
  turn = 0

  print_score(player1)
  print_score(player2)

  while not game_over:
    print_board(board)

    # Player 1
    if turn == 0:
      col = player_move(board, player1)

      if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, 1)

        if winning_move(board, 1):
          print_board(board)
          print(f"{player1} Wins!!!")
          game_over = True
          update_scoreboard(scoreboard, player1)


    # Player 2
    else:
      col = col = player_move(board, player2)

      if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, 2)

        if winning_move(board, 2):
          print_board(board)
          print(f"{player2} Wins!!!")
          game_over = True
          update_scoreboard(scoreboard, player2)

    turn += 1
    # If turn is equal to '2', reset it to '0'
    turn = turn % 2

  if input("Would you like to play again? (y/n)") == "y":
    play_game(player1, player2)

print("Welcome to Connect 4!")
scoreboard = load_scoreboard()
player1 = process_player_name(1)
player2 = process_player_name(2)
play_game(player1, player2)
print("Thanks for playing!")