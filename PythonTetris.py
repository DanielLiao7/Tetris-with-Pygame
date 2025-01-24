# -------------------------
#   Daniel Liao, 2023
# -------------------------

import pygame
import random

# I decided to make my constants global to save from having to put them as parameters in every function
# Piece Coords based on imaginary grid with top left being (0, 0) and bottom right being (3, 3)
# Each sublist of points represents a different rotation
# Source: https://static.wikia.nocookie.net/tetrisconcept/images/3/3d/SRS-pieces.png/revision/latest/scale-to-width-down/336?cb=20060626173148
PIECES = [
    # Line
    [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(1, 0), (1, 1), (1, 2), (1, 3)]
    ],
    # Square
    [
        [(0, 0), (1, 0), (0, 1), (1, 1)]
    ],
    # T
    [
        [(0, 1), (1, 1), (2, 1), (1, 0)],
        [(1, 2), (1, 1), (1, 0), (2, 1)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 2), (1, 1), (1, 0), (0, 1)]
    ],
    # J
    [
        [(0, 1), (1, 1), (2, 1), (0, 0)],
        [(1, 2), (1, 1), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 2), (1, 1), (1, 0), (0, 2)]
    ],
    # L
    [
        [(0, 1), (1, 1), (2, 1), (2, 0)],
        [(1, 2), (1, 1), (1, 0), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(1, 2), (1, 1), (1, 0), (0, 0)]
    ],
    # S
    [
        [(0, 1), (1, 1), (1, 0), (2, 0)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(0, 2), (1, 2), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)]
    ],
    # Z
    [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 2), (1, 1), (2, 1), (2, 0)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(0, 2), (0, 1), (1, 1), (1, 0)]
    ]
]

COLORS = [
    # cyan, yellow, magenta, blue, orange, green, red, black(7 will always represent an empty space)
    [(0, 255, 255), (255, 255, 0), (255, 0, 255), (0, 0, 255), (255, 127, 0), (0, 255, 0), (255, 0, 0), (0, 0, 0)],
    # Dark mode
    [(0, 220, 220), (220, 220, 0), (220, 0, 220), (0, 0, 220), (220, 110, 0), (0, 220, 0), (220, 0, 0), (0, 0, 0)],
    # borderless theme (colors desaturated)
    [(0, 240, 240), (240, 240, 0), (240, 0, 240), (0, 0, 240), (240, 120, 0), (0, 240, 0), (240, 0, 0), (0, 0, 0)],
    # Grayscale
    [(170, 170, 170), (190, 190, 190), (100, 100, 100), (60, 60, 60), (150, 150, 150), (130, 130, 130), (80, 80, 80), (0, 0, 0)],
    # Christmas
    [(144, 196, 139), (222, 150, 129), (77, 48, 41), (35, 61, 36), (171, 63, 53), (79, 122, 70), (204, 96, 96), (247, 190, 186)],
    # Idk what this is
    [(247, 77, 77), (247, 108, 77), (247, 122, 77), (247, 134, 77), (247, 148, 77), (247, 162, 77), (247, 185, 77), (171, 225, 235)],
    # Terminal
    [(230, 230, 230), (230, 230, 230), (230, 230, 230), (230, 230, 230), (230, 230, 230), (230, 230, 230), (230, 230, 230), (0, 0, 0)]
]

# background color, indicator color, big border color, UI box colors, small border color, text color, grid outline color
# Uses dictionaries, so I don't have to remember the index for each one
UI_COLORS = [
    # Default:
    {"background": (255, 255, 255), "indicator": (255, 255, 255), "big_border": (200, 200, 200),
     "UI_box": (250, 250, 250), "small_borders": (20, 20, 20), "text": (20, 20, 20), "grid_outline": (255, 255, 255)},
    # Dark mode
    {"background": (20, 20, 20), "indicator": (220, 220, 220), "big_border": (160, 160, 160),
     "UI_box": (20, 20, 20), "small_borders": (220, 220, 220), "text": (220, 220, 220), "grid_outline": (220, 220, 220)},
    # Borderless
    {"background": (255, 255, 255), "indicator": (255, 255, 255), "big_border": (200, 200, 200),
     "UI_box": (250, 250, 250), "small_borders": (40, 40, 40), "text": (20, 20, 20), "grid_outline": (255, 255, 255)},
    # Grayscale
    {"background": (20, 20, 20), "indicator": (230, 230, 230), "big_border": (200, 200, 200),
     "UI_box": (230, 230, 230), "small_borders": (20, 20, 20), "text": (230, 230, 230), "grid_outline": (230, 230, 230)},
    # Christmas
    {"background": (242, 141, 133), "indicator": (255, 255, 255), "big_border": (150, 66, 60),
     "UI_box": (191, 247, 186), "small_borders": (49, 79, 46), "text": (34, 56, 32), "grid_outline": (255, 255, 255)},
    # Idk what this is
    {"background": (59, 106, 150), "indicator": (255, 255, 255), "big_border": (191, 209, 219),
     "UI_box": (202, 235, 252), "small_borders": (191, 209, 219), "text": (255, 255, 255), "grid_outline": (255, 255, 255)},
    # Terminal
    {"background": (0, 0, 0), "indicator": (100, 100, 100), "big_border": (230, 230, 230),
     "UI_box": (0, 0, 0), "small_borders": (230, 230, 230), "text": (230, 230, 230), "grid_outline": (0, 0, 0)}
    ]

