from spriteW import SpriteW

class Item(SpriteW):
    __images = {...}
    def __init__(self, x, y, type):
        SpriteW.__init__(self, x, y, __images[type])
