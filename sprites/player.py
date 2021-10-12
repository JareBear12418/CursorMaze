import pygame
import pygame.gfxdraw


BLACK = (0,0,0)



class Player(pygame.sprite.Sprite):
    def __init__(self, image, player_color, overlay, pos, width, show_vignete):
        super().__init__()
        self.width = width
        self.image = image
        self.PLAYER_COLOR = player_color
        self.pos = pygame.Vector2(pos)
        self.vignette = overlay
        self.vignette_rect = self.vignette.get_rect(center=self.pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.SHAPE: str = 'CIRCLE' #! 'SQAURE' OR 'CIRCLE'
        self.SHOW_VIGNETEE: bool = show_vignete
        self.smooth_time: float = 1
        self.time: float = 0
        self.TRAIL_POSTITIONS: list = []
        self.TRAIL_MAX_LENGTH: int = 150
        self.TRAIL_IMAGE = pygame.image.load("./assets/circle.png").convert_alpha()
        self.TAIL = self.LOAD_TRAIL(self.TRAIL_IMAGE, self.PLAYER_COLOR)
        self.IS_MOVING: bool = False
        self.SPEED_BOOST: float = 1.05
        self.SPEED_BOOST_DURATION: float = 10
        self.MAX_SPEED_DURATION: float = 10
        self.health = 5
        self.MAX_HEALTH = 5
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        
    def change_debugging_mode(self, dev_mode, maze_col):
        # NOTE DEBUGGING OR DEVELOPMENT ONLY
        self.DEVELOPER_MODE: bool = dev_mode
        self.ENABLE_MAZE_GOL: bool = maze_col

    def reset(self):
        self.health = self.MAX_HEALTH
        self.SPEED_BOOST_DURATION = self.MAX_SPEED_DURATION
        self.TRAIL_POSTITIONS.clear()
        
    def update(self, events, dt, cols, rows, grid):
        def lerp(a, b, f):
            return a + f * (b - a)

        pressed = pygame.key.get_pressed()
        move = pygame.Vector2((0, 0))

        # calculate maximum movement and current cell position  
        testdist = dt // 5 + 1 # distance from the wall
        cell_X = self.rect.centerx // self.width
        selfcell_Y = self.rect.centery // self.width
        min_X = self.rect.left // self.width
        max_X = self.rect.right // self.width
        min_Y = self.rect.top // self.width
        max_Y = self.rect.bottom // self.width
        # print(f'cell_X: {cell_X} | cell_Y: {cell_Y}\tmin_X: {min_X}, max_X: {max_X}, min_Y: {min_Y}, max_Y: {max_Y}')
        # test move up
        if not self.ENABLE_MAZE_GOL:
            if pressed[pygame.K_w]: 
                self.time += 0.03
                move += (0, -1)
            elif pressed[pygame.K_s]: 
                self.time += 0.03
                move += (0, 1)     
            if pressed[pygame.K_d]: 
                self.time += 0.03
                move += (1, 0)       
            elif pressed[pygame.K_a]: 
                self.time += 0.03
                move += (-1, 0)
        else:
            if pressed[pygame.K_w]:
            # if min_X == max_X and pressed[pygame.K_w]:
                self.time += 0.03
                next_Y = (self.rect.top-testdist) // self.width
                if cell_Y == next_Y or (next_Y >= 0 and not grid[cell_Y][cell_X].walls[0]):
                    move += (0, -1)
            # test move down
            elif pressed[pygame.K_s]:
            # elif min_X == max_X and pressed[pygame.K_s]:
                self.time += 0.03
                next_Y = (self.rect.bottom+testdist) // self.width
                if cell_Y == next_Y or (next_Y < rows and not grid[cell_Y][cell_X].walls[2]):
                    move += (0, 1)            
            # test move right
            if pressed[pygame.K_d]:
            # if min_Y == max_Y and pressed[pygame.K_d]:
                self.time += 0.03
                next_X = (self.rect.right+testdist) // self.width
                if cell_X == next_X or (next_X < cols and not grid[cell_Y][cell_X].walls[1]):
                    move += (1, 0)
            # test move left
            elif pressed[pygame.K_a]:
            # elif  min_Y > (max_Y-1) and  min_Y < (max_Y+1) and pressed[pygame.K_a]:
                self.time += 0.03
                next_X = (self.rect.left-testdist) // self.width
                if cell_X == next_X or (next_X >= 0 and not grid[cell_Y][cell_X].walls[3]):
                    move += (-1, 0)
                
        if not pressed[pygame.K_w] and not pressed[pygame.K_a]and not pressed[pygame.K_s]and not pressed[pygame.K_d]:
            self.IS_MOVING = False
        else: self.IS_MOVING = True
        
        # Smooth starting movement
        if self.time >= self.smooth_time: 
            self.pos = self.pos + move * lerp(0, self.smooth_time, dt/5)
            if pygame.key.get_mods() & pygame.KMOD_SHIFT: 
                if self.SPEED_BOOST_DURATION >= 0 and self.IS_MOVING: 
                    self.SPEED_BOOST_DURATION -= 0.03
                    self.pos = self.pos + move * lerp(0, self.SPEED_BOOST, dt/5)
        else: 
            self.pos = self.pos + move * lerp(0, self.time, dt/5)
        if not self.IS_MOVING and self.SPEED_BOOST_DURATION <= self.MAX_SPEED_DURATION: self.SPEED_BOOST_DURATION += 0.03
        self.rect.center = self.pos
        self.vignette_rect.center = self.pos  
        if len(self.TRAIL_POSTITIONS) >= self.TRAIL_MAX_LENGTH:
            if not self.IS_MOVING: self.TRAIL_POSTITIONS.append(self.pos)
            self.TRAIL_POSTITIONS.pop(0)
        else: self.TRAIL_POSTITIONS.append(self.pos)
        
    def draw(self, screen):
        fade_amounts = self.get_fade_values(0, 255, len(self.TRAIL_POSTITIONS))
        size_amounts = self.get_fade_values(0, 7, len(self.TRAIL_POSTITIONS)-(len(self.TRAIL_POSTITIONS)//2))
        for index, tail_pos in enumerate(self.TRAIL_POSTITIONS):
            self.TAIL.set_alpha(fade_amounts[index])
            finalImage = self.TAIL.copy()
            try: finalImage = pygame.transform.scale(finalImage, (size_amounts[index], size_amounts[index]))
            except: pass
            finalImage.blit(self.TAIL, (0, 0), special_flags = pygame.BLEND_MULT)
            screen.blit(finalImage, (tail_pos.x-3,tail_pos.y-3))
        pimg = pygame.rect.Rect((self.pos.x-3,self.pos.y-3, 11, 11))
        if self.SHAPE is 'SQUARE': pygame.draw.rect(screen, self.PLAYER_COLOR, pimg)
        elif self.SHAPE is 'CIRCLE': pygame.draw.circle(screen, self.PLAYER_COLOR, self.pos, 7)
        TOP_VIGNETTE = pygame.rect.Rect((0,0),(self.screen_width,self.vignette_rect.y))
        BOTTOM_VIGNETTE = pygame.rect.Rect((0,self.vignette_rect.y+self.vignette_rect.h),(self.screen_width,self.screen_height))
        
        LEFT_VIGNETTE = pygame.rect.Rect((0, self.vignette_rect.y),(self.vignette_rect.x, self.screen_height - (self.vignette_rect.y+self.vignette_rect.h)+self.vignette_rect.y-(self.vignette_rect.h/2)))
        RIGHT_VIGNETTE = pygame.rect.Rect((self.vignette_rect.x+self.vignette_rect.w,self.vignette_rect.y),(self.screen_width,self.screen_height - (self.vignette_rect.y+self.vignette_rect.h)+self.vignette_rect.y-(self.vignette_rect.h/2)))
        if self.SHOW_VIGNETEE:
            pygame.draw.rect(screen, BLACK, TOP_VIGNETTE)
            pygame.draw.rect(screen, BLACK, BOTTOM_VIGNETTE)
            pygame.draw.rect(screen, BLACK, LEFT_VIGNETTE)
            pygame.draw.rect(screen, BLACK, RIGHT_VIGNETTE)
            screen.blit(self.vignette, (self.vignette_rect.x, self.vignette_rect.y))
        colliding_with_GUI = pygame.Rect(0, self.screen_height-150, 90, 150).colliderect(self.rect)
        if colliding_with_GUI:
            self.draw_bars(screen, (self.screen_width-80, self.screen_height-130, 30, 120), (255, 255, 255, 127), (self.PLAYER_COLOR[0],self.PLAYER_COLOR[1],self.PLAYER_COLOR[2],127), self.SPEED_BOOST_DURATION, self.MAX_SPEED_DURATION, 'BOOST', 1) # Boost bar
            self.draw_bars(screen, (self.screen_width-40, self.screen_height-130, 30, 120), (255, 255, 255, 127), (255,75,75,127), self.health, self.MAX_HEALTH, 'HEALTH', 1) # health bar
        else:
            self.draw_bars(screen, (10, self.screen_height-130, 30, 120), (255, 255, 255, 127), (self.PLAYER_COLOR[0],self.PLAYER_COLOR[1],self.PLAYER_COLOR[2],127), self.SPEED_BOOST_DURATION, self.MAX_SPEED_DURATION, 'BOOST', 1) # Boost bar
            self.draw_bars(screen, (50, self.screen_height-130, 30, 120), (255, 255, 255, 127), (255,75,75,127), self.health, self.MAX_HEALTH, 'HEALTH', 1) # health bar
        
    def draw_bars(self, screen, rect, outline_color, fill_color, value, max_value, name, width=1):
        x, y, w, h = rect
        width = max(width, 1)  # Draw at least one rect.
        width = min(min(width, w//2), h//2)  # Don't overdraw.
        BAR_POSITON = (value/max_value)*h
        pygame.gfxdraw.box(screen, pygame.Rect(x,y+BAR_POSITON+h-BAR_POSITON,w,h-(BAR_POSITON)-h), fill_color)# alpha level
        myfont = pygame.font.SysFont('arial.ttf', 22)
        space = 12
        for letter in name:
            textsurface = myfont.render(letter, True, (255, 255, 255))
            screen.blit(textsurface,(x+10,y+space))
            space += 17
            
        # This draws several smaller outlines inside the first outline. Invert
        # the direction if it should grow outwards.
        for i in range(width):
            pygame.gfxdraw.rectangle(screen, (x+i, y+i, w-i*2, h-i*2), outline_color)
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
                numbers.append(int(start + (amount_of_numbers - 1) * step))  # end
        return numbers

    def LOAD_TRAIL(self, image, outline_color):
        colouredImage = pygame.Surface(image.get_size())
        colouredImage.fill(outline_color)
        finalImage = image.copy()
        finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
        return finalImage
    