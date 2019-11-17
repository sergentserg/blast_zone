from .animatedSprite import AnimatedSprite

class MuzzleFlash(AnimatedSprite):
    def __init__(self, x, y, filename):
        AnimatedSprite.__init__(self, x, y, filename):
