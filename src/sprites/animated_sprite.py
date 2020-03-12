from math import floor
from .spriteW import SpriteW
import src.utility.sprite_loader as sprite_loader
import src.config as cfg

class AnimatedSprite(SpriteW):
    def __init__(self, x, y, groups, images, frame_info):
        # Pass in default image
        SpriteW.__init__(self, x, y, images[0], groups)
        # Load all images
        self.images = [self.image]
        self.images.extend([sprite_loader.get_image(img) for img in images[1:]])
        for image in self.images:
            image.set_colorkey(cfg.BLACK)
        # Store animation data
        self.frame_info = frame_info
        # Animation 0 is the default
        self.change_anim(0)
        self.anim_fps = 24.0

    def update_anim(self, dt):
        # Update time in current frame of the animation
        self.frame_time += dt

        # Check if its time to update frame
        if self.frame_time > (1/self.anim_fps):
            self.current_frame += floor(self.frame_time * self.anim_fps)

            # Check if we reached final frame in animation
            if self.current_frame >= self.frame_info[self.anim_num]["num_frames"]:
                self._handle_last()
            # Update the active image
            self.image = self.images[self.current_frame]
            self.frame_time = self.frame_time % (1/self.anim_fps)

    def _handle_last():
        self.current_frame = self.current_frame % self.frame_info[self.anim_num]["num_frames"]

    def change_anim(self, num):
        self.anim_num = num
        self.current_frame = 0
        self.frame_time = 0.0
        img_num = self.frame_info[self.anim_num]["start_frame"]
        self.image = self.images[img_num]
