# Use NumPy to create and manipulate a matrix (to be used as the game board)
import numpy
# Use to convert Python dictionary to JSON and vice versa
import json
# Use to exit the application
import sys

import math
# Use to handle the GUI
import pygame
# Use to handle player text input
import keyboard

pygame.init()

# Game conditions
ROW_COUNT = 6
COLUMN_COUNT = 7
WIN_COUNT = 4

# App dimensions
CELLSIZE = 100
PIECE_RADIUS = int(CELLSIZE / 2 - 8)
TOP_MARGIN = 43
GAME_HEIGHT = (ROW_COUNT + 1) * CELLSIZE + TOP_MARGIN
GAME_WIDTH = COLUMN_COUNT * CELLSIZE
SIZE = (GAME_WIDTH, GAME_HEIGHT)

# RGB Values
BLACK = (30, 30, 30)
BLUE = (50, 50, 255)
GREY = (50, 50, 50)
RED = (255, 50, 50)
DARK_RED = (160, 40, 40)
YELLOW = (255, 215, 50)
DARK_YELLOW = (200, 140, 40)
WHITE = (235, 235, 235)

# Fonts
FONT_LEADERBOARD_TITLE = pygame.font.Font("cafeteria-black.ttf", 70)
FONT_LEADERBOARD1 = pygame.font.Font("cafeteria-black.ttf", 50)
FONT_LEADERBOARD2 = pygame.font.Font("cafeteria-black.ttf", 40)
FONT_LEADERBOARD3 = pygame.font.Font("cafeteria-black.ttf", 35)
FONT_MENU = pygame.font.Font("cafeteria-black.ttf", 50)
FONT_NAME_TITLE = pygame.font.Font("cafeteria-black.ttf", 60)
FONT_NAME1 = pygame.font.Font("cafeteria-black.ttf", 45)
FONT_SCORES = pygame.font.Font("cafeteria-black.ttf", 30)
FONT_TITLE1 = pygame.font.Font("cafeteria-black.ttf", 100)
FONT_TITLE2 = pygame.font.Font("cafeteria-black.ttf", 120)
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
        screen.fill(GREY),
        screen.blit(game_title1, (centre_element(game_title1), 120)),
        screen.blit(game_title2, (centre_element(game_title2), 210)),
        pygame.draw.circle(screen, RED, (120, 227), PIECE_RADIUS),
        pygame.draw.circle(screen, DARK_RED, (120, 227), PIECE_RADIUS - 5, 3),
        pygame.draw.circle(screen, YELLOW, (GAME_WIDTH - 120, 227),
                           PIECE_RADIUS),
        pygame.draw.circle(screen, DARK_YELLOW, (GAME_WIDTH - 120, 227),
                           PIECE_RADIUS - 5, 3)
    ])


# Displays title for name input pages
def display_name_input_title(player):
    if player == 1:
        name_input_title1 = FONT_NAME_TITLE.render("Player 1", True, RED)
    else:
        name_input_title1 = FONT_NAME_TITLE.render("Player 2", True, YELLOW)

    name_input_title2 = FONT_NAME_TITLE.render(" enter your name!", True,
                                               WHITE)

    # Used to establish total width of title1 and title2
    name_input_title = FONT_NAME_TITLE.render("Player 2 enter your name!",
                                              True, WHITE)

    indent = name_input_title1.get_rect().width

    pygame.display.update([
        screen.fill(GREY),
        screen.blit(name_input_title1,
                    (centre_element(name_input_title), 200)),
        screen.blit(name_input_title2,
                    (centre_element(name_input_title) + indent + 10, 200)),
    ])


# Edits the name, dependant on which key has been passed
def name_input(name, key, shifted):
    if key == "backspace":
        return name[0:-1]
    if key == "space":
        key = " "
    if shifted:
        key = key.upper()

    if len(name) < 12 and (len(key) == 1 or key == " "):
        name = name + key

    return name


