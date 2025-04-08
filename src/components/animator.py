import pygame


class Frame:
    def __init__(self, frame, pos, frame_pos):
        self.world_pos = pos
        self.frame_pos = frame_pos
        self.image = frame
        self.rect = self.image.get_rect(center=self.world_pos)

    def set_pos(self, pos):
        self.world_pos = pos


class Animation:
    def __init__(
        self,
        spritesheet,
        sprite_size,
        rows,
        cols,
        duration,
        start_frame=1,
        end_frame=-1,
        world_pos=(0, 0),
    ):
        self.frame_count = 0
        self.frames = []  # cols * rows
        count = 0

        for y in range(0, rows):
            y_pos = y * sprite_size
            for x in range(0, cols):
                x_pos = x * sprite_size
                count += 1
                if end_frame == -1:
                    if count >= start_frame:
                        frame = pygame.Surface.subsurface(
                            spritesheet, (x_pos, y_pos, sprite_size, sprite_size)
                        )
                        self.frames.append(Frame(frame, world_pos, (x_pos, y_pos)))
                else:
                    if count >= start_frame and count <= end_frame:
                        frame = pygame.Surface.subsurface(
                            spritesheet, (x_pos, y_pos, sprite_size, sprite_size)
                        )
                        self.frames.append(Frame(frame, world_pos, (x_pos, y_pos)))

        self.max_duration = duration // self.length()
        self.duration = self.max_duration

    def length(self):
        return len(self.frames)

    def set_duration(self, new_dur):
        self.max_duration = new_dur // self.length()

    def get_frame(self, idx):
        if idx >= self.length() or idx < 0:
            raise IndexError(f"Animation frame: {idx} is not found")
        return self.frames[idx]

    def get_current_frame(self):
        return self.get_frame(self.frame_count)

    def update(self):
        if self.duration > 0:
            self.duration -= 1
        else:
            self.frame_count = (self.frame_count + 1) % self.length()
            self.duration = self.max_duration

    def draw(self, screen):
        frame = self.get_frame(self.frame_count)
        screen.blit(frame.image, frame.rect)

    def _debug_print(self):
        print("frame_count:", self.frame_count)
        print("frames: ", self.length())
        for frame in self.frames:
            print("\t", frame.frame_pos)


class Animator:
    def __init__(self, sp_file, sprite_size, rows, cols, pos):
        self.sprite_sheet = pygame.image.load(sp_file).convert_alpha()
        self.sprite_size = sprite_size
        self.rows = rows
        self.cols = cols
        self.world_pos = pos
        self.animations = {}
        self.current_animation = None

    def add(self, name, duration, start_frame=1, end_frame=-1):
        self.animations[name] = Animation(
            self.sprite_sheet,
            self.sprite_size,
            self.rows,
            self.cols,
            duration,
            start_frame,
            end_frame,
            self.world_pos,
        )

    def play(self, name):
        if self.current_animation is not None:
            if (
                self.current_animation.frame_count
                == self.current_animation.length() - 1
            ):
                self.current_animation = self.animations.get(name)
                self.current_animation.frame_count = 0
        else:
            self.current_animation = self.animations.get(name)
            if self.current_animation is None:
                raise IndexError(f"Animator::play({name}): could not find animation")

    def update(self):
        if self.current_animation is not None:
            self.current_animation.update()

    def draw(self, screen):
        if self.current_animation is not None:
            self.current_animation.draw(screen)

    def get_frame(self):
        if self.current_animation is not None:
            return self.current_animation.get_current_frame()
