self.imagefrom math import floor
from .spriteW import SpriteW
from src.utility.sprite_loader import img_loader

class AnimatedSprite(SpriteW):
    def __init__(self, x, y, img_files, frame_info):
        SpriteW.__init__(self, x, y, img_files[0])
        # Load all images
        self.images = [self.image]
        self.images.extend([img_loader.get_image(img) for img in img_files[1:]])
        # Store animation data
        self.frame_info = [{"start_frame": data[0], "num_frames": data[1]} for data in frame_info]
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
            if self.current_frame >= self.num_frames:
                self.current_frame = self.current_frame % self.num_frames

            # Update the active image
            self.image = self.images[self.current_frame]
            self.frame_time = self.frame_time % (1/self.anim_fps)

    def change_anim(self, num):
        self.anim_num = num
        self.current_frame = 0
        self.frame_time = 0.0
        img_num = self.frame_info[self.anim_num]["start_frame"]
        self.image = self.images[img_num]
