import pyglet
from pyglet.window import key, Window
from pyglet import clock
from pyglet import shapes
import random
from sprites.cell import Cell
from sprites.player_pyglet import Player
from time import time
w, a, s, d, SHIFT = False, False, False, False, False

x, y = 0, 0

size = (500, 500)
CELL_WIDTH = 100
FULLSCREEN: bool = False

config = pyglet.gl.Config(double_buffer=True)
window = Window(size[0], size[1], 'Maze Race', config=config)  # Defines window

done = False
cols = int(size[0] // CELL_WIDTH)
rows = int(size[1] // CELL_WIDTH)

px = random.randint(2, cols-3) * CELL_WIDTH + CELL_WIDTH//2
py = random.randint(2, rows-3) * CELL_WIDTH + CELL_WIDTH//2

grid = []
stack = []

# NOTE loading pyglet stuff
maze_cells_batch = pyglet.graphics.Batch()
player_batch = pyglet.graphics.Batch()
FPS: int = 120
# Show FPS
# fps = clock.clockDisplay()

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
PLAYER_COLOR: tuple = (12, 12, 255)
BACKGROUND_COLOR: tuple = (30, 30, 30)

END_COLOR: tuple = (220, 50, 50, 10)
START_COLOR: tuple = (50, 220, 50, 10)
pyglet.gl.glClearColor(
    BACKGROUND_COLOR[0]/255, BACKGROUND_COLOR[1]/255, BACKGROUND_COLOR[2]/255, 1)  # background color

# NOTE MAZE GEN VARS

# bottom left, top left, bottom right, top right
random_ending_positions = [(0, 0), (0, rows-1), (cols-1, 0), (cols-1, rows-1)]
random_end = random.choice(random_ending_positions)

next_cell = 0

play_game = False
finished_maze = False
generated_maze = False
saved_maze = False
player1 = None


@window.event
def on_key_press(symbol, modifiers):  # Looks for a keypress
    global w, a, s, d, SHIFT
    if symbol == key.W:
        w = True
    elif symbol == key.A:
        a = True
    elif symbol == key.S:
        s = True
    elif symbol == key.D:
        d = True
    elif symbol == key.Q:
        reset_maze()
    elif symbol == 65505:
        SHIFT = True


@window.event
def on_key_release(symbol, modifiers):
    global w, a, s, d, SHIFT
    if symbol == key.W:
        w = False
    elif symbol == key.A:
        a = False
    elif symbol == key.S:
        s = False
    elif symbol == key.D:
        d = False
    elif symbol == 65505:
        SHIFT = False


@window.event
def on_mouse_motion(x1, y1, dx, dy):
    global x, y
    x = x1
    y = y1


@window.event
def update(dt):  # Update movements
    global finished_maze, generated_maze, player1, grid, cols, rows, maze_cells_batch, x, y
    player1.update(x, y, SHIFT, dt, cols, rows, grid, maze_cells_batch, size)
    player1.finishX, player1.finishY = random_end[0], random_end[1]

    if player1.cell_X == random_end[0] and player1.cell_Y == random_end[1]:
        reset_maze()
        load_maze()
    import time

    # pygame.draw.rect(screen,GREEN,(px-CELL_WIDTH//2,py-CELL_WIDTH//2,CELL_WIDTH,CELL_WIDTH))
    # pygame.draw.rect(screen,RED,(random_end[0]*CELL_WIDTH, random_end[1]*CELL_WIDTH, CELL_WIDTH, CELL_WIDTH))


framerate = pyglet.text.Label(text='Unknown', font_name='Verdana',
                              font_size=8, x=10, y=size[1]-10, color=(255, 255, 255, 255))
last = time()
frames = 0


@window.event
def on_draw():  # Main update loop
    global maze_cells_batch, generated_maze, play, saved_maze, player1, random_end, px, py, frames, last, framerate
    window.clear()
    if not generated_maze:
        load_maze()
    # render_maze()
    # END OF MAZE
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f/stream', [random_end[0]*CELL_WIDTH, random_end[1]*CELL_WIDTH, random_end[0]*CELL_WIDTH, random_end[1]*CELL_WIDTH+CELL_WIDTH, random_end[0]
                         * CELL_WIDTH+CELL_WIDTH, random_end[1]*CELL_WIDTH+CELL_WIDTH, random_end[0]*CELL_WIDTH+CELL_WIDTH, random_end[1]*CELL_WIDTH]), ('c4B', (END_COLOR[0], END_COLOR[1], END_COLOR[2], END_COLOR[3])*4))
    # SPAWN POINT
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f/stream', [px-CELL_WIDTH//2, py-CELL_WIDTH//2, px-CELL_WIDTH//2, py-CELL_WIDTH//2+CELL_WIDTH, px-CELL_WIDTH//2+CELL_WIDTH,
                         py-CELL_WIDTH//2+CELL_WIDTH, px-CELL_WIDTH//2+CELL_WIDTH, py-CELL_WIDTH//2]), ('c4B', (START_COLOR[0], START_COLOR[1], START_COLOR[2], START_COLOR[3])*4))
    maze_cells_batch.draw()
    player1.draw()
    if time() - last >= 1:
        framerate.text = str(frames)
        frames = 0
        last = time()
    else:
        frames += 1
    framerate.draw()

    # window.flip()


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


