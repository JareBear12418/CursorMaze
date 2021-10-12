import random
import pygame
from pprint import pprint as print
from sprites.cell import Cell
from sprites.player import Player
from PIL import Image
import numpy as np
import ui_manager


pygame.init()

WHITE = (240, 240, 240)
GREY = (12, 12, 12)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (0, 0, 255)

size = (500, 500)
CELL_WIDTH = 50

FULLSCREEN: bool = False

if FULLSCREEN:
    flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
else:
    flags = pygame.DOUBLEBUF

screen = pygame.display.set_mode(size, flags)

pygame.display.set_caption("Maze Racer")

done = False

clock = pygame.time.Clock()

cols = int(size[0] // CELL_WIDTH)
rows = int(size[1] // CELL_WIDTH)
grid = []
stack = []

pos = (0, 0)


# NOTE DEBUGGING OR DEVELOPMENT ONLY
'''
Shows debugging text
Press "q" to finish maze
'''
DEVELOPER_MODE: bool = True
SHOW_MAZE: bool = True
ENABLE_MAZE_COL: bool = True

# NOTE GAME RULES
SHOW_VIGNETEE: bool = False
PLAYER_COLOR: tuple = (50, 50, 150)
BACKGROUND_COLOR: tuple = (12, 12, 12)


def load_player():
    global px, py
    pimg = pygame.Surface((10, 10), pygame.SRCALPHA)
    alpha_img = pygame.Surface(pimg.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 140))
    pimg.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    pimg.fill((200, 20, 20))
    overlay = pygame.image.load("./assets/vignette.png")
    px = random.randint(1, rows-2) * CELL_WIDTH + CELL_WIDTH//2
    py = random.randint(1, cols-2) * CELL_WIDTH + CELL_WIDTH//2
    return Player(pimg, PLAYER_COLOR, overlay, (px, py), CELL_WIDTH, SHOW_VIGNETEE)


def removeWalls(current_cell, next_cell):
    x = int(current_cell.x / CELL_WIDTH) - int(next_cell.x / CELL_WIDTH)
    y = int(current_cell.y / CELL_WIDTH) - int(next_cell.y / CELL_WIDTH)
    if x == -1:  # right of current
        current_cell.walls[1] = False
        next_cell.walls[3] = False
    elif x == 1:  # left of current
        current_cell.walls[3] = False
        next_cell.walls[1] = False
    elif y == -1:  # bottom of current
        current_cell.walls[2] = False
        next_cell.walls[0] = False
    elif y == 1:  # top of current
        current_cell.walls[0] = False
        next_cell.walls[2] = False


for y in range(rows):
    grid.append([])
    for x in range(cols):
        grid[y].append(Cell(x, y, CELL_WIDTH, PLAYER_COLOR, BACKGROUND_COLOR))

random_ending_positions = [(0, 0), (0, rows-1), (cols-1, 0), (rows-1, cols-1)]
random_end = random.choice(random_ending_positions)

current_cell = grid[random_end[0]][random_end[1]]
next_cell = 0

play_game = False
# -------- Main Program Loop -----------


def main():
    global current_cell, grid, random_end, px, py, play_game, done
    player = None
    initialized = False
    dt = 0
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    if not initialized:  # Only runs once. When program starts
        player = load_player()
        player.change_debugging_mode(DEVELOPER_MODE, ENABLE_MAZE_COL)
        sprites.add(player)
        saved_maze = False
        initialized = True

    play = False
    while not done:
        if play_game:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            if play:
                # Covers up everything with dark blue
                screen.fill((12, 12, 25))
                # BUG THIS TAKES ALOT OF PERFORMANCE loads maze
                if SHOW_MAZE:
                    if not saved_maze:
                        for y in range(rows):
                            for x in range(cols):
                                grid[y][x].draw(screen)
                        # remove all black and make transparent
                        pygame.image.save(screen, "maze.png")
                        # Load image and ensure it is 3-channel RGB...
                        # ... not 1-channel greyscale, not 4-channel RGBA, not 1-channel palette
                        im = Image.open('maze.png').convert('RGB')
                        # Make into Numpy array of RGB and get dimensions
                        RGB = np.array(im)
                        h, w = RGB.shape[:2]
                        # Add an alpha channel, fully opaque (255)
                        RGBA = np.dstack(
                            (RGB, np.zeros((h, w), dtype=np.uint8)+255))
                        # Make mask of black pixels - mask is True where image is black
                        mBlack = (RGBA[:, :, 0:3] == [0, 0, 0]).all(2)
                        # Make all pixels matched by mask into transparent ones
                        RGBA[mBlack] = (0, 0, 0, 0)
                        # Convert Numnpy array back to PIL Image and save
                        Image.fromarray(RGBA).save('maze.png')
                        saved_maze = True
                    # laod maze.png and ignore alpha
                    maze = pygame.image.load("maze.png").convert_alpha()
                    pygame.draw.rect(
                        screen, GREEN, (px-CELL_WIDTH//2, py-CELL_WIDTH//2, CELL_WIDTH, CELL_WIDTH))
                    pygame.draw.rect(
                        screen, RED, (random_end[0]*CELL_WIDTH, random_end[1]*CELL_WIDTH, CELL_WIDTH, CELL_WIDTH))
                    screen.blit(maze, (0, 0))
                player.draw(screen)
                # sprites.update(None, dt, cols, rows, grid) # Player trail
                # FIXME draw to maze instead of screen
                player.update(None, dt, cols, rows, grid)

                dt = clock.tick(60)  # set clock speed higher is faster.

                finished = pygame.Rect(random_end[0]*CELL_WIDTH, random_end[1]*CELL_WIDTH, random_end[0]
                                       * CELL_WIDTH+CELL_WIDTH, random_end[1]*CELL_WIDTH+CELL_WIDTH).colliderect(player.rect)

                if DEVELOPER_MODE:
                    font = pygame.font.SysFont('arial.ttf', 22)
                    player_pos_text = font.render(
                        f'Player pos: x={int(player.pos.x)}, y={int(player.pos.y)}', True, (0, 255, 0))

                    text_to_draw = [player_pos_text]
                    screen.blit(player_pos_text, (10, 10))
                    # screen.blit([t for t in text_to_draw],(10,10))

                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_q] and DEVELOPER_MODE:
                    finished = True
                if finished:

                    saved_maze = False
                    # init new grid
                    grid = []
                    for y in range(rows):
                        grid.append([])
                        for x in range(cols):
                            grid[y].append((x, y, CELL_WIDTH, PLAYER_COLOR))
                    # create new random player positon
                    px = random.randint(1, rows-2) * CELL_WIDTH + CELL_WIDTH//2
                    py = random.randint(1, cols-2) * CELL_WIDTH + CELL_WIDTH//2

                    player.pos = pygame.Vector2(px, py)
                    player.rect = player.image.get_rect(center=player.pos)

                    player.reset()
                    # clear screen
                    screen.fill(0)
                    play = False
                    random_end = random.choice(random_ending_positions)
                    current_cell = grid[random_end[1]][random_end[0]]

            else:
                # Creates the end of maze (Where it begins)
                current_cell.visited = True
                current_cell.current = True

                next_cell = current_cell.checkNeighbors(cols, rows, grid)
                if next_cell != False:
                    current_cell.neighbors = []
                    stack.append(current_cell)
                    removeWalls(current_cell, next_cell)
                    current_cell.current = False
                    current_cell = next_cell
                elif len(stack) > 0:
                    current_cell.current = False
                    current_cell = stack.pop()
                else:
                    play = True

                # enable this code to visualize the maze being generated incrementally
                # for y in range(rows):
                #     for x in range(cols):
                #         grid[y][x].draw(screen)
        else:  # were in the menu
            ui_manager.Main_Menu(size, screen, start_game, quit_game)
        pygame.display.flip()


def start_game():
    global play_game
    play_game = True


def quit_game():
    global done
    done = True


if __name__ == '__main__':
    main()
    pygame.quit()
