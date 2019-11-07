import xml.etree.ElementTree as ET
import pygame as pg
from os import path

pg.init()

cur_dir_name = path.dirname(__file__)
img_dir = path.join(cur_dir_name, 'img')

class Spritesheet:
    def __init__(self, spritesheet_data):
        """ file_data is a dictionary with the spritesheet file,
        the xml for the spritesheet, and a preload XML/JSON
        file_data = {"spritesheet": "file_name", "xml": "file_name",
                        "preloads": "file_name"}
        """
        self.spritesheet = pg.image.load(path.join(img_dir, spritesheet_data["spritesheet"])).convert_alpha()
        tree = ET.parse(path.join(img_dir, spritesheet_data["xml"]))
        self.root = tree.getroot()
        self.preloads = {}
        self.preload_surfaces(spritesheet_data["preloads"])

    def get_image(self, filename):
        """ Returns image from preloads; creates it if DNE
        """

        return self.preloads.get(filename, self.create_surface(filename))

    def create_surface(self, filename):
        for node in self.root:
            if(node.attrib['name'] == filename):
                data = node.attrib
                rect = (int(data['x']), int(data['y']), int(data['width']), int(data['height']))
                image = pg.Surface((rect[2], rect[3]))
                image.blit(spritesheet, (0, 0), rect)
                return image

    def preload_surfaces(self, preload_file):
        # tree of preload surfaces
        tree = ET.parse(preload_file)
        preload_root = tree.getroot()
        for node in preload_root:
            # prerender the image
            filename = node.attrib['name']
            self.preloads[filename] = self.create_surface(filename)

            #delete corresponding tree node
            # self.root.remove(node)
            for texture in self.root:
                if(texture.attrib['name'] == filename):
                    self.root.remove(texture)

game_spritesheet = Spritesheet(spritesheet_data)