def start_game():
    global play_game
    play_game = True


def quit_game():
    global done
    done = True


def reset_maze():
    global current_cell, grid, generated_maze, play, saved_maze, maze_cells_batch, random_end, px, py, player1
    px = random.randint(2, cols-3) * CELL_WIDTH + CELL_WIDTH//2
    py = random.randint(2, rows-3) * CELL_WIDTH + CELL_WIDTH//2
    player1.Player_Sprite.x = px
    player1.Player_Sprite.y = py
    maze_cells_batch = pyglet.graphics.Batch()
    play, generated_maze = False, False
    grid = []
    for y in range(rows):
        grid.append([])
        for x in range(cols):
            grid[y].append(
                Cell(x, y, CELL_WIDTH, PLAYER_COLOR, BACKGROUND_COLOR))

    random_end = random.choice(random_ending_positions)

    # Creates the end of maze (Where it begins)
    current_cell = grid[random_end[1]][random_end[0]]
    player1.reset()
    load_maze()


def load_maze():
    global play, finished_maze, generated_maze, maze_cells_batch, current_cell, grid, cols, rows
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
        saved_maze = False
        generated_maze = True
        # grid = grid[::-1]
    if SHOW_MAZE:
        render_maze()
    # enable this code to visualize the maze being generated incrementally
    # for y in range(rows):
    #     for x in range(cols):
    #         grid[y][x].draw(maze_cells_batch)


def render_maze():
    for y in range(rows):
        for x in range(cols):
            grid[y][x].draw(maze_cells_batch)


def load_player():
    global px, py
    px = random.randint(2, rows-2) * CELL_WIDTH + CELL_WIDTH//2
    py = random.randint(2, cols-2) * CELL_WIDTH + CELL_WIDTH//2
    vignette_sprte = pyglet.image.load("./assets/vignette.png")
    vignette_sprte.anchor_x = vignette_sprte.width // 2  # this line is new
    vignette_sprte.anchor_y = vignette_sprte.height // 2  # and this line also
    vignette = pyglet.sprite.Sprite(vignette_sprte, x=px, y=py)
    Player_Sprite = pyglet.image.load("assets/player.png")
    Player_Sprite.anchor_x = Player_Sprite.width // 2  # this line is new
    Player_Sprite.anchor_y = Player_Sprite.height // 2  # and this line also
    player = pyglet.sprite.Sprite(Player_Sprite, x=px, y=py)
    player.draw()
    return Player(player, PLAYER_COLOR, vignette, (px, py), CELL_WIDTH, SHOW_VIGNETEE, size)


def main():
    global player1
    initialized = False
    player1 = load_player()
    player1.change_debugging_mode(DEVELOPER_MODE, ENABLE_MAZE_COL)

    window.clear()
    reset_maze()
    load_maze()
    # pyglet.clock.schedule_interval(update, 1.0/128.0)
    # pyglet.clock.set_fps_limit(128)
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()


if __name__ == '__main__':
    main()
