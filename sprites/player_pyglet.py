import pyglet
from sprites.rect import Rect
import math
from pyglet import gl
import random
from pprint import pprint as print
BLACK = (0, 0, 0)


class Ray():
    def __init__(self, origin, x, y, color, opacity, RAYS_BATCH):
        self.origin = origin
        self.x = x
        self.y = y
        self.color = color
        self.opacity = opacity
        self.RAYS_BATCH = RAYS_BATCH

    def draw(self):
        # self.RAYS_BATCH.add(2, gl.GL_LINES, None, ('v2f/stream', (self.origin[0],self.origin[1], self.x,self.y)), ('c3B', (self.color[0],self.color[1],self.color[2] , self.color[0],self.color[1],self.color[2])))
        ray = pyglet.shapes.Line(
            self.origin[0], self.origin[1], self.x, self.y, 1, color=self.color, batch=self.RAYS_BATCH)
        ray.opacity = self.opacity
        # ray.draw()
        return ray
        # self.RAYS_LIST.append(ray)


class Player():
    def __init__(self, image, player_color, overlay, pos, width, show_vignete, screen):
        self.width = width
        self.Player_Sprite = image
        self.PLAYER_COLOR = player_color
        self.pos = pos
        self.cell_X, self.cell_Y = 0, 0

        self.finishX, self.finishY = 0, 0
        self.points_of_collision = []

        self.vignette = overlay
        self.vignette_rect = Rect(pos[0], pos[1], self.vignette)
        # self.vignette_rect = self.vignette.get_rect(center=self.pos)
        self.rect = Rect(pos[0], pos[1], self.Player_Sprite)
        # self.rect = self.Player_Sprite.get_rect(center=self.pos)
        self.SHAPE: str = 'CIRCLE'  # ! 'SQAURE' OR 'CIRCLE'
        self.SHOW_VIGNETEE: bool = show_vignete
        self.smooth_time: float = 1
        self.time: float = 0

        self.RENDERED_TEXT: bool = False
        self.BARS_BATCH = pyglet.graphics.Batch()
        self.TEXT_BATCH = pyglet.graphics.Batch()

        self.RAYS_BATCH = pyglet.graphics.Batch()
        self.RAYS_LIST = []

        self.TEXT_LIST: list = []

        self.TRAIL_POSTITIONS: list = []
        self.TRAIL_MAX_LENGTH: int = 25
        self.TRAIL_BATCH = pyglet.graphics.Batch()
        self.TRAIL_LINES: list = []
        # self.TAIL = self.LOAD_TRAIL(self.TRrangeAIL_IMAGE, self.PLAYER_COLOR)

        self.IS_MOVING: bool = False
        self.SPEED_BOOST: float = 1.05
        self.SPEED_BOOST_DURATION: float = 10
        self.MAX_SPEED_DURATION: float = 10

        self.health = 5
        self.MAX_HEALTH = 5
        self.screen_width, self.screen_height = screen

    def reset(self):
        self.health = self.MAX_HEALTH
        self.SPEED_BOOST_DURATION = self.MAX_SPEED_DURATION
        self.TRAIL_POSTITIONS.clear()
        self.TRAIL_BATCH = pyglet.graphics.Batch()

    def change_debugging_mode(self, dev_mode, maze_col):
        # NOTE DEBUGGING OR DEVELOPMENT ONLY
        self.DEVELOPER_MODE: bool = dev_mode
        self.ENABLE_MAZE_GOL: bool = maze_col

    def update(self, x, y, SHIFT, dt, cols, rows, grid, maze_cells_batch, screen_size):  # Update movements
        self.grid = grid
        self.rows = rows
        self.cols = cols
        if screen_size[0] > screen_size[1]:
            self.MAX_RAY_LENGTH = screen_size[0]
        else:
            self.MAX_RAY_LENGTH = screen_size[1]
        self.maze_cells_batch = maze_cells_batch
        self.rect.update(self.Player_Sprite.x, self.Player_Sprite.y)

        if len(self.TRAIL_POSTITIONS) >= self.TRAIL_MAX_LENGTH:
            if not self.IS_MOVING:
                self.TRAIL_POSTITIONS.append(
                    (self.Player_Sprite.x, self.Player_Sprite.y))
                try:
                    self.TRAIL_LINES.append(self.line)
                except:
                    pass
            self.TRAIL_POSTITIONS.pop(0)
            self.TRAIL_LINES.pop(0)
        else:
            self.TRAIL_POSTITIONS.append(
                (self.Player_Sprite.x, self.Player_Sprite.y))
            try:
                self.TRAIL_LINES.append(self.line)
            except:
                pass

        self.vignette_rect.update(self.Player_Sprite.x, self.Player_Sprite.y)
        self.vignette.x = self.rect.left()
        self.vignette.y = self.rect.bottom()
        testdist = dt // 5  # distance from the wall
        self.cell_X = int(self.rect.centerx() // self.width)
        self.cell_Y = int(self.rect.centery() // self.width)
        # min_X = self.rect.leftX() // self.width
        # max_X = self.rect.rightX() // self.width
        # min_Y = self.rect.topY() // self.width
        # max_Y = self.rect.bottomY() // self.width

        w, a, s, d = False, False, False, False
        if x > self.Player_Sprite.x:
            d = True
            a = False
        elif x < self.Player_Sprite.x:
            d = False
            a = True
        if y > self.Player_Sprite.y:
            w = True
            s = False
        elif y < self.Player_Sprite.y:
            w = False
            s = True

        if not w and not a and not s and not d:
            self.IS_MOVING = False
        else:
            self.IS_MOVING = True
        self.TRAIL_MAX_LENGTH = 25
        speed = 10
        if (
            self.time >= self.smooth_time
            and SHIFT
            and self.SPEED_BOOST_DURATION >= 0
            and self.IS_MOVING
        ):
            self.SPEED_BOOST_DURATION -= 0.03
            speed = 4
            self.TRAIL_MAX_LENGTH = 27
        if not self.IS_MOVING and self.SPEED_BOOST_DURATION <= self.MAX_SPEED_DURATION:
            self.SPEED_BOOST_DURATION += 0.03

        if self.ENABLE_MAZE_GOL:
            if w == True:  # UP
                self.time += 0.03
                next_Y = ((self.rect.top()-testdist) // self.width)
                is_wall = self.grid[self.cell_Y][self.cell_X].walls[2]
                if self.cell_Y == next_Y or (next_Y >= 0 and not is_wall):
                    self.Player_Sprite.y += speed
            elif s == True:  # DOWN
                self.time += 0.03
                next_Y = (
                    (self.rect.bottom()-(self.Player_Sprite.height)+testdist) // self.width)
                is_wall = self.grid[self.cell_Y][self.cell_X].walls[0]
                if self.cell_Y == next_Y or (next_Y < self.rows and not is_wall):
                    self.Player_Sprite.y -= speed
            if a == True:  # LEFT
                self.time += 0.03
                next_X = (
                    (self.rect.left()-(self.Player_Sprite.width)-testdist) // self.width)
                is_wall = self.grid[self.cell_Y][self.cell_X].walls[3]
                if self.cell_X == next_X or (next_X >= 0 and not is_wall):
                    self.Player_Sprite.x -= speed
            elif d == True:  # RIGHT
                self.time += 0.03
                next_X = ((self.rect.right()+testdist) // self.width)
                is_wall = self.grid[self.cell_Y][self.cell_X].walls[1]
                if self.cell_X == next_X or (next_X < self.cols and not is_wall):
                    self.Player_Sprite.x += speed
        else:
            self.Player_Sprite.x = x
            self.Player_Sprite.y = y
            # if w == True:
            #     self.Player_Sprite.y += 5
            # elif s == True:
            #     self.Player_Sprite.y -= 5
            # if a == True:
            #     self.Player_Sprite.x -= 5
            # elif d == True:
            #     self.Player_Sprite.x += 5
            # self.rotate(w, a, s, d)

    def draw(self):
        # gl stuff
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA,
                              pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        pyglet.gl.glEnable(pyglet.gl.GL_LINE_SMOOTH)
        pyglet.gl.glHint(pyglet.gl.GL_LINE_SMOOTH_HINT, pyglet.gl.GL_DONT_CARE)

        self.RAYS_BATCH = pyglet.graphics.Batch()
        self.LEFT_BOTTOM_BATCH = pyglet.graphics.Batch()
        self.RIGHT_BOTTOM_BATCH = pyglet.graphics.Batch()
        self.LEFT_TOP_BATCH = pyglet.graphics.Batch()
        self.RIGHT_TOP_BATCH = pyglet.graphics.Batch()

        self.TOP_BATCH = pyglet.graphics.Batch()
        self.BOTTOM_BATCH = pyglet.graphics.Batch()
        self.RIGHT_BATCH = pyglet.graphics.Batch()
        self.LEFT_BATCH = pyglet.graphics.Batch()

        self.RAYS_LIST.clear()
        # x2 = math.cos(0) * 100 + self.Player_Sprite.x
        # y2 = math.sin(0) * 100 + self.Player_Sprite.y
        x3 = self.Player_Sprite.x
        y3 = self.Player_Sprite.y
        try:

            self.total_walls_in_cell = []
            points = []
            for y in range(self.rows):
                for x in range(self.cols):
                    wall_top: bool = self.grid[y][x].walls[0]
                    wall_right: bool = self.grid[y][x].walls[1]
                    wall_bottom: bool = self.grid[y][x].walls[2]
                    wall_left: bool = self.grid[y][x].walls[3]
                    if wall_top:
                        x1 = self.grid[y][x].top_wall_1[0]
                        y1 = self.grid[y][x].top_wall_1[1]
                        x2 = self.grid[y][x].top_wall_2[0]
                        y2 = self.grid[y][x].top_wall_2[1]
                        self.total_walls_in_cell.append([(x1, y1), (x2, y2)])
                        # self.total_walls_in_cell.append((x1, y1))
                        # self.total_walls_in_cell.append((x2, y2))
                    if wall_right:  # RIGHT
                        x1 = self.grid[y][x].right_wall_1[0]
                        y1 = self.grid[y][x].right_wall_1[1]
                        x2 = self.grid[y][x].right_wall_2[0]
                        y2 = self.grid[y][x].right_wall_2[1]
                        self.total_walls_in_cell.append([(x1, y1), (x2, y2)])
                        # self.total_walls_in_cell.append((x1, y1))
                        # self.total_walls_in_cell.append((x2, y2))
                    if wall_left:  # LEFT
                        x1 = self.grid[y][x].left_wall_1[0]
                        y1 = self.grid[y][x].left_wall_1[1]
                        x2 = self.grid[y][x].left_wall_2[0]
                        y2 = self.grid[y][x].left_wall_2[1]
                        self.total_walls_in_cell.append([(x1, y1), (x2, y2)])
                        # self.total_walls_in_cell.append((x1, y1))
                        # self.total_walls_in_cell.append((x2, y2))
                    if wall_bottom:  # BOTTOM
                        x1 = self.grid[y][x].bottom_wall_1[0]
                        y1 = self.grid[y][x].bottom_wall_1[1]
                        x2 = self.grid[y][x].bottom_wall_2[0]
                        y2 = self.grid[y][x].bottom_wall_2[1]
                        self.total_walls_in_cell.append([(x1, y1), (x2, y2)])
                        # self.total_walls_in_cell.append((x1, y1))
                        # self.total_walls_in_cell.append((x2, y2))
        except Exception as e:
            print(f'{e} 2')

        # for i in range(lines):
        for wall in self.total_walls_in_cell:
            x1 = wall[0][0]
            y1 = wall[0][1]
            x2 = wall[1][0]
            y2 = wall[1][1]
            points.append((x1, y1))
            points.append((x2, y2))
            # distance = math.hypot(x3 - x1, y3 - y1)
            # if distance > 200:
            # distance = math.hypot(x3 - x2, y3 - y2)
            # if distance < 200:
            # ray = Ray((x3, y3), x2, y2, (255,255,255), 40, self.RAYS_BATCH)
            # ray = ray.draw()
            # self.RAYS_LIST.append(ray)
        uniqueAngles = []
        for point in points:
            angle = math.atan2(point[1]-y3, point[0]-x3)
            uniqueAngles.append(angle-0.00001)
            uniqueAngles.append(angle)
            uniqueAngles.append(angle+0.00001)

        # Remove duplicats, this almost triples performance.
        print(f'Before: {len(uniqueAngles)}')
        uniqueAngles = list(set(uniqueAngles))
        print(f'After: {len(uniqueAngles)}')

        uniqueAngles.sort()
        self.points_of_collision.clear()
        self.points_of_collision.append((x3, y3))
        # self.points_of_collision.append(x3)
        # self.points_of_collision.append(y3)
        # self.points_of_collision.append(y3)

        # unique_line_angles = []
        # for wall in self.total_walls_in_cell:
        #     distance = math.hypot(x3 - wall[0][1], y3 - wall[0][0])
        #     if distance < 100:
        #         unique_line_angles.append([(x3, y3), (wall[0][1], wall[0][0])])
        first_point = None
        for angle in uniqueAngles:
            closest = None
            # FOR RAYCASTS
            x4 = math.cos(angle) * 100 + self.Player_Sprite.x
            y4 = math.sin(angle) * 100 + self.Player_Sprite.y
        #     has_intersection = Trueet current I
            for i, wall in enumerate(self.total_walls_in_cell):

                # ANOTHER RAYCASTING IMPLEMNTATION THAT DOESNT WORK
                r_px = x3
                r_py = y3
                r_dx = x4-x3
                r_dy = y4-y3

                s_px = wall[0][0]
                s_py = wall[0][1]
                s_dx = wall[1][0]-wall[0][0]
                s_dy = wall[1][1]-wall[0][1]

                r_mag = math.sqrt(r_dx*r_dx+r_dy*r_dy)
                s_mag = math.sqrt(s_dx*s_dx+s_dy*s_dy)
                try:
                    if(r_dx/r_mag == s_dx/s_mag and r_dy/r_mag == s_dy/s_mag):
                        continue
                    T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px)) / \
                        (s_dx*r_dy - s_dy*r_dx)
                    T1 = (s_px+s_dx*T2-r_px)/r_dx
                    if T1 < 0:
                        continue
                    if T2 < 0 or T2 > 1:
                        continue
                    if not closest or T1 < closest:
                        closest = T1
                except:
                    pass
            try:
                if not first_point:
                    first_point = (r_px+r_dx*closest, r_py+r_dy*closest)
                self.points_of_collision.append(
                    (r_px+r_dx*closest, r_py+r_dy*closest))
                # self.points_of_collision.append(r_px+r_dx*closest)
                # self.points_of_collision.append(r_py+r_dy*closest)
                # self.points_of_collision.sort()
                # ray = Ray((x3, y3), r_px+r_dx*closest, r_py+r_dy*closest,
                #         (255, 255, 255), 10, self.RAYS_BATCH)
                # ray = ray.draw()
                # self.RAYS_LIST.append(ray)
            except (UnboundLocalError, TypeError, IndexError):
                pass
        new_points_of_collision = []
        try:
            # This is to finish the polygon where we started
            # self.points_of_collision.append(first_point[0])
            # self.points_of_collision.append(first_point[1])
            self.points_of_collision.append((first_point))
            for index in range(len(self.points_of_collision)):
                index+1

                x1 = self.points_of_collision[index-1][0]
                y1 = self.points_of_collision[index-1][1]

                x2 = self.points_of_collision[index][0]
                y2 = self.points_of_collision[index][1]

                distance = math.hypot(x1 - x2, y1 - y2)
                if distance < self.MAX_RAY_LENGTH:
                    # print(distance)
                    # else:
                    # new_points_of_collision.append((x1,y1))
                    # new_points_of_collision.append((x2,y2))
                    new_points_of_collision.append(x2)
                    new_points_of_collision.append(y2)
            # Draw rays
            for i in range(len(new_points_of_collision)):
                i+1
                ray = Ray((x3, y3), new_points_of_collision[i-1], new_points_of_collision[i],
                          (255, 255, 255), 10, self.RAYS_BATCH)
                ray = ray.draw()
                self.RAYS_LIST.append(ray)
            # Draw polygon
            ec = int(len(new_points_of_collision)/2)
            self.RAYS_BATCH.add(ec, pyglet.gl.GL_POLYGON, None,
                                ("v2f/stream", new_points_of_collision),
                                ("c4B", (255, 255, 255, 10)*ec))
        except Exception as e:
            print(e)
            # RAYCAST IMPLEMENTATION
           #     x1 = wall[0][0]
           #     y1 = wall[0][1]
           #     x2 = wall[1][0]
           #     y2 = wall[1][1]

           #     denominator = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
           #     t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
           #     u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
           #     # distance = math.sqrt(math.pow((x3-pt1),2)+math.pow((y3-pt2),2))
           #     # FOR RAYCASING
           #     if t > 0 and t < 1 and u > 0:
           #         pt1 = x1 + t * (x2 - x1);
           #         pt2 = y1 + t * (y2 - y1);
           #         distance = math.hypot(x3 - pt1, y3 - pt2)
           #         if distance < record:
           #             record = distance
           #             closest = (pt1, pt2)
           # if closest:
           #     self.points_of_collision.append((closest[0], closest[1]))
           #     # self.points_of_collision.append(closest[0])
           #     # self.points_of_collision.append(closest[1])
           #     ray = Ray((x3, y3), closest[0], closest[1], (255,255,255), 40, self.RAYS_BATCH)
           #     ray = ray.draw()
           #     self.RAYS_LIST.append(ray)
        # except Exception as e: print(f'{e} 2')
        # OLD VIGNETTE METHOD START -----
    #     init_bottom_left = False
    #     init_bottom_right = False
    #     init_top_left = False
    #     init_top_right = False

    #     record_left = 1000
    #     record_right = 0
    #     record_top = 0
    #     record_bottom = 1000
    #     # for i in range(lines):
    #     for index, _ in enumerate(self.points_of_collision):
    #         x1 = self.points_of_collision[index][0]
    #         y1 = self.points_of_collision[index][1]
    #         index + 1
    #         x2 = self.points_of_collision[index][0]
    #         y2 = self.points_of_collision[index][1]
    # #         # distance = math.hypot(x1 - x2, y1 - y2)
    # #         # self.RAYS_BATCH.add(2, gl.GL_LINE_LOOP, None, ('v2f', (x1,y1, x2, y2)), ('c3B', [(255)]*(3*2)))

    # #         #     print(distance)
    # #         #     if distance < record:
    # #         #         record = distance
    # #         #         shortest = (x2, y2)
    # #         # if x2 <= self.Player_Sprite.x and y2 <= self.Player_Sprite.y: # bottom left
    # #         #     if not init_bottom_left:
    # #         #         self.RAYS_BATCH.add(2, gl.GL_TRIANGLE_STRIP, None, ('v2f', (0,0, shortest[0],shortest[1])), ('c3B', [(255)]*(3*2)))
    # #         #         init_bottom_left = True
    # #         #     else:
    # #         #         self.RAYS_BATCH.add(2, gl.GL_TRIANGLE_STRIP, None, ('v2f', (x1,y1, shortest[0],shortest[1])), ('c3B', [(255)]*(3*2)))
    # #         # self.RAYS_BATCH.add(2, gl.GL_LINES, None, ('v2f', (self.points_of_collision[index-1][0],self.points_of_collision[index-1][1],self.points_of_collision[index][0],self.points_of_collision[index][1])), ('c3B', [(100)]*(3*2)))

    #         if x2 < record_left: record_left = x2
    #         if x2 > record_right: record_right = x2
    #         if y2 > record_top: record_top = y2
    #         if y2 < record_bottom: record_bottom = y2
    #         # if y2 > self.Player_Sprite.y and y2 < record_top and x2 >= (self.Player_Sprite.x-10) and x2 <= (self.Player_Sprite.x+10): record_top = y2 # shortest top positon

    #         if x2 <= self.Player_Sprite.x and y2 <= self.Player_Sprite.y: # bottom left
    #             if x1 <= self.Player_Sprite.x and y1 <= self.Player_Sprite.y: # bottom left
    #                 if not init_bottom_left:
    #                     self.LEFT_BOTTOM_BATCH.add(2, gl.GL_TRIANGLE_FAN, None, ('v2f', (0,0, x2,y2)), ('c3B', [(0)]*(3*2)))
    #                     init_bottom_left = True
    #                 else:
    #                     self.LEFT_BOTTOM_BATCH.add(2, gl.GL_TRIANGLE_FAN, None, ('v2f', (x1,y1, x2,y2)), ('c3B', [(0)]*(3*2)))
    #         if x2 <= self.Player_Sprite.x and y2 >= self.Player_Sprite.y: # top left
    #             if x1 <= self.Player_Sprite.x and y1 >= self.Player_Sprite.y:
    #                 if not init_top_left:
    #                     self.LEFT_TOP_BATCH.add(2, gl.GL_TRIANGLE_FAN, None, ('v2f', (0,self.screen_height, x2,y2)), ('c3B', [(0)]*(3*2)))
    #                     init_top_left = True
    #                 else:
    #                     self.LEFT_TOP_BATCH.add(2, gl.GL_TRIANGLE_FAN, None, ('v2f', (x1,y1, x2,y2)), ('c3B', [(0)]*(3*2)))

    #         if x2 >= self.Player_Sprite.x and y2 >= self.Player_Sprite.y: # top right
    #             if x1 >= self.Player_Sprite.x and y1 >= self.Player_Sprite.y: # top right
    #                 if not init_top_right:
    #                     self.RIGHT_TOP_BATCH.add(2, gl.GL_TRIANGLE_FAN, None, ('v2f', (self.screen_width,self.screen_height, x2,y2)), ('c3B', [(0)]*(3*2)))
    #                     init_top_right = True
    #                 else:
    #                     self.RIGHT_TOP_BATCH.add(2, gl.GL_TRIANGLE_FAN, None, ('v2f', (x1,y1, x2,y2)), ('c3B', [(0)]*(3*2)))
    #         if x2 >= self.Player_Sprite.x and y2 <= self.Player_Sprite.y: # bottom right
    #             if x1 >= self.Player_Sprite.x and y1 <= self.Player_Sprite.y: # bottom right
    #                 if not init_bottom_right:
    #                     self.RIGHT_BOTTOM_BATCH.add(2, gl.GL_TRIANGLE_FAN, None, ('v2f', (self.screen_width,0, x2,y2)), ('c3B', [(0)]*(3*2)))
    #                     init_bottom_right = True
    #                 else:
    #                     self.RIGHT_BOTTOM_BATCH.add(2, gl.GL_TRIANGLE_FAN, None, ('v2f', (x1,y1, x2,y2)), ('c3B', [(0)]*(3*2)))

    #             # if y2 > self.Player_Sprite.y and x2 >= (self.Player_Sprite.x) and x2 <= (self.Player_Sprite.x+11):
    #                 # self.TOP_BATCH.add(3, gl.GL_TRIANGLE_FAN, None, ('v2f', (0,self.screen_height, self.screen_width,self.screen_height, x2, y2)), ('c3B', [(170)]*(3*3)))
    #         # self.BOTTOM_BATCH.add(4, gl.GL_QUADS, None, ('v2f', (0,0, self.screen_width,0, self.screen_width, record_bottom, 0, record_bottom)), ('c3B', [(0)]*(3*4)))
    #         # self.LEFT_BATCH.add(4, gl.GL_QUADS, None, ('v2f', (0,0, 0,self.screen_height, record_left,self.screen_height, record_left,0)), ('c3B', [(0)]*(3*4)))
    #         # self.RIGHT_BATCH.add(4, gl.GL_QUADS, None, ('v2f', (self.screen_width,0, self.screen_width,self.screen_height, record_right,self.screen_height, record_right,0)), ('c3B', [(0)]*(3*4)))
        # OLD VIGNETTE METHOD END -----

        # pass
        # print(self.Player_Sprite.x,self.Player_Sprite.y)

        # print(self.rect.x, self.rect.y)s
        # self.Player_Sprite.x = x
        # self.Player_Sprite.y = y

        # print(self.Player_Sprite.x, s)

        # TAIL
        fade_amounts = self.get_fade_values(0, 255, len(self.TRAIL_POSTITIONS))
        size_amounts = self.get_fade_values(0, 7, len(self.TRAIL_POSTITIONS))
        for index, tail_pos in enumerate(self.TRAIL_POSTITIONS):
            try:
                # self.TRAIL_BATCH.addself.makeCircle(tail_pos[0],tail_pos[1],size_amounts[index],12, self.PLAYER_COLOR))
                #     print(index)
                # circle1 = pyglet.shapes.Circle(tail_pos[0], tail_pos[1], size_amounts[index]*10, color = self.PLAYER_COLOR, batch = self.TRAIL_BATCH)
                #     circle1.opacity = 100
                x1 = self.TRAIL_POSTITIONS[index-1][0]
                y1 = self.TRAIL_POSTITIONS[index-1][1]
                x2 = tail_pos[0]
                y2 = tail_pos[1]
                # pyglet.gl.glLineWidth(self.WALL_WIDTH)
                # self.TRAIL_BATCH.add(2, gl.GL_LINES, None, ('v2f', (x,y, self.Player_Sprite.x, self.Player_Sprite.y)), ('c3B', (self.PLAYER_COLOR[0],self.PLAYER_COLOR[1],self.PLAYER_COLOR[2] , self.PLAYER_COLOR[0],self.PLAYER_COLOR[1],self.PLAYER_COLOR[2])))
                self.line = pyglet.shapes.Line(
                    x1, y1, x2, y2, 3, color=self.PLAYER_COLOR, batch=self.TRAIL_BATCH)
                self.line.opacity = 127
                # self.line.opacity = fade_amounts[0]
                # print(fade_amounts)

                # changing opacity of the line2
                # opacity is visibility (0 = invisible, 255 means visible)
            except IndexError:
                # the reason we pass this exception is because at the first index of the list it tries to find the one before and thus crashes.
                pass

        #     pyglet.graphics.draw(4, pyglet.gl.GL_, ('v2f', [0,0,
        #                                                         self.screen_width,0,
        #                                                         self.screen_width,self.vignette_rect.bottom()-(self.vignette.height/2)+(self.Player_Sprite.height/2),
        #                                                         0, self.vignette_rect.bottom()-(self.vignette.height/2)+(self.Player_Sprite.height/2)]), ('c3B', (0,0,0 ,0,0,0 ,0,0,0 ,0,0,0)))
        #     self.TAIL.set_alpha(fade_amounts[index])
        #     finalImage = self.TAIL.copy()
        #     try: finalImage = pygame.transform.scale(finalImage, (size_amounts[index], size_amounts[index]))
        #     except: passsa
        self.TRAIL_BATCH.draw()
        self.RIGHT_BOTTOM_BATCH.draw()
        self.RIGHT_TOP_BATCH.draw()
        self.LEFT_TOP_BATCH.draw()
        self.LEFT_BOTTOM_BATCH.draw()
        # self.TOP_BATCH.draw()
        # self.BOTTOM_BATCH.draw()
        # self.RIGHT_BATCH.draw()
        # self.LEFT_BATCH.draw()
        self.RAYS_BATCH.draw()

        # TOP
        if self.SHOW_VIGNETEE:
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [0, 0,
                                                                 self.screen_width, 0,
                                                                 self.screen_width, self.vignette_rect.bottom()-(self.vignette.height/2)
                                                                 + (self.Player_Sprite.height/2),
                                                                 0, self.vignette_rect.bottom()-(self.vignette.height/2)+(self.Player_Sprite.height/2)]), ('c3B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))

            # BOTTOM
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [0, self.screen_height,
                                                                 self.screen_width, self.screen_height,
                                                                 self.screen_width, self.vignette_rect.top()-(self.vignette.height/2)
                                                                 - (self.Player_Sprite.height/2),
                                                                 0, self.vignette_rect.top()-(self.vignette.height/2)-(self.Player_Sprite.height/2)]), ('c3B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))

            # LEFT
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [0, self.vignette_rect.top()-(self.vignette.height/2)+(self.Player_Sprite.height/2),
                                                                 self.vignette_rect.left()-(self.vignette.width/2)+(self.Player_Sprite.width
                                                                                                                    / 2), self.vignette_rect.bottom()+(self.vignette.height/2)+(self.Player_Sprite.height/2),
                                                                 self.vignette_rect.left()-(self.vignette.width/2)+(self.Player_Sprite.width
                                                                                                                    / 2), self.vignette_rect.bottom()-(self.vignette.height/2)+(self.Player_Sprite.height/2),
                                                                 0, self.vignette_rect.bottom()-(self.vignette.height/2)+(self.Player_Sprite.height/2)]), ('c3B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))
            # RIGHT
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [self.screen_width, self.vignette_rect.top()-(self.vignette.height/2)+(self.Player_Sprite.height/2),
                                                                 self.vignette_rect.right()-(self.vignette.width/2)-(self.Player_Sprite.width
                                                                                                                     / 2), self.vignette_rect.bottom()+(self.vignette.height/2)+(self.Player_Sprite.height/2),
                                                                 self.vignette_rect.right()-(self.vignette.width/2)-(self.Player_Sprite.width
                                                                                                                     / 2), self.vignette_rect.bottom()-(self.vignette.height/2)+(self.Player_Sprite.height/2),
                                                                 self.screen_width, self.vignette_rect.bottom()-(self.vignette.height/2)+(self.Player_Sprite.height/2)]), ('c3B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))

            self.vignette.draw()
        self.Player_Sprite.draw()

        self.TEXT_BATCH = pyglet.graphics.Batch()  # RESET TEXT GRAPHICS
        if self.finishX * self.width <= 200 and self.finishY * self.width < 260:
            if self.vignette_rect.x >= self.screen_width-200 and self.vignette_rect.y <= 260:
                self.draw_bars((10, -110, 30, 120), (255, 255, 255), self.PLAYER_COLOR,
                               50, self.SPEED_BOOST_DURATION, self.MAX_SPEED_DURATION, 'BOOST')
                self.draw_bars((50, -110, 30, 120), (255, 255, 255),
                               (255, 75, 75), 50, self.health, self.MAX_HEALTH, 'HEALTH')
            else:
                self.draw_bars((self.screen_width-80, -110, 30, 120), (255, 255, 255),
                               self.PLAYER_COLOR, 50, self.SPEED_BOOST_DURATION, self.MAX_SPEED_DURATION, 'BOOST')
                self.draw_bars((self.screen_width-40, -110, 30, 120), (255, 255, 255),
                               (255, 75, 75), 50, self.health, self.MAX_HEALTH, 'HEALTH')
        else:
            if self.vignette_rect.x <= 200 and self.vignette_rect.y <= 260:
                self.draw_bars((self.screen_width-80, -110, 30, 120), (255, 255, 255),
                               self.PLAYER_COLOR, 50, self.SPEED_BOOST_DURATION, self.MAX_SPEED_DURATION, 'BOOST')
                self.draw_bars((self.screen_width-40, -110, 30, 120), (255, 255, 255),
                               (255, 75, 75), 50, self.health, self.MAX_HEALTH, 'HEALTH')
            else:
                self.draw_bars((10, -110, 30, 120), (255, 255, 255), self.PLAYER_COLOR,
                               50, self.SPEED_BOOST_DURATION, self.MAX_SPEED_DURATION, 'BOOST')
                self.draw_bars((50, -110, 30, 120), (255, 255, 255),
                               (255, 75, 75), 50, self.health, self.MAX_HEALTH, 'HEALTH')

        self.TEXT_BATCH.draw()
        self.RENDERED_TEXT = False
        # self.BARS_BATCH.draw()

    def draw_bars(self, rect, outline_color, fill_color, opacity, value, max_value, name, width=1):
        # pyglet.gl.glLineWidth(width)
        x, y, w, h = rect
        width = max(width, 1)  # Draw at least one rect.
        width = min(min(width, w//2), h//2)  # Don't overdraw.
        BAR_POSITON = (value/max_value)*h
        # pygame.gfxdraw.box(screen, pygame.Rect(x,y+BAR_POSITON+h-BAR_POSITON,w,h-(BAR_POSITON)-h), fill_color)# alpha level
        # pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', [x,y,
        #                                                      x,y+(BAR_POSITON)-h,
        #                                                      x+w,y+h-(BAR_POSITON)-h,
        #                                                      x,y+w]), ('c3B', (fill_color[0],fill_color[1],fill_color[2],fill_color[0],fill_color[1],fill_color[2], fill_color[0],fill_color[1],fill_color[2], fill_color[0],fill_color[1],fill_color[2])))
        bar = pyglet.shapes.Rectangle(
            x, y+BAR_POSITON+h-BAR_POSITON, w, h+(BAR_POSITON)-h, color=fill_color, batch=self.BARS_BATCH)

        # self.BARS_BATCH.add(4, gl.GL_LINES, None, ('v2f', (x,y ,x,y-h, x+w,y-h ,x+w,y)), ('c3B', (outline_color[0],outline_color[1],outline_color[2] , outline_color[0],outline_color[1],outline_color[2],outline_color[0],outline_color[1],outline_color[2] , outline_color[0],outline_color[1],outline_color[2])))
        line_left = pyglet.shapes.Line(
            x, y+h, x, y+h*2, width, color=outline_color, batch=self.BARS_BATCH)
        line_right = pyglet.shapes.Line(
            x+w, y+h, x+w, y+h*2, width, color=outline_color, batch=self.BARS_BATCH)
        line_top = pyglet.shapes.Line(
            x, y+h*2, x+w, y+h*2, width, color=outline_color, batch=self.BARS_BATCH)
        line_bottom = pyglet.shapes.Line(
            x, y+h, x+w, y+h, width, color=outline_color, batch=self.BARS_BATCH)
        # changing opacity of the rect1
        # opacity is visibility (0 = invisible, 255 means visible)
        bar.opacity = opacity
        bar.draw()
        self.BARS_BATCH.draw()

        # myfont = pygame.font.SysFont('arial.ttf', 22)
        if not self.RENDERED_TEXT:
            space = -15
            for letter in name:
                play_text = pyglet.text.Label(letter, font_name="Arial", font_size=11, x=x+14, y=y+h+h+space,
                                              anchor_x='center', anchor_y='center', color=(255, 255, 255, 255), batch=self.TEXT_BATCH)
                self.TEXT_LIST.append(play_text)
                # textsurface = myfont.render(letter, True, (255, 255, 255))
                # screen.blit(textsurface,(x+10,y+space))
                space -= 17
        self.TEXT_LIST.clear()
        # This draws several smaller outlines inside the first outline. Invert
        # the direction if it should grow outwards.
        # for i in range(width):
        #     pygame.gfxdraw.rectangle(screen, (x+i, y+i, w-i*2, h-i*2), outline_color)

    def get_fade_values(self, start, max_value, amount_of_numbers):
        # NOTE TYPES
        numbers = []
        try:
            step = (max_value - start) / (amount_of_numbers - 1)
        except ZeroDivisionError:
            step = (max_value - start) / amount_of_numbers
        for i in range(amount_of_numbers):
            # In this case we want to start at 1, to simplify things.
            i = i + 1
            if i == 1:
                numbers.append(int(start))  # first number
            elif i == 2:
                numbers.append(int(start + step))  # second number
            if 3 <= i < amount_of_numbers:
                # everything in between
                numbers.append(int(start + (i - 1) * step))
            if i == amount_of_numbers:
                numbers.append(
                    int(start + (amount_of_numbers - 1) * step))  # end
        return numbers

    # def rotate(self, w, a, s, d):
    #     if a:
    #         self.Player_Sprite.rotation = -90
    #     elif d:
    #         self.Player_Sprite.rotation = 90
    #     if w:
    #         if a:
    #             self.Player_Sprite.rotation = -45
    #         elif d:
    #             self.Player_Sprite.rotation = 45
    #         else:
    #             self.Player_Sprite.rotation = 0
    #     elif s:
    #         if a:
    #             self.Player_Sprite.rotation = -135
    #         elif d:
    #             self.Player_Sprite.rotation = 135
    #         else:
    #             self.Player_Sprite.rotation = 180
