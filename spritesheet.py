import xml.etree.ElementTree as ET
import pygame as pg
from os import path

pg.init()

cur_dir_name = path.dirname(__file__)
img_dir = path.join(cur_dir_name, 'img')
tree = ET.parse(path.join(img_dir, 'onlyObjects_default.xml'))
root = tree.getroot()
spritesheet = pg.image.load(path.join(img_dir, 'onlyObjects_default.png'))


def get_image(filename):
    for texture in root:
        if(texture.attrib['name'] == filename):
            print("Found it!")
            data = texture.attrib
            rect = [data['x'], data['y'], data['width'], data['height']]
            for i in range(len(rect)):
                rect[i] = int(rect[i])

            print(rect)
            image = pg.Surface((rect[2], rect[3]))
            image.blit(spritesheet, (0, 0), tuple(rect))
            #blit(src, dest, Rectangle)
            print(image)
            return image
            # Load the image or whatever.
    print("We didn't find shit son, looked in " + img_dir)

get_image("barricadeMetal.png")
