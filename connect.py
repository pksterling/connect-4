# Use NumPy to create and manipulate a matrix (to be used as the game board)
import numpy
# Use to convert Python dictionary to JSON and vice versa
import json
import sys
import math
import pygame
pygame.init()

# Game conditions
ROW_COUNT = 6
COLUMN_COUNT = 7
WIN_COUNT = 4

# App dimensions
CELLSIZE = 100
PIECE_RADIUS = int(CELLSIZE / 2 - 8)
TOP_MARGIN = 43
GAME_WIDTH = COLUMN_COUNT * CELLSIZE
GAME_HEIGHT = (ROW_COUNT + 1) * CELLSIZE + TOP_MARGIN
SIZE = (GAME_WIDTH, GAME_HEIGHT)

# RGB Values
BLACK = (50, 50, 50)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
DARK_RED = (160, 40, 40)
YELLOW = (255, 215, 50)
DARK_YELLOW = (200, 140, 40)
WHITE = (235, 235, 235)

# Fonts
FONT_TITLE1 = pygame.font.Font("cafeteria-black.ttf", 100)
FONT_TITLE2 = pygame.font.Font("cafeteria-black.ttf", 120)
FONT_MENU = pygame.font.Font("cafeteria-black.ttf", 50)
FONT_SCORES = pygame.font.Font("cafeteria-black.ttf", 30)
FONT_WINNER = pygame.font.Font("cafeteria-black.ttf", 80)


# Create scoreboard variable for amending and overwriting
def load_scoreboard():
    try:
        with open('scoreboard.json') as json_file:
            scoreboard = json.load(json_file)
    except FileNotFoundError:
        scoreboard = {}

    return scoreboard


# Display the main menu title
def display_menu_title():
    game_title1 = FONT_TITLE1.render("CONNECT", True, WHITE)
    game_title2 = FONT_TITLE2.render("FOUR", True, WHITE)

    pygame.display.update([
        screen.fill(BLACK),
        screen.blit(game_title1, (centre_element(game_title1), 120)),
        screen.blit(game_title2, (centre_element(game_title2), 210)),
        pygame.draw.circle(screen, RED, (120, 227), PIECE_RADIUS),
        pygame.draw.circle(screen, DARK_RED, (120, 227), PIECE_RADIUS - 5, 3),
        pygame.draw.circle(
            screen, YELLOW, (GAME_WIDTH - 120, 227), PIECE_RADIUS),
        pygame.draw.circle(screen, DARK_YELLOW,
                           (GAME_WIDTH - 120, 227), PIECE_RADIUS - 5, 3)
    ])


# Display scores at top of screen
def display_scoreboard():
    red_score_text = FONT_SCORES.render(f"Red: {scoreboard['Red']}", True, RED)
    yellow_score_text = FONT_SCORES.render(
        f"Yellow: {scoreboard['Yellow']}", True, YELLOW)

    pygame.display.update([
        pygame.draw.rect(screen, BLACK, (0, 0, GAME_WIDTH, TOP_MARGIN)),
        screen.blit(red_score_text, (20, 5)),
        screen.blit(yellow_score_text, (GAME_WIDTH -
                    yellow_score_text.get_rect().width - 20, 5))
    ])


# Create a matrix of 0s, representing the board
def create_board():
    board = numpy.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# Checks if the cursor is within the bounds of a button
def mouse_on_button(mouse_position, button_size, posy):
    return (
        GAME_WIDTH / 2 - button_size[0] / 2 <= mouse_position[0] <= GAME_WIDTH / 2 +
        button_size[0] /
        2 and posy <= mouse_position[1] <= posy + button_size[1]
    )

# Display empty connect 4 board


def display_board():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * CELLSIZE, (r + 1) * CELLSIZE + TOP_MARGIN, CELLSIZE, CELLSIZE)
            )

            pygame.draw.circle(screen, BLACK, (int(
                (c + 0.5) * CELLSIZE), int((r + 1.5) * CELLSIZE + TOP_MARGIN)), PIECE_RADIUS)

    pygame.display.flip()


# Display a button with a background, returns button surface
def display_button(button_text, y):
    button_bg = pygame.Surface(button_text.get_size())
    button_bg.fill(BLACK)

    pygame.display.update([
        screen.blit(button_bg, (centre_element(button_bg), y)),
        screen.blit(button_text, (centre_element(button_text), y)),
    ])

    return button_bg


# Clear space above board of previously rendered hover-pieces
def clear_top_banner():
    pygame.display.update(
        pygame.draw.rect(screen, BLACK, (0, TOP_MARGIN, GAME_WIDTH, CELLSIZE))
    )

# Display game piece that follows the cursor's X position above the game board
def render_hover_piece(posx, turn):
    if turn == 0:
        colour = RED
        rim = DARK_RED
    elif turn == 1:
        colour = YELLOW
        rim = DARK_YELLOW

    marginx = int(CELLSIZE / 2)

    if posx < marginx:
        posx = marginx
    elif posx > GAME_WIDTH - marginx:
        posx = GAME_WIDTH - marginx

    clear_top_banner()
    pygame.display.update([
        pygame.draw.circle(screen, colour, (posx, int(
            PIECE_RADIUS + 7 + TOP_MARGIN)), PIECE_RADIUS),
        pygame.draw.circle(screen, rim, (posx, int(
            PIECE_RADIUS + 7 + TOP_MARGIN)), PIECE_RADIUS - 5, 3)
    ])