GRID_WIDTH, GRID_HEIGHT = (10, 24)

START_POS = (3, 0)

UPDATE_CAP = 165


# Also referenced this for rendering: https://www.geeksforgeeks.org/pygame-drawing-objects-and-shapes/
def render(pg, surface, grid, piece, rotation, pieceX, pieceY, heldPiece, nextPieces, texts, theme):
    cellSize = 20
    borderWidth = 1
    # For borderless theme:
    if theme == 2:
        borderWidth = 0

    surface.fill(UI_COLORS[theme]["background"])

    gridLeftMargin = 7

    # Draws a rectangle the size of the grid so that the cell borders have a unique color
    pg.draw.rect(surface, UI_COLORS[theme]["grid_outline"], [gridLeftMargin * cellSize, 0, GRID_WIDTH * cellSize,
                                                             GRID_HEIGHT * cellSize])

    # Draws each square of the grid with its corresponding color
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            pg.draw.rect(surface, COLORS[theme][grid[y][x]], [(gridLeftMargin + x) * cellSize, y * cellSize,
                                                              cellSize-borderWidth, cellSize-borderWidth])

    # Draws an indicator for where the piece will land
    for y in range(pieceY, GRID_HEIGHT):
        if collision("down", grid, piece, pieceX, y, rotation):
            for point in PIECES[piece][rotation]:
                pg.draw.rect(surface, UI_COLORS[theme]["indicator"], [(gridLeftMargin + pieceX + point[0]) * cellSize,
                                                                      (y + point[1]) * cellSize, cellSize-borderWidth,
                                                                      cellSize-borderWidth])
            break

    # Draws the piece currently in play
    for point in PIECES[piece][rotation]:
        pg.draw.rect(surface, COLORS[theme][piece], [(gridLeftMargin + pieceX + point[0]) * cellSize,
                                                     (pieceY + point[1]) * cellSize, cellSize-borderWidth,
                                                     cellSize-borderWidth])

    # Draws the border for the grid
    pg.draw.rect(surface, UI_COLORS[theme]["big_border"], [gridLeftMargin * cellSize, 0, GRID_WIDTH * cellSize,
                                                           GRID_HEIGHT * cellSize], 3)

    # Draws UI for held piece and next pieces:
    # Referenced: https://www.geeksforgeeks.org/how-to-draw-a-rectangle-with-rounded-corner-in-pygame/
    UIBoxWidth = 5
    heldLeftMargin = 1
    nextLeftMargin = 18
    UITopMargin = 2

    # first one draws the background for the box, the second one draws the border
    pg.draw.rect(surface, UI_COLORS[theme]["UI_box"], [heldLeftMargin * cellSize, UITopMargin * cellSize,
                                                       UIBoxWidth * cellSize, UIBoxWidth * cellSize], 0, 3)
    pg.draw.rect(surface, UI_COLORS[theme]["small_borders"], [heldLeftMargin * cellSize, UITopMargin * cellSize,
                                                              UIBoxWidth * cellSize, UIBoxWidth * cellSize], 2, 3)

    pg.draw.rect(surface, UI_COLORS[theme]["UI_box"], [nextLeftMargin * cellSize, UITopMargin * cellSize,
                                                       UIBoxWidth * cellSize, 13 * cellSize], 0, 3)
    pg.draw.rect(surface, UI_COLORS[theme]["small_borders"], [nextLeftMargin * cellSize, UITopMargin * cellSize,
                                                              UIBoxWidth * cellSize, 13 * cellSize], 2, 3)

    # Draws the text
    for text in texts:
        surface.blit(text[0], text[1])

    # Draws the held piece
    if heldPiece != -1:
        # Gets the length & height of the piece by finding the points that are furthest out vertically and horizontally
        # Source: https://www.geeksforgeeks.org/python-min-and-max-value-in-list-of-tuples/
        maxLength = max(PIECES[heldPiece][0])[0] + 1
        maxHeight = max(PIECES[heldPiece][0])[1] + 1

        for point in PIECES[heldPiece][0]:
            # Offsets the position, so it doesn't draw on the board
            pg.draw.rect(surface, COLORS[theme][heldPiece], [(heldLeftMargin + ((UIBoxWidth - maxLength)/2) + point[0]) * cellSize,
                                                             (3.5 + ((UITopMargin - maxHeight)/2) + point[1]) * cellSize,
                                                             cellSize - borderWidth, cellSize - borderWidth])

    # Draws the next pieces to be played
    for i in range(len(nextPieces)):
        maxLength = max(PIECES[nextPieces[i]][0])[0] + 1

        for point in PIECES[nextPieces[i]][0]:
            pg.draw.rect(surface, COLORS[theme][nextPieces[i]],
                         [(nextLeftMargin + ((UIBoxWidth - maxLength)/2) + point[0]) * cellSize,
                          ((UITopMargin - 2.5) + (4*(i+1)) + point[1]) * cellSize, cellSize - borderWidth,
                          cellSize - borderWidth])

    pg.display.flip()