# Displays the player name input page
def name_input_screen(player):
    scoreboard = load_scoreboard()
    show_name_input = True

    display_name_input_title(player)

    menu_button_text = FONT_SCORES.render("MENU", True, WHITE)
    menu_button = display_button(menu_button_text, 5)

    name = ''
    pygame.display.update([
        pygame.draw.rect(screen, BLACK, (150, 350, 400, 50)),
    ])

    while show_name_input:
        key = keyboard.read_key()

        if keyboard.is_pressed("shift"):
            shifted = True
        else:
            shifted = False

        for event in pygame.event.get():
            # Handle button hover effect and render hovering piece
            if event.type == pygame.MOUSEMOTION:
                if mouse_on_button(event.pos, menu_button.get_size(), 5):
                    menu_button_text = FONT_SCORES.render("MENU", True, BLUE)
                else:
                    menu_button_text = FONT_SCORES.render("MENU", True, WHITE)

                display_button(menu_button_text, 5)

            # Handle clicking of 'menu' button and player moves
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_on_button(event.pos, menu_button.get_size(), 5):
                    show_name_input = False
                    main_menu()

            # Handle all release key events
            if event.type == pygame.KEYUP:
                if key == "enter" and len(name) > 0:
                    if name not in scoreboard:
                        # Add new player to scoreboard
                        scoreboard[name] = {}
                        scoreboard[name]["Played"] = 0
                        scoreboard[name]["Won"] = 0
                        
                        update_scoreboard(scoreboard)

                    show_name_input = False
                    return name

                name = name_input(name, key, shifted)

        name_text = FONT_NAME1.render(name, True, WHITE)

        pygame.display.update([
            pygame.draw.rect(screen, BLACK, (150, 348, 400, 52)),
            screen.blit(name_text, (centre_element(name_text), 345)),
        ])


# Create a matrix of 0s, representing the board
def create_board():
    board = numpy.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# Display scores at top of screen
def display_scoreboard(player1, player2):
    scoreboard = load_scoreboard()

    red_score_text = FONT_SCORES.render(
        f"{player1}: {scoreboard[player1]['Won']} / {scoreboard[player1]['Played']}",
        True, RED)
    yellow_score_text = FONT_SCORES.render(
        f"{player2}: {scoreboard[player2]['Won']} / {scoreboard[player2]['Played']}",
        True, YELLOW)

    pygame.display.update([
        pygame.draw.rect(screen, GREY, (0, 0, GAME_WIDTH, TOP_MARGIN)),
        screen.blit(red_score_text, (20, 5)),
        screen.blit(yellow_score_text,
                    (GAME_WIDTH - yellow_score_text.get_rect().width - 20, 5))
    ])


# Checks if the cursor is within the bounds of a button
def mouse_on_button(mouse_position, button_size, posy):
    return (GAME_WIDTH / 2 - button_size[0] / 2 <= mouse_position[0] <=
            GAME_WIDTH / 2 + button_size[0] / 2
            and posy <= mouse_position[1] <= posy + button_size[1])


# Display empty connect 4 board
def display_board():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen, BLUE,
                (c * CELLSIZE,
                 (r + 1) * CELLSIZE + TOP_MARGIN, CELLSIZE, CELLSIZE))

            pygame.draw.circle(screen, GREY, (int(
                (c + 0.5) * CELLSIZE), int((r + 1.5) * CELLSIZE + TOP_MARGIN)),
                               PIECE_RADIUS)

    pygame.display.flip()


# Display a button with a background, returns button surface
def display_button(button_text, y):
    button_bg = pygame.Surface(button_text.get_size())
    button_bg.fill(GREY)

    pygame.display.update([
        screen.blit(button_bg, (centre_element(button_bg), y)),
        screen.blit(button_text, (centre_element(button_text), y)),
    ])

    return button_bg


# Clear space above board of previously rendered hover-pieces
def clear_top_banner():
    pygame.display.update(
        pygame.draw.rect(screen, GREY, (0, TOP_MARGIN, GAME_WIDTH, CELLSIZE)))


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
        pygame.draw.circle(screen, colour,
                           (posx, int(PIECE_RADIUS + 7 + TOP_MARGIN)),
                           PIECE_RADIUS),
        pygame.draw.circle(screen, rim,
                           (posx, int(PIECE_RADIUS + 7 + TOP_MARGIN)),
                           PIECE_RADIUS - 5, 3)
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

                pygame.draw.circle(screen, colour,
                                   (int((c + 0.5) * CELLSIZE),
                                    int((r + 1.5) * CELLSIZE + TOP_MARGIN)),
                                   PIECE_RADIUS)
                pygame.draw.circle(screen, rim,
                                   (int((c + 0.5) * CELLSIZE),
                                    int((r + 1.5) * CELLSIZE + TOP_MARGIN)),
                                   PIECE_RADIUS - 5, 3)

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

    pygame.display.update(
        screen.blit(winner_message,
                    (centre_element(winner_message), TOP_MARGIN)))