# Check if the top row of a column is used
def column_is_full(board, col):
    return board[ROW_COUNT - 1][col] != 0


# Check each row of a column, returning the first empty location
def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row


# Change the relevant board location, from '0' to '1'/'2'
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# Check if each cell is taken and display a game piece if so
def draw_pieces(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            cell = int(board[ROW_COUNT - 1 - r][c])

            if cell > 0:
                if cell == 1:
                    colour = RED
                    rim = DARK_RED
                elif cell == 2:
                    colour = YELLOW
                    rim = DARK_YELLOW

                pygame.draw.circle(screen, colour, (int(
                    (c + 0.5) * CELLSIZE),  int((r + 1.5) * CELLSIZE + TOP_MARGIN)), PIECE_RADIUS)
                pygame.draw.circle(screen, rim, (int(
                    (c + 0.5) * CELLSIZE),  int((r + 1.5) * CELLSIZE + TOP_MARGIN)), PIECE_RADIUS - 5, 3)

    pygame.display.update()


# If passed a valid move, will adjust the board and update the display
def player_move(board, player, posx):
    col = int(math.floor(posx / CELLSIZE))

    if column_is_full(board, col):
        return False
    else:
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player)
        draw_pieces(board)
        return True


# Checks one player's pieces for a line of length 'WIN_COUNT'
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


# Returns X dimension required for centring
def centre_element(text):
    return GAME_WIDTH / 2 - text.get_rect().width / 2


# Displays congratulations message above the game board
def display_winner(player_name):
    winner_message = FONT_WINNER.render(f"{player_name} Wins!!!", True, WHITE)

    pygame.display.update(screen.blit(
        winner_message, (centre_element(winner_message), TOP_MARGIN)))


# Adds ome point to the winner's score and overwrites the scoreboard file
def update_scoreboard(scoreboard, winner):
    scoreboard[winner] += 1

    # Overwrite scoreboard file
    with open('scoreboard.json', 'w') as file:
        json.dump(scoreboard, file, ensure_ascii=False)


# Displays the main menu
def main_menu():
    show_menu = True

    display_menu_title()
    display_scoreboard()

    play_button_text = FONT_MENU.render("Play Game", True, WHITE)
    quit_button_text = FONT_MENU.render("Quit Game", True, WHITE)
    play_button = display_button(play_button_text, 400)
    quit_button = display_button(quit_button_text, 470)

    while show_menu:
        play_button.fill(BLACK)
        quit_button.fill(BLACK)

        for event in pygame.event.get():
            # Handle button hover effect
            if event.type == pygame.MOUSEMOTION:
                if mouse_on_button(event.pos, play_button.get_size(), 400):
                    play_button_text = FONT_MENU.render(
                        "Play Game", True, BLUE)
                else:
                    play_button_text = FONT_MENU.render(
                        "Play Game", True, WHITE)

                if mouse_on_button(event.pos, quit_button.get_size(), 470):
                    quit_button_text = FONT_MENU.render(
                        "Quit Game", True, BLUE)
                else:
                    quit_button_text = FONT_MENU.render(
                        "Quit Game", True, WHITE)

            # Handle clicking of menu options
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_on_button(event.pos, play_button.get_size(), 400):
                    show_menu = False
                    play_game()

                elif mouse_on_button(event.pos, quit_button.get_size(), 470):
                    sys.exit()

            display_button(play_button_text, 400)
            display_button(quit_button_text, 470)


# Displays and plays the game
def play_game():
    board = create_board()
    game_over = False
    turn = 0

    screen.fill(BLACK)
    pygame.display.flip()
    display_scoreboard()
    display_board()

    menu_button_text = FONT_SCORES.render("MENU", True, WHITE)
    menu_button = display_button(menu_button_text, 5)

    while not game_over:
        player_moved = False

        if turn == 0:
            player = 1
            player_name = "Red"
        else:
            player = 2
            player_name = "Yellow"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Handle button hover effect and render hovering piece
            if event.type == pygame.MOUSEMOTION:
                if mouse_on_button(event.pos, menu_button.get_size(), 5):
                    menu_button_text = FONT_SCORES.render("MENU", True, BLUE)
                else:
                    menu_button_text = FONT_SCORES.render("MENU", True, WHITE)

                display_button(menu_button_text, 5)
                render_hover_piece(event.pos[0], turn)

            # Handle clicking of 'menu' button and player moves
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_on_button(event.pos, menu_button.get_size(), 5):
                    main_menu()
                else:
                    player_moved = player_move(board, player, event.pos[0])
                    clear_top_banner()

                    if winning_move(board, player):
                        game_over = True
                        display_winner(player_name)
                        update_scoreboard(scoreboard, player_name)
                        display_scoreboard()

        if player_moved:
            turn += 1
        # If turn is equal to '2', reset it to '0'
        turn = turn % 2

    pygame.time.wait(3000)
    main_menu()


screen = pygame.display.set_mode(SIZE)
scoreboard = load_scoreboard()
main_menu()