# Checks if the piece will collide with the walls or with pieces in the grid on the next move
def collision(direction, grid, piece, pieceX, pieceY, testRotation):
    for point in PIECES[piece][testRotation]:
        if direction == "left":
            if pieceX + point[0] - 1 < 0:
                return True
            if grid[pieceY + point[1]][pieceX + point[0] - 1] != 7:  # 7 represents the index for an empty space
                return True
        if direction == "right":
            if pieceX + point[0] + 1 >= GRID_WIDTH:
                return True
            if grid[pieceY + point[1]][pieceX + point[0] + 1] != 7:
                return True
        if direction == "down":
            if pieceY + point[1] + 1 >= GRID_HEIGHT:
                return True
            if grid[pieceY + point[1] + 1][pieceX + point[0]] != 7:
                return True
        if direction == "rotate":
            if pieceY + point[1] >= GRID_HEIGHT:
                return True
            if pieceX + point[0] >= GRID_WIDTH:
                return True
            if pieceX + point[0] < 0:
                return True
            if grid[pieceY + point[1]][pieceX + point[0]] != 7:
                return True

    return False


# Checks for any rows that are completed and returns the total amount
def checkRows(grid):
    count = 0
    numRows = 0
    for row in range(len(grid)):
        for value in grid[row]:
            if value != 7:  # 7 represents the index for an empty space
                count += 1

        if count == GRID_WIDTH:
            clearRow(grid, row)
            numRows += 1

        count = 0

    return numRows


# Clears the given row
def clearRow(grid, row):
    # Sets each row to a clone of the row above, starting from the row that needs to be cleared
    for y in range(row, 0, -1):
        grid[y] = grid[y-1][:]


# Returns the amount that the score should increase by for line clearing
def calcScoreAddition(numLines, level):
    if numLines == 1:
        return 100*level
    if numLines == 2:
        return 300*level
    if numLines == 3:
        return 500*level
    if numLines == 4:
        return 800*level

    return 0


