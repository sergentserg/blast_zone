import pygame as pg
from os import path
import xml.etree.ElementTree as ET

# 1) Create spritesheet loader within game class?

class ImageLoader:
    """ Spritesheet wrapper class, supports surface creation given a filename.
        args: spritesheet_data = {
                "spritesheet":"fn.png",
                "texture_data": "fn.xml",
                "preloads":"preloads.xml"
                }

    """
    # default spritesheet
    __kenney_textures = {"spritesheet": "onlyObjects_default.png",
                    "texture_data": "onlyObjects_default.xml",
                    "preloads": "preloads.xml"}

    # initialize member variables
    def __init__(self, spritesheet_data = __kenney_textures):
        img_dir = path.dirname(__file__)
        # Spritesheet with surfaces
        self.__spritesheet = pg.image.load(path.join(img_dir,spritesheet_data["spritesheet"])).convert_alpha()

        # Tree with data about each spritesheet texture
        tree = ET.parse(path.join(img_dir, spritesheet_data["texture_data"]))
        self.__root = tree.getroot()

        # Dictionary of surfaces to pre-create upon loading the game
        self.__preloads = {}
        self.__preload_surfaces(path.join(img_dir, spritesheet_data["preloads"]))

    def get_image(self, filename):
        """ get_image(filename): Returns 2D pygame surface corresponding to
            filename from a loaded spritesheet created on the fly,

        """
        return self.__preloads.get(filename, self.__create_surface(filename))

    def __create_surface(self, filename):
        """ create_surface(filename): Creates a 2D pygame surface corresponding
            to filename from a loaded spritesheet
        """
        for node in self.__root:
            if(node.attrib['name'] == filename):
                data = node.attrib
                rect = (int(data['x']), int(data['y']), int(data['width']), int(data['height']))
                image = pg.Surface((rect[2], rect[3]))
                image.blit(self.__spritesheet, (0, 0), rect)
                return image

    def __preload_surfaces(self, preload_file):
        """ preload_surfaces(preload_file): Creates regularly used surfaces
            from a given preload XML file, and stores them in a dict

        """
        # Go through tree of preload surfaces
        tree = ET.parse(preload_file)
        preload_root = tree.getroot()
        for node in preload_root:
            # prerender the image
            filename = node.attrib['name']
            self.__preloads[filename] = self.__create_surface(filename)

            #delete corresponding tree node
            # self.root.remove(node)
            for texture in self.__root:
                if(texture.attrib['name'] == filename):
                    self.__root.remove(texture)

img_loader = ImageLoader()
