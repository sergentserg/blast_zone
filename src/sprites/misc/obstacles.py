from src.sprites.spriteW import SpriteW
import src.config as cfg

class Tree(SpriteW):
    image = 'treeGreen_small.png'
    def __init__(self, x, y, groups):
        SpriteW.__init__(self, x, y, Tree.image, groups)
        self._layer = cfg.ITEM_LAYER
