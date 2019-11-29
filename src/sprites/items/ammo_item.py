from item import Item

class AmmoItem(Item):
    def __init__(self, x, y, filename):
        image_file = "speed_item.png"
        Item.__init__(self, x, y, filename):
