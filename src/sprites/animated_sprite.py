from .spriteW import SpriteW
from src.utility.sprite_loader import img_loader

class AnimatedSprite(SpriteW):
    def __init__(self, x, y, images):
        SpriteW.__init__(self, x, y, images[0])
        self.images = [self.img]
        # Append the other frames
        self.images.extend([img_loader.get_image(img) for img in images[1:]])
        self.num_frames = len(self.images)
        self.current_frame = 0
        self.anim_fps = None
        self.frame_time = None
        # If false, sprite killed at end of last frame
        self.is_loopable = None

    def update_anim(self, dt):
        print("Update animation!")
