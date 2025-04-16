import pygame

class Gun:
    def __init__(self, player1, screen):
        self.image = pygame.image.load("arm.png").convert_alpha()
        self.screen = screen
        self.player1 = player1
        self.angle = 0
        self.rotation_speed = 5
        self.max_angle = 180
        self.need_fire = False

    def update_position(self):
        # Position of the shoulder (or wherever the arm connects)
        x_offset = 22
        y_offset = 45
        self.x = self.player1.x + x_offset
        self.y = self.player1.y +y_offset

    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.need_fire = True
            # Increase angle gradually until max_angle is reached
            if self.angle < self.max_angle:
                self.angle += self.rotation_speed
                self.angle = min(self.angle, self.max_angle)
        else:
            if self.need_fire:
                self.fire_bullet()
                self.need_fire = False

            # Reset arm angle to match player lean
            self.angle = self.player1.lean_angle

    def fire_bullet(self):
        pass

    def draw(self):
        pivot = [self.x, self.y]
        offset = pygame.math.Vector2(5, 15)

        rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1)  # Rotate the image.
        rotated_offset = offset.rotate(-self.angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        self.screen.blit(rotated_image, rect)

