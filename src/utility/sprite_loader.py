from os import path
import xml.etree.ElementTree as ET
import pygame as pg

# from src.settings import GAME_DIR
import src.config as cfg

class ImageLoader:
    def __init__(self):
        """
        file_data = {"spritesheet": "file_name","xml": "file_name", "preloads": "file_name"}

        """
        # assets
        objects_data = {
                    "spritesheet": "onlyObjects_default.png",
                    "xml": "onlyObjects_default.xml",
                    "preloads": "preloads.xml"}
        ui_data = {
                    "spritesheet": "blueSheet.png",
                    "xml": "blueSheet.xml",
                    "preloads": ''}

        # img_dir = path.join(GAME_DIR, 'img')
        self.spritesheets_data = {'objs': {}, 'ui': {}}

        # Initialize game objects spritesheet
        objects_dir = path.join(cfg.IMG_DIR, 'object_spsheet')
        obj_img_paths = {key: path.join(objects_dir, objects_data[key]) for key in objects_data}
        self._init_spritesheet(obj_img_paths, self.spritesheets_data['objs'])

        #Initialize UI spritesheet
        ui_dir = path.join(cfg.IMG_DIR, 'ui_spsheet')
        ui_img_paths = {key: path.join(ui_dir, ui_data[key]) for key in ui_data}
        self._init_spritesheet(ui_img_paths, self.spritesheets_data['ui'])

    def get_image(self, fn):
        """ Returns image from preloads; creates it if DNE """
        # Check if image exists in object spritesheet
        objs_dict = self.spritesheets_data['objs']
        img = objs_dict['preloads'].get(fn, self._create_surface(fn, objs_dict))

        #return if found
        if img:
            return img
        else:
        # If didn't find, check UI spritesheet
            ui_dict = self.spritesheets_data['ui']
            return ui_dict['preloads'].get(fn, self._create_surface(fn, ui_dict))

    def _create_surface(self, filename, spritesheet_data):
        spritesheet = spritesheet_data["spritesheet"]
        root = spritesheet_data["root"]
        for node in root:
            if(node.attrib['name'] == filename):
                data = node.attrib
                rect = (int(data['x']), int(data['y']), int(data['width']), int(data['height']))
                image = pg.Surface((rect[2], rect[3]))
                image.blit(spritesheet, (0, 0), rect)
                return image

    def _init_spritesheet(self, paths, spritesheet_data):
        # Save spritesheet PNG
        spritesheet_data["spritesheet"] = pg.image.load(paths["spritesheet"]).convert_alpha()

        # Save the spritesheet XML root
        tree = ET.parse(paths["xml"])
        spritesheet_data["root"] = tree.getroot()

        # Save the preloads
        spritesheet_data["preloads"] = {}
        if not (path.basename(paths["preloads"]) == ''):
            self._preload_surfaces(paths["preloads"], spritesheet_data)

    def _preload_surfaces(self, preload_file, spritesheet_data):
        # xml tree of preload surface nodes
        tree = ET.parse(preload_file)
        preload_root = tree.getroot()
        for node in preload_root:
            # render the image
            fn = node.attrib['name']
            spritesheet_data['preloads'][fn] = self._create_surface(fn, spritesheet_data)

            #delete corresponding tree node
            for texture in spritesheet_data['root']:
                if(texture.attrib['name'] == fn):
                    spritesheet_data['root'].remove(texture)

_img_loader = ImageLoader()

get_image = _img_loader.get_image
