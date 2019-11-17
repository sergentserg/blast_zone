from item import Item

class AmmoItem(Item):
    def __init__(self, x, y, filename):
        Item.__init__(self, x, y, filename):
