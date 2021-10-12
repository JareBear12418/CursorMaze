# import pygame
from pyglet import shapes
import random
# importing pyglet module
import pyglet
from pyglet import gl

pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

# importing shapes from the pyglet
WHITE = (255, 255, 255)
# GREY = (12,12,25) # Nice dark blue for player matching
GREY = (12, 12, 12)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 75, 75)
GREEN = (75, 255, 75)
BLUE = (0, 0, 255)


class Cell():
    def __init__(self, x, y, width, color, backgroundColor):
        self.width = width
        self.WALL_WIDTH = 4
        pyglet.gl.glLineWidth(self.WALL_WIDTH)

        self.WALL_COLOR = (130, 130, 130)
        self.BACKGROUNDCOLOR = backgroundColor
        self.cells_list = []
        self.batch = pyglet.graphics.Batch()
        self.x = x * self.width
        self.y = y * self.width

        self.visited = False
        self.end = False

        self.walls = [True, True, True, True]  # top , right , bottom , left

        # neighbors
        self.neighbors = []

        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0

        # x1, x2, y1, x2
        self.top_wall_1 = (self.x + self.width, self.y)
        self.top_wall_2 = (self.x, self.y)

        self.right_wall_1 = (self.x + self.width, self.y)
        self.right_wall_2 = (self.x + self.width, self.y + self.width)

        self.bottom_wall_1 = (self.x + self.width, self.y + self.width)
        self.bottom_wall_2 = (self.x, self.y + self.width)

        self.left_wall_1 = (self.x, self.y + self.width)
        self.left_wall_2 = (self.x, self.y)

        self.next_cell = 0

        self.should_draw = True

    def draw(self, batch):
        # if not self.should_draw:
        #     return
        if self.end:
            pass
            # pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [self.x, self.y+self.width, self.x+self.width, self.y+self.width, self.x+self.width, self.y, self.x, self.y]), ('c3B', (0,0,0, 0,0,0, 0,0,0, 0,0,0)))
            # s = shapes.Rectangle(self.x,self.y,self.width,self.width, color = BLACK, batch = batch)
            # self.cells_list.append(s)
            # pygame.draw.rect(screen,BLACK,(self.x,self.y,self.width,self.width)) #end to maze
            # pass
        elif self.visited:

            # pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [self.x, self.y+self.width, self.x+self.width, self.y+self.width, self.x+self.width, self.y, self.x, self.y]), ('c3B', (0,0,0, 0,0,0, 0,0,0, 0,0,0)))
            # s = shapes.Rectangle(self.x,self.y,self.width,self.width, color = BLACK, batch = batch)
            # self.cells_list.append(s)
            # pygame.draw.rect(screen,BLACK,(self.x,self.y,self.width,self.width)) #cells for maze
            if self.walls[0]:  # TOP [0]
                batch.add(2, gl.GL_LINES, None, ('v2f', (self.x + self.width, self.y, self.x, self.y)), ('c3B',
                          (self.WALL_COLOR[0], self.WALL_COLOR[1], self.WALL_COLOR[2], self.WALL_COLOR[0], self.WALL_COLOR[1], self.WALL_COLOR[2])))
            else:
                batch.add(2, gl.GL_LINES, None, ('v2f', (self.x + self.width-(self.WALL_WIDTH/2), self.y, self.x+(self.WALL_WIDTH/2), self.y)), ('c3B',
                          (self.BACKGROUNDCOLOR[0], self.BACKGROUNDCOLOR[1], self.BACKGROUNDCOLOR[2], self.BACKGROUNDCOLOR[0], self.BACKGROUNDCOLOR[1], self.BACKGROUNDCOLOR[2])))
                # s=shapes.Line(self.x,self.y, self.x + self.width,self.y, self.WALL_WIDTH, color = self.WALL_COLOR, batch = batch)
                # self.cells_list.append(s)
                # pygame.draw.line(screen,self.WALL_COLOR,
                #                  (self.x,self.y),
                #                  ((self.x + self.width),self.y),
                #                  self.WALL_WIDTH) # top
            if self.walls[1]:  # RIGHT
                batch.add(2, gl.GL_LINES, None, ('v2f', (self.x + self.width, self.y, self.x + self.width, self.y + self.width)), ('c3B',
                          (self.WALL_COLOR[0], self.WALL_COLOR[1], self.WALL_COLOR[2], self.WALL_COLOR[0], self.WALL_COLOR[1], self.WALL_COLOR[2])))
            else:
                batch.add(2, gl.GL_LINES, None, ('v2f', (self.x + self.width, self.y+(self.WALL_WIDTH/2), self.x + self.width, self.y + self.width-(self.WALL_WIDTH/2))),
                          ('c3B', (self.BACKGROUNDCOLOR[0], self.BACKGROUNDCOLOR[1], self.BACKGROUNDCOLOR[2], self.BACKGROUNDCOLOR[0], self.BACKGROUNDCOLOR[1], self.BACKGROUNDCOLOR[2])))
                # s = shapes.Line(self.x + self.width,self.y, self.x + self.width,self.y + self.width, self.WALL_WIDTH, color = self.WALL_COLOR, batch = batch)
                # self.cells_list.append(s)
                # pygame.draw.line(screen,self.WALL_COLOR,
                #                  ((self.x + self.width),self.y),
                #                  ((self.x + self.width),(self.y + self.width)),
                #                  self.WALL_WIDTH) # right
            if self.walls[2]:  # BOTTOM [2]
                batch.add(2, gl.GL_LINES, None, ('v2f', (self.x + self.width, self.y + self.width, self.x, self.y + self.width)), ('c3B',
                          (self.WALL_COLOR[0], self.WALL_COLOR[1], self.WALL_COLOR[2], self.WALL_COLOR[0], self.WALL_COLOR[1], self.WALL_COLOR[2])))
            else:
                batch.add(2, gl.GL_LINES, None, ('v2f', (self.x + self.width, self.y + self.width, self.x, self.y + self.width)), ('c3B',
                          (self.BACKGROUNDCOLOR[0], self.BACKGROUNDCOLOR[1], self.BACKGROUNDCOLOR[2], self.BACKGROUNDCOLOR[0], self.BACKGROUNDCOLOR[1], self.BACKGROUNDCOLOR[2])))
                # s = shapes.Line(self.x + self.width,self.y + self.width, self.x,self.y + self.width, self.WALL_WIDTH, color = self.WALL_COLOR, batch = batch)
                # self.cells_list.append(s)
                # pygame.draw.line(screen,self.WALL_COLOR,
                #                  ((self.x + self.width),(self.y + self.width)),
                #                  (self.x,(self.y + self.width)),
                #                  self.WALL_WIDTH) # bottom
            if self.walls[3]:  # LEFT
                batch.add(2, gl.GL_LINES, None, ('v2f', (self.x, self.y + self.width, self.x, self.y)), ('c3B',
                          (self.WALL_COLOR[0], self.WALL_COLOR[1], self.WALL_COLOR[2], self.WALL_COLOR[0], self.WALL_COLOR[1], self.WALL_COLOR[2])))
            else:
                batch.add(2, gl.GL_LINES, None, ('v2f', (self.x, self.y + self.width-self.WALL_WIDTH, self.x, self.y+(self.WALL_WIDTH/2))), ('c3B',
                          (self.BACKGROUNDCOLOR[0], self.BACKGROUNDCOLOR[1], self.BACKGROUNDCOLOR[2], self.BACKGROUNDCOLOR[0], self.BACKGROUNDCOLOR[1], self.BACKGROUNDCOLOR[2])))
                # s = shapes.Line(self.x,self.y + self.width, self.x, self.y, self.WALL_WIDTH, color = self.WALL_COLOR, batch = batch)
                # self.cells_list.append(s)
                # pygame.draw.line(screen,self.WALL_COLOR,
                #                  (self.x,(self.y + self.width)),
                #                  (self.x,self.y),
                #                  self.WALL_WIDTH) # left
            # else:
            #     s = shapes.Line(0,0,0,0, color = BLACK, batch = batch)
            #     self.cells_list.append(s)
            # try: return s
            # except: pass

    def checkNeighbors(self, cols, rows, grid):
        # print(f"Top; y: {str(int(self.y / self.width))} y - 1: {str(int(self.y / self.width) - 1)}")
        if int(self.y / self.width) >= 1:
            self.top = grid[int(self.y / self.width)
                            - 1][int(self.x / self.width)]

        # print(f"Right; x: {str(int(self.x / self.width))} x + 1: {str(int(self.x / self.width) + 1)}")
        if int(self.x / self.width) + 1 <= cols - 1:
            self.right = grid[int(self.y / self.width)
                              ][int(self.x / self.width) + 1]

        # print(f"Bottom; y: {str(int(self.y / self.width))} y + 1: {str(int(self.y / self.width) + 1)}")
        if int(self.y / self.width) + 1 <= rows - 1:
            self.bottom = grid[int(self.y / self.width)
                               + 1][int(self.x / self.width)]

        # print(f"Left; x: {str(int(self.x / self.width))} x - 1: {str(int(self.x / self.width) - 1)}")
        if int(self.x / self.width) >= 1:
            self.left = grid[int(self.y / self.width)
                             ][int(self.x / self.width) - 1]
        # print("--------------------")

        if self.top != 0 and self.top.visited == False:
            self.neighbors.append(self.top)
        if self.right != 0 and self.right.visited == False:
            self.neighbors.append(self.right)
        if self.bottom != 0 and self.bottom.visited == False:
            self.neighbors.append(self.bottom)
        if self.left != 0 and self.left.visited == False:
            self.neighbors.append(self.left)

        if len(self.neighbors) <= 0:
            return False

        self.next_cell = self.neighbors[random.randrange(
            0, len(self.neighbors))]
        return self.next_cell