# Sorts the scoreboard by wins in descending order
def sort_scoreboard(scoreboard):
    sorted_tuples = sorted(
        scoreboard.items(),
        key=lambda item: item[1]['Won'] - item[1]['Played'] / 1000,
        reverse=True)
    sorted_scoreboard = {k: v for k, v in sorted_tuples}

    return sorted_scoreboard


# Updates and overwrites the scoreboard file
def update_scoreboard(scoreboard, winner=None, loser=None):
    if winner and loser:
        scoreboard[winner]["Won"] += 1
        scoreboard[winner]["Played"] += 1
        scoreboard[loser]["Played"] += 1

    scoreboard = sort_scoreboard(scoreboard)

    # Overwrite scoreboard file
    with open('scoreboard.json', 'w') as file:
        json.dump(scoreboard, file, ensure_ascii=False)

    return scoreboard


# Displays and plays the game
def play_game():
    player1 = name_input_screen(1)
    player2 = name_input_screen(2)

    board = create_board()
    scoreboard = load_scoreboard()
    game_over = False
    turn = 0

    screen.fill(GREY)
    pygame.display.flip()
    display_scoreboard(player1, player2)
    display_board()

    menu_button_text = FONT_SCORES.render("MENU", True, WHITE)
    menu_button = display_button(menu_button_text, 5)

    while not game_over:
        player_moved = False

        if turn == 0:
            player = 1
            player_name = player1
            other_player = player2
        else:
            player = 2
            player_name = player2
            other_player = player1

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
                        scoreboard = update_scoreboard(scoreboard, player_name,
                                                       other_player)
                        display_scoreboard(player1, player2)

        if player_moved:
            turn += 1
        # If turn is equal to '2', reset it to '0'
        turn = turn % 2

    pygame.time.wait(3000)
    main_menu()


# Display the title for the leaderboard page
def display_leaderboard_title():
    leaderboard_title = FONT_LEADERBOARD_TITLE.render("LEADERBOARD", True,
                                                      WHITE)

    pygame.display.update([
        screen.fill(GREY),
        screen.blit(leaderboard_title,
                    (centre_element(leaderboard_title), 57)),
        pygame.draw.circle(screen, RED, (95, 100), 30),
        pygame.draw.circle(screen, DARK_RED, (95, 100), 30 - 3, 2),
        pygame.draw.circle(screen, YELLOW, (GAME_WIDTH - 95, 100), 30),
        pygame.draw.circle(screen, DARK_YELLOW, (GAME_WIDTH - 95, 100), 30 - 3,
                           2)
    ])


def display_leaderboard_table():
    scoreboard = load_scoreboard()
    header1 = FONT_LEADERBOARD3.render("P", True, WHITE)
    header2 = FONT_LEADERBOARD3.render("W", True, WHITE)

    pygame.display.update([
        screen.blit(header1,
                    (GAME_WIDTH - header1.get_size()[0] / 2 - 228, 160)),
        screen.blit(header2,
                    (GAME_WIDTH - header2.get_size()[0] / 2 - 165, 160)),
    ])

    leaderboard_count = 7 if len(scoreboard.keys()) > 7 else len(
        scoreboard.keys())
    for i in range(leaderboard_count):
        top_margin = 195 + (i + 1) * 65
        player = list(scoreboard.keys())[i]
        name = FONT_LEADERBOARD2.render(player, True, WHITE)
        played = FONT_LEADERBOARD3.render(f"{scoreboard[player]['Played']}",
                                          True, WHITE)
        won = FONT_LEADERBOARD1.render(f"{scoreboard[player]['Won']}", True,
                                       WHITE)

        if i % 4 == 0:
            pygame.display.update([
                pygame.draw.circle(screen, RED, (80, top_margin - 20), 14),
                pygame.draw.circle(screen, DARK_RED, (80, top_margin - 20), 12,
                                   1),
                pygame.draw.circle(screen, RED,
                                   (GAME_WIDTH - 80, top_margin - 20), 14),
                pygame.draw.circle(screen, DARK_RED,
                                   (GAME_WIDTH - 80, top_margin - 20), 12, 1),
            ])
        if i % 4 == 2:
            pygame.display.update([
                pygame.draw.circle(screen, YELLOW, (80, top_margin - 20), 14),
                pygame.draw.circle(screen, DARK_YELLOW, (80, top_margin - 20),
                                   12, 1),
                pygame.draw.circle(screen, YELLOW,
                                   (GAME_WIDTH - 80, top_margin - 20), 14),
                pygame.draw.circle(screen, DARK_YELLOW,
                                   (GAME_WIDTH - 80, top_margin - 20), 12, 1),
            ])

        pygame.display.update([
            screen.blit(name, (140, top_margin - name.get_size()[1])),
            screen.blit(played, (GAME_WIDTH - played.get_size()[0] / 2 - 225,
                                 top_margin - played.get_size()[1])),
            screen.blit(won, (GAME_WIDTH - won.get_size()[0] / 2 - 165,
                              top_margin - won.get_size()[1] + 4)),
        ])


