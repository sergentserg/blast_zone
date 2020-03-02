from os import path
import xml.etree.ElementTree as ET
import pygame as pg

import src.config as cfg

class ImageLoader:
    def __init__(self, *spritesheets):
        """
        spritesheets is a list of dictionaries whose contents are:
        {'spritesheet': filename.png, 'xml' :filename.xml}.

        """

        self._spritesheets_data = []
        self._loaded_surfaces = {}
        for sheet in spritesheets:
            sheet_paths = {f_type: path.join(cfg.IMG_DIR, fn) for f_type, fn in sheet.items()}
            sheet_surface = pg.image.load(sheet_paths["spritesheet"]).convert_alpha()
            tree = ET.parse(sheet_paths["xml"])
            self._spritesheets_data.append({"surface": sheet_surface, "root": tree.getroot()})

    def get_image(self, fn):
        """ Returns image from preloads; creates it if DNE """
        # Check if loaded, and load it if not loaded.
        return self._loaded_surfaces.setdefault(fn, self._create_surface(fn))

    def _create_surface(self, filename):
        # Find the image and create a surface.
        for sheet_data in self._spritesheets_data:
            for node in sheet_data["root"]:
                if(node.attrib['name'] == filename):
                    data = node.attrib
                    rect = (int(data['x']), int(data['y']), int(data['width']), int(data['height']))
                    image = pg.Surface((rect[2], rect[3]))
                    image.blit(sheet_data["surface"], (0, 0), rect)
                    return image


_img_loader = ImageLoader(*cfg.SPRITESHEET_DATA)

get_image = _img_loader.get_image
