from spriteW import SpriteW

class Bullet(SpriteW):
    def __init__(self, x, y, filename):
        SpriteW.__init__(self, x, y, filename):

bullet = Bullet(0, 0, "bulletDark2.png")
