import pyglet

#! YO DUDE TABNINE AUTOCOMPLETED MOST OF THIS SHIT ITS SMARTER THAN ME LMAO

# NOTE if something is missing ask me
class Rect():
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.texture = texture
    
    def update(self,x ,y):
        self.x = x
        self.y = y 
    
    def top(self):
        return self.y + self.texture.height
    
    def bottom(self):
        return self.y
    
    def right(self):
        return self.x + self.texture.width
    
    def left(self):
        return self.x
    
    def topRight(self):
        return (self.x + self.texture.width/2, self.y - self.texture.height/2)
    
    def topLeft(self):
        return (self.x - self.texture.width/2, self.y - self.texture.height/2)
    
    def bottomRight(self):
        return (self.x + self.texture.width/2, self.y + self.texture.height/2)
    
    def bottomLeft(self):
        return (self.x - self.texture.width/2, self.y + self.texture.height/2)
    
    def centerx(self):
        return self.x + (self.texture.width//2)

    def centery(self):
        return self.y + (self.texture.height//2)

    def collidesWith(self, otherRect):
        return (
            otherRect.right() >= self.left() or otherRect.left() <= self.right()
        ) and (
            otherRect.bottom() >= self.bottom() or otherRect.top() <= self.top()
        )