def main():
    running = True
    gameOver = False
    paused = False

    clock = pygame.time.Clock()
    pygame.init()

    screenWidth = 485
    screenHeight = 530

    theme = 0  # Index for which sublist(theme) in COLORS to use
    # Dictionary to make changing theme logic more concise
    numberKeysToTheme = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3, pygame.K_5: 4, pygame.K_6: 5,
                         pygame.K_7: 6}

    # Source for pygame surface and rectangle drawing: https://www.geeksforgeeks.org/how-to-draw-rectangle-in-pygame/
    surface = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Tetris")  # https://www.geeksforgeeks.org/how-to-change-the-name-of-a-pygame-window/

    # Reference: https://www.geeksforgeeks.org/python-display-text-to-pygame-window/#
    # Text creation put here, so they aren't redefined every frame(although some have to be)
    font = pygame.font.SysFont('calibri', 16)

    heldText = font.render("Held Piece:", False, UI_COLORS[theme]["text"])
    heldTextRect = heldText.get_rect()
    heldTextRect.topleft = (20, 20)

    nextText = font.render("Next Pieces:", False, UI_COLORS[theme]["text"])
    nextTextRect = nextText.get_rect()
    nextTextRect.topleft = (18 * 20, 20)

    scoreText = font.render("Score:", False, UI_COLORS[theme]["text"])
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.topleft = (20, 8 * 20)

    linesText = font.render("Lines:", False, UI_COLORS[theme]["text"])
    linesTextRect = linesText.get_rect()
    linesTextRect.topleft = (20, 9 * 20)

    levelText = font.render("Level:", False, UI_COLORS[theme]["text"])
    levelTextRect = levelText.get_rect()
    levelTextRect.topleft = (20, 10 * 20)

    texts = [[heldText, heldTextRect], [nextText, nextTextRect], [scoreText, scoreTextRect], [linesText, linesTextRect],
             [levelText, levelTextRect]]

    # Creates a 2d list of 7's which represents the index for an empty space in COLORS
    # Source: https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/
    grid = [[7 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

    piece = random.randrange(len(PIECES))
    pieceX, pieceY = START_POS
    rotation = 0

    nextPieces = [random.randrange(len(PIECES)), random.randrange(len(PIECES)), random.randrange(len(PIECES))]

    heldPiece = -1
    hasHeld = False

    holdTime = 0
    holdCount = 0
    holdingKey = False

    passedTime = 0

    # Scoring system based on https://tetris.wiki/Scoring
    # 10 lines cleared for each level increase
    score = 0
    linesCleared = 0

    # Official tetris gravity curve from: https://harddrop.com/wiki/Tetris_Worlds
    startingLevel = 1
    level = startingLevel
    fallSpeed = ((0.8-((level-1)*0.007))**(level-1)) * 1000  # Time in milis for how long until piece moves down 1 space

    while running:

        clock.tick(UPDATE_CAP)

        # ----------------------------------------ONE-TIME INPUT HANDLING-------------------------------------------
        for event in pygame.event.get():
            # Allows you to exit the game
            if event.type == pygame.QUIT:
                running = False

            if not gameOver:
                # Rotating, Holding, and Hard-dropping implmented here because the keys aren't meant to be held
                # Used this source for reference: https://www.geeksforgeeks.org/how-to-get-keyboard-input-in-pygame/
                if event.type == pygame.KEYDOWN:
                    if not paused:
                        if event.key == pygame.K_UP:
                            if not rotation == len(PIECES[piece]) - 1:
                                if not collision("rotate", grid, piece, pieceX, pieceY, rotation + 1):
                                    rotation += 1
                            else:
                                if not collision("rotate", grid, piece, pieceX, pieceY, 0):
                                    rotation = 0
                        if event.key == pygame.K_c:
                            if not hasHeld:
                                hasHeld = True
                                temp = piece
                                if heldPiece == -1:
                                    piece = nextPieces.pop(0)
                                    nextPieces.append(random.randrange(len(PIECES)))
                                else:
                                    piece = heldPiece
                                heldPiece = temp
                                pieceX, pieceY = START_POS
                                rotation = 0
                        if event.key == pygame.K_SPACE:
                            count = 0  # count how many lines for scoring
                            for y in range(pieceY, GRID_HEIGHT):
                                if collision("down", grid, piece, pieceX, y, rotation):
                                    # Check for Gameover:
                                    if count == 0 and pieceX == START_POS[0] and pieceY == START_POS[1]:
                                        gameOver = True

                                    # Adds the piece to the grid and then starts with a new piece
                                    for point in PIECES[piece][rotation]:
                                        grid[y + point[1]][pieceX + point[0]] = piece
                                    pieceX, pieceY = START_POS
                                    rotation = 0
                                    piece = nextPieces.pop(0)
                                    nextPieces.append(random.randrange(len(PIECES)))
                                    numLines = checkRows(grid)
                                    linesCleared += numLines
                                    score += calcScoreAddition(numLines, level)
                                    score += 2*count
                                    hasHeld = False  # Player should be able to hold again when the piece touches the bottom
                                    break  # https://www.programiz.com/python-programming/break-continue
                                count += 1
                        # More concise format for changing theme based on number pressed
                        # https://stackoverflow.com/questions/18774499/multiple-possibilities-for-a-single-variable-if-statements-in-python
                        if event.key in numberKeysToTheme:
                            theme = numberKeysToTheme[event.key]
                            # Update these texts so they have the right color
                            heldText = font.render("Held Piece:", False, UI_COLORS[theme]["text"])
                            nextText = font.render("Next Pieces:", False, UI_COLORS[theme]["text"])
                            texts[0][0] = heldText
                            texts[1][0] = nextText
                    # Allows you to pause and unpause the game
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused

        if not gameOver:
            if not paused:
                # ----------------------------------------CONTINUOUS INPUT HANDLING------------------------------------
                # Info about keyboard input for when keys are held from:
                # https://stackoverflow.com/questions/16044229/how-to-get-keyboard-input-in-pygame
                keys = pygame.key.get_pressed()
                # Check when not holding a movement key
                if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN]):
                    holdingKey = False
                    holdCount = 0
                    holdTime = 400  # First press should be instant so holdTime is set to greater than the hold duration
                else:
                    holdingKey = True
                    holdTime += clock.get_time()

                # In Tetris the first 2 moves when holding a key usually have a delay to make precise movement easier
                # This holding system is implmemented to replicate that
                # Numbers obtained through trial and error
                holdDuration = 220
                if holdCount > 1:
                    holdDuration = 30

                if holdTime >= holdDuration and holdingKey:
                    holdTime = 0
                    holdCount += 1

                    if keys[pygame.K_LEFT]:
                        if not collision("left", grid, piece, pieceX, pieceY, rotation):
                            pieceX -= 1
                    if keys[pygame.K_RIGHT]:
                        if not collision("right", grid, piece, pieceX, pieceY, rotation):
                            pieceX += 1
                    if keys[pygame.K_DOWN]:
                        if not collision("down", grid, piece, pieceX, pieceY, rotation):
                            pieceY += 1
                            score += 1
                        else:
                            # Check for Gameover:
                            if pieceX == START_POS[0] and pieceY == START_POS[1]:
                                gameOver = True
                            # Once the piece touches the bottom, start with a new piece & add the old piece to the grid
                            for point in PIECES[piece][rotation]:
                                grid[pieceY + point[1]][pieceX + point[0]] = piece
                            pieceX, pieceY = START_POS
                            rotation = 0
                            piece = nextPieces.pop(0)
                            nextPieces.append(random.randrange(len(PIECES)))
                            numLines = checkRows(grid)
                            linesCleared += numLines
                            score += calcScoreAddition(numLines, level)
                            hasHeld = False

                # ----------------------------------------PIECE FALLING LOGIC------------------------------------------
                # Researched some info about pygame's time system: https://www.geeksforgeeks.org/pygame-time/
                passedTime += clock.get_time()
                # Moves the piece down by 1 after a certain amount of time
                if passedTime >= fallSpeed:
                    passedTime = 0
                    if not collision("down", grid, piece, pieceX, pieceY, rotation):
                        pieceY += 1
                    else:
                        # Check for Gameover:
                        if pieceX == START_POS[0] and pieceY == START_POS[1]:
                            gameOver = True
                        # Once the piece touches the bottom, start with a new piece & add the old piece to the grid
                        for point in PIECES[piece][rotation]:
                            grid[pieceY + point[1]][pieceX + point[0]] = piece
                        pieceX, pieceY = START_POS
                        rotation = 0
                        piece = nextPieces.pop(0)
                        nextPieces.append(random.randrange(len(PIECES)))
                        numLines = checkRows(grid)
                        linesCleared += numLines
                        score += calcScoreAddition(numLines, level)
                        hasHeld = False

                # ------------------------------------LEVEL UPDATING & RENDER STUFF------------------------------------
                # Level increases for every 10 times the starting level of lines cleared
                level = (linesCleared // (10*startingLevel)) + startingLevel
                # level capped at 20 because realistically no one should be able to get past it
                if level > 20:
                    level = 20
                fallSpeed = ((0.8 - ((level - 1) * 0.007)) ** (level - 1)) * 1000

                # Update text for score, lines cleared, and level
                scoreText = font.render("Score: " + str(score), False, UI_COLORS[theme]["text"])
                texts[2][0] = scoreText
                linesText = font.render("Lines: " + str(linesCleared), False, UI_COLORS[theme]["text"])
                texts[3][0] = linesText
                levelText = font.render("Level: " + str(level), False, UI_COLORS[theme]["text"])
                texts[4][0] = levelText

                render(pygame, surface, grid, piece, rotation, pieceX, pieceY, heldPiece, nextPieces, texts, theme)
            else:
                # Display PAUSED Text
                largeFont = pygame.font.SysFont('calibri', 48)
                pausedText = largeFont.render("PAUSED", False, (0, 255, 0))
                pausedTextRect = pausedText.get_rect()
                pausedTextRect.topleft = (8 * 20, 7 * 20)
                surface.blit(pausedText, pausedTextRect)
                pygame.display.flip()
        else:
            # Display GAME OVER Text
            largeFont = pygame.font.SysFont('calibri', 48)
            gameOverText = largeFont.render("GAME OVER", False, (255, 0, 0))
            gameOverTextRect = gameOverText.get_rect()
            gameOverTextRect.topleft = (6 * 20, 7 * 20)
            surface.blit(gameOverText, gameOverTextRect)
            pygame.display.flip()


main()

