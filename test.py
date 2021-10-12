import random
import pygame
pygame.init()

WHITE = (255,255,255)
GREY = (20,20,20)
BLACK = (0,0,0)
PURPLE = (100,0,100)
RED = (255,0,0)

size = (500,500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Maze Generator")

done = False

clock = pygame.time.Clock()

width = 45
cols = int(size[0] / width)
rows = int(size[1] / width)

stack = []

pos = (0,0)
class Player(pygame.sprite.Sprite):
    def __init__(self, image, overlay, pos):
        super().__init__()
        self.image = image
        self.pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.vignette = overlay
        self.rect_overlay = self.vignette.get_rect()
        self.smooth_time = 5
        self.time = 0
        
    def update(self, events, dt):
        def lerp(a, b, f):
            return a + f * (b - a)
        pressed = pygame.key.get_pressed()
        move = pygame.Vector2((0, 0))
        if pressed[pygame.K_w]: 
            self.time += 0.01
            move += (0, -1)
        else: self.time = 0
        if pressed[pygame.K_a]: 
            move += (-1, 0)
        if pressed[pygame.K_s]: 
            move += (0, 1)
        if pressed[pygame.K_d]: 
            move += (1, 0)
        
        if self.time > self.smooth_time:
            self.pos = self.pos + move * lerp(0, self.smooth_time, dt/5) *  1.3
        else:
            self.pos = self.pos + move * lerp(0, self.time, dt/5)* 1.3
        self.rect.center = self.pos      
        self.rect_overlay.center = self.pos  
        #if move.length() > 0: move.normalise_ip()
    def draw(self):
        # pimg = pygame.Surface((10, 10), pygame.SRCALPHA)
        pimg = pygame.rect.Rect(self.pos, (10, 10))
        # alpha_img = pygame.Surface(pimg.get_size(), pygame.SRCALPHA)
        # alpha_img.fill((255, 255, 255, 140))
        # pimg.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        # pimg.fill((200, 20, 20))
        overlay = pygame.image.load("vignette.png")
        overlay = pygame.transform.scale(overlay, (500, 500))
        pygame.draw.rect(screen, GREY, pimg)
        # pygame.draw(screen, GREY, overlay)
        screen.blit(self.vignette, (self.rect_overlay.x, self.rect_overlay.y))

def load_background(filename=None):
    name = filename if filename else "vignette.png"
    background = pygame.image.load(name)
    background = pygame.transform.rotate(background, -90)
    background = pygame.transform.scale(background, (800,600))
    return background

def load_player():
    pimg = pygame.Surface((10, 10), pygame.SRCALPHA)
    alpha_img = pygame.Surface(pimg.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, 140))
    pimg.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    pimg.fill((200, 20, 20))
    overlay = pygame.image.load("vignette.png")
    # overlay = pygame.transform.scale(overlay, (500, 500))
    # Anti aliasing
    return Player(pimg, overlay, (25, 325))

class Cell():
    def __init__(self,x,y):
        global width
        self.x = x * width
        self.y = y * width

        self.visited = False
        self.current = False

        self.walls = [True,True,True,True] # top , right , bottom , left

        # neighbors
        self.neighbors = []

        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0

        self.next_cell = 0

    def draw(self):
        if self.current:
            pygame.draw.rect(screen,WHITE,(self.x,self.y,width,width))
        elif self.visited:
            pygame.draw.rect(screen,WHITE,(self.x,self.y,width,width))

            if self.walls[0]:
                pygame.draw.line(screen,WHITE,(self.x,self.y),((self.x + width),self.y),1) # top
            if self.walls[1]:
                pygame.draw.line(screen,WHITE,((self.x + width),self.y),((self.x + width),(self.y + width)),1) # right
            if self.walls[2]:
                pygame.draw.line(screen,WHITE,((self.x + width),(self.y + width)),(self.x,(self.y + width)),1) # bottom
            if self.walls[3]:
                pygame.draw.line(screen,WHITE,(self.x,(self.y + width)),(self.x,self.y),1) # left

    def checkNeighbors(self):
        print(f"Top; y: {str(int(self.y / width))} y - 1: {str(int(self.y / width) - 1)}")
        if int(self.y / width) >= 1:
            self.top = grid[int(self.y / width) - 1][int(self.x / width)]

        print(f"Right; x: {str(int(self.x / width))} x + 1: {str(int(self.x / width) + 1)}")
        if int(self.x / width) + 1 <= cols - 1:
            self.right = grid[int(self.y / width)][int(self.x / width) + 1]

        print(f"Bottom; y: {str(int(self.y / width))} y + 1: {str(int(self.y / width) + 1)}")
        if int(self.y / width) + 1 <= rows - 1:
            self.bottom = grid[int(self.y / width) + 1][int(self.x / width)]

        print(f"Left; x: {str(int(self.x / width))} x - 1: {str(int(self.x / width) - 1)}")
        if int(self.x / width) >= 1:
            self.left = grid[int(self.y / width)][int(self.x / width) - 1]
        print("--------------------")

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

        self.next_cell = self.neighbors[random.randrange(0,len(self.neighbors))]
        return self.next_cell

def removeWalls(current_cell,next_cell):
    x = int(current_cell.x / width) - int(next_cell.x / width)
    y = int(current_cell.y / width) - int(next_cell.y / width)
    if x == -1: # right of current
        current_cell.walls[1] = False
        next_cell.walls[3] = False
    elif x == 1: # left of current
        current_cell.walls[3] = False
        next_cell.walls[1] = False
    elif y == -1: # bottom of current
        current_cell.walls[2] = False
        next_cell.walls[0] = False
    elif y == 1: # top of current
        current_cell.walls[0] = False
        next_cell.walls[2] = False

grid = []

for y in range(rows):
    grid.append([])
    for x in range(cols):
        grid[y].append(Cell(x,y))

current_cell = grid[0][0]
next_cell = 0

# -------- Main Program Loop -----------
# -------- Main Program Loop -----------
def main():
    global current_cell, grid

    player = None
    initialized = False
    current_maze = None
    dt = 0
    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    if not initialized:
        #current_maze = 0
        player = load_player()
        sprites.add(player)
        initialized = True

    play = False
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if play:
            # pygame.draw.rect(screen, (164, 164, 255), player.rect) # Player trail
            sprites.update(None, dt) # Player trail
            # sprites.draw(screen) # Player trail
 
            screen.fill(WHITE)#Covers up everything with black
            player.draw()
            
            dt = clock.tick(360) # Higher the smoother, (basicly FPS)

            finished = pygame.Rect(0, 0, width, width).colliderect(player.rect)
            if finished:
                # init new grid
                grid = []
                for y in range(rows):
                    grid.append([])
                    for x in range(cols):
                        grid[y].append(Cell(x,y))
                current_cell = grid[0][0]
                # create new random player positon
                px = random.randint(0, rows-1) * width + width//2
                py = random.randint(0, cols-1) * width + width//2
                player.pos = pygame.Vector2(px, py)
                player.rect = player.image.get_rect(center=player.pos)
                # clear screen
                screen.fill(0)
                play = False

        else:
            current_cell.visited = True
            current_cell.current = True

            next_cell = current_cell.checkNeighbors()
            if next_cell != False:
                current_cell.neighbors = []
                stack.append(current_cell)
                removeWalls(current_cell,next_cell)
                current_cell.current = False
                current_cell = next_cell
            elif len(stack) > 0:
                current_cell.current = False
                current_cell = stack.pop()
            else:
                play = True

            for y in range(rows):
                for x in range(cols):
                    grid[y][x].draw()

        pygame.display.flip()


main()
pygame.quit()