# Displays the leaderboard
def leaderboard():
    show_leaderboard = True

    screen.fill(GREY)
    pygame.display.flip()
    display_leaderboard_title()
    display_leaderboard_table()

    menu_button_text = FONT_SCORES.render("MENU", True, WHITE)
    menu_button = display_button(menu_button_text, 5)

    while show_leaderboard:
        for event in pygame.event.get():
            # Handle button hover effect and render hovering piece
            if event.type == pygame.MOUSEMOTION:
                if mouse_on_button(event.pos, menu_button.get_size(), 5):
                    menu_button_text = FONT_SCORES.render("MENU", True, BLUE)
                else:
                    menu_button_text = FONT_SCORES.render("MENU", True, WHITE)

                display_button(menu_button_text, 5)

            # Handle clicking of 'menu' button and player moves
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_on_button(event.pos, menu_button.get_size(), 5):
                    show_leaderboard = False
                    main_menu()


# Displays the main menu
def main_menu():
    show_menu = True

    display_menu_title()

    play_button_text = FONT_MENU.render("Play Game", True, WHITE)
    play_button_y = 400
    play_button = display_button(play_button_text, play_button_y)

    leaderboard_button_text = FONT_MENU.render("Leaderboard", True, WHITE)
    leaderboard_button_y = 470
    leaderboard_button = display_button(leaderboard_button_text,
                                        leaderboard_button_y)

    quit_button_text = FONT_MENU.render("Quit Game", True, WHITE)
    quit_button_y = 540
    quit_button = display_button(quit_button_text, quit_button_y)

    while show_menu:
        play_button.fill(GREY)
        leaderboard_button.fill(GREY)
        quit_button.fill(GREY)

        events = pygame.event.get()

        for event in events:
            # Handle button hover effect
            if event.type == pygame.MOUSEMOTION:
                if mouse_on_button(event.pos, play_button.get_size(),
                                   play_button_y):
                    play_button_text = FONT_MENU.render(
                        "Play Game", True, BLUE)
                else:
                    play_button_text = FONT_MENU.render(
                        "Play Game", True, WHITE)

                if mouse_on_button(event.pos, leaderboard_button.get_size(),
                                   leaderboard_button_y):
                    leaderboard_button_text = FONT_MENU.render(
                        "Leaderboard", True, BLUE)
                else:
                    leaderboard_button_text = FONT_MENU.render(
                        "Leaderboard", True, WHITE)

                if mouse_on_button(event.pos, quit_button.get_size(),
                                   quit_button_y):
                    quit_button_text = FONT_MENU.render(
                        "Quit Game", True, BLUE)
                else:
                    quit_button_text = FONT_MENU.render(
                        "Quit Game", True, WHITE)

            # Handle clicking of menu options
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_on_button(event.pos, play_button.get_size(),
                                   play_button_y):
                    show_menu = False
                    play_game()

                elif mouse_on_button(event.pos, leaderboard_button.get_size(),
                                     leaderboard_button_y):
                    show_menu = False
                    leaderboard()

                elif mouse_on_button(event.pos, quit_button.get_size(),
                                     quit_button_y):
                    sys.exit()

            display_button(play_button_text, play_button_y)
            display_button(leaderboard_button_text, leaderboard_button_y)
            display_button(quit_button_text, quit_button_y)


screen = pygame.display.set_mode(SIZE)
main_menu()
