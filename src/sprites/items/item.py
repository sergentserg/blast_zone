from .spriteW import SpriteW

class Item(SpriteW):
    def __init__(self, x, y, filename):
        SpriteW.__init__(self, x, y, filename):
