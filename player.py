import pygame
import config


class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/player.png")
        self.width, self.height = self.image.get_size()
        self.x = x
        self.y = y - self.height  # Adjust to sit on the roof
        self.vel_y = 0
        self.vel_x = 0  # Horizontal velocity
        self.gravity = 1
        self.jump_strength = -18
        self.on_ground = True

        # Leaning mechanics
        self.lean_angle = 0  # Starts upright
        self.lean_speed = 0  # Initial lean speed
        self.lean_direction = 1  # 1 = right, -1 = left
        self.max_lean = 50  # Max tilt angle
        self.change_max_angle = False

    def jump(self):
        """Make the player jump if on the ground and lean direction is considered."""
        if self.on_ground:
            # Apply horizontal jump direction based on lean angle
            jump_direction = -1 if self.lean_angle > 0 else 1
            self.vel_y = self.jump_strength
            self.vel_x = jump_direction * abs(self.lean_angle) * 0.2  # Horizontal movement smoothened
            self.on_ground = False
            # reset leaning
            self.max_lean = abs(self.lean_angle) + 30
            if self.lean_angle == 0:
                self.lean_speed = 1
            else:
                self.lean_speed = abs(self.lean_angle) * 0.15  # Initial lean speed

            self.change_max_angle = False

    def apply_gravity(self):
        """Applies gravity and checks for roof collision."""
        self.vel_y += self.gravity
        self.y += self.vel_y

        # Check if player lands on the roof
        if self.y + self.height >= config.ROOF_Y and config.ROOF_X <= self.x <= config.ROOF_X + config.ROOF_WIDTH - self.width:
            self.y = config.ROOF_Y - self.height  # Place player on top of the roof
            self.vel_y = 0

            # If the player lands from a jump, reset leaning

            self.on_ground = True
            self.vel_x = 0  # Reset horizontal velocity to stop sliding

    def lean_and_move(self):
        if self.change_max_angle and abs(self.lean_angle) < 10:
            self.max_lean *= 0.8
            self.change_max_angle = False

        if self.on_ground:
            if self.max_lean < 7:
                self.lean_angle = 0
                self.lean_speed = 0

            # Lean back and forth until slowing down
            self.lean_angle += self.lean_speed * self.lean_direction

            # If leaning too much, switch direction

            if abs(self.lean_angle) >= self.max_lean:
                self.lean_angle = (self.max_lean) * self.lean_direction
                self.lean_direction *= -1  # Reverse direction
                self.lean_speed = max(self.lean_speed * 0.75, 0.5)
                self.change_max_angle = True

    def update_position(self):
        """Update the player's position with smooth horizontal movement."""
        self.x += self.vel_x

    def draw(self, screen):
        """Draw the player on the screen."""
        rotated_image = pygame.transform.rotate(self.image, self.lean_angle)
        image_rect = rotated_image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(rotated_image, image_rect.topleft)

    def apply_movement(self):
        self.apply_gravity()
        self.lean_and_move()  # Leaning movement
        self.update_position()  # Apply smooth horizontal movement

    def get_data(self):
        return {
            "x": self.x,
            "y": self.y,
            "lean_angle": self.lean_angle,
        }