
import pygame
import pygame.gfxdraw
class Main_Menu():
    def __init__(self, screen_size: tuple, screen, start_game, quit_game):
        super().__init__()
        # Functions that call back to main
        self.start_game = start_game
        self.quit_game = quit_game
        self.screen_width, self.screen_height = screen_size[0], screen_size[1]
        self.screen = screen
        events = pygame.event.get()
        sprites = pygame.sprite.Group()
        sprites.add(Button(
                        pygame.Color((110,220,110)), 
                        pygame.Color((50,200,50)), 
                        pygame.Rect((self.screen_width/2)-50, (self.screen_height/2.2), 100, 50), 
                        lambda b: self.Play(),
                        'Play',
                        pygame.Color('black')))

        sprites.add(Button(
                        pygame.Color((220,110,110)), 
                        pygame.Color((200,50,50)), 
                        pygame.Rect((self.screen_width/2)-50, (self.screen_height/1.7), 100, 50), 
                        lambda b: self.Quit(),
                        'Quit'))
        sprites.update(events)
        sprites.draw(self.screen)
        
    def Play(self):
        self.start_game()
        
    def Quit(self):
        self.quit_game()
        
class Button(pygame.sprite.Sprite):
    # 1) no need to have 4 parameters for position and size, use pygame.Rect instead
    # 2) let the Button itself handle which color it is
    # 3) give a callback function to the button so it can handle the click itself 
    def __init__(self, color, color_hover, rect, callback, text='', outline=None):
        super().__init__()
        self.text = text
        # a temporary Rect to store the size of the button
        tmp_rect = pygame.Rect(0, 0, *rect.size)

        # create two Surfaces here, one the normal state, and one for the hovering state
        # we create the Surfaces here once, so we can simple blit them and dont have
        # to render the text and outline again every frame
        self.org = self._create_image(color, outline, text, tmp_rect)
        self.hov = self._create_image(color_hover, outline, text, tmp_rect)

        # in Sprites, the image attribute holds the Surface to be displayed...
        self.image = self.org
        # ...and the rect holds the Rect that defines it position
        self.rect = rect
        self.callback = callback

    def _create_image(self, color, outline, text, rect):
        # function to create the actual surface
        # see how we can make use of Rect's virtual attributes like 'size'
        img = pygame.Surface(rect.size)
        font = pygame.font.SysFont('comicsans', 20)
        if outline:
            # here we can make good use of Rect's functions again
            # first, fill the Surface in the outline color
            # then fill a rectangular area in the actual color
            # 'inflate' is used to 'shrink' the rect
            img.fill(outline)
            img.fill(color, rect.inflate(-4, -4))
        else:
            img.fill(color)

        # render the text once here instead of every frame
        if text != '':
            text_surf = font.render(text, 1, pygame.Color('black'))
            # again, see how easy it is to center stuff using Rect's attributes like 'center'
            text_rect = text_surf.get_rect(center=rect.center)
            img.blit(text_surf, text_rect)
        return img

    def update(self, events):
        # here we handle all the logic of the Button
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        # if the mouse in inside the Rect (again, see how the Rect class
        # does all the calculation for use), use the 'hov' image instead of 'org'
        self.image = self.hov if hit else self.org
        for event in events:
            # the Button checks for events itself.
            # if this Button is clicked, it runs the callback function
            if event.type == pygame.MOUSEBUTTONDOWN and hit:
                self.callback(self)