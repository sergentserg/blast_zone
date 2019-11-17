from .barrel import Barrel

class DoubleBarrel(Barrel):
    def __init__(self, x, y, filename):
        Barrel.__init__(self, x, y, filename)
