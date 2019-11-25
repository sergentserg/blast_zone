from .spriteW import SpriteW
from src.utility.sprite_loader import img_loader

class AnimatedSprite(SpriteW):
    def __init__(self, x, y, images):
        SpriteW.__init__(self, x, y, images[0])
        self.images = [self.img]
        # Append the other frames
        self.images.extend([img_loader.get_image(img) for img in images[1:]])
        self.num_frames = len(self.images)
        self.past_frame = 0
        self.current_frame = 0
        self.anim_fps = 24.0
        self.frame_time = 0.0
        # If false, sprite killed at end of last frame
        self.is_loopable = True

    def update_anim(self, dt):
        print("current_frame is: ", self.current_frame)
        # print("dt is: ", dt)
        # Update how long we've been in current frame
        self.frame_time += dt
        print("frame time is: ", self.frame_time)
        # print("The current frame is : ", self.current_frame)
        # print("The current frame time : ", self.frame_time)

        # Check if its time to update frame
        if self.frame_time > (1/self.anim_fps):
            # print("Update time...")
            self.current_frame += int(self.frame_time * self.anim_fps)
            # Check if we reached final frame in animation
            if self.current_frame >= self.num_frames:
                self.past_frame = self.current_frame
                self.current_frame = self.current_frame % self.num_frames
            # else:
            #     self.kill()
            #     return
            self.img = self.images[self.current_frame]
            self.frame_time = self.frame_time % (1/self.anim_fps)
            # print("Resetting frame time...: ", self.frame_time)
