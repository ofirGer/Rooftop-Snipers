import pygame


class Gun:
    def __init__(self, player1, screen):
        self.image = pygame.image.load("assets/arm.png").convert_alpha()

        self.bullet_frames = [pygame.image.load(f"assets/bullets/bullet{i}.png").convert_alpha() for i in range(1, 7)]
        self.bullet_angle = 0

        self.screen = screen
        self.player1 = player1
        self.angle = 0
        self.rotation_speed = 5
        self.max_angle = 180
        self.need_fire = False

        self.firing = False
        self.current_bullet_frame = 0
        self.bullet_timer = 0
        self.bullet_frame_delay = 5

        self.returning_to_normal = False
        self.return_speed = 5

    def update_position(self):
        x_offset = 22
        y_offset = 45
        self.x = self.player1.x + x_offset
        self.y = self.player1.y + y_offset

    def shoot(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            if self.returning_to_normal:
                # Snap instantly to 0 if firing while returning
                self.angle = 0
                self.returning_to_normal = False

            self.need_fire = True
            if self.angle < self.max_angle:
                self.angle += self.rotation_speed
                self.angle = min(self.angle, self.max_angle)
        else:
            if self.need_fire:
                self.start_bullet_animation()
                self.need_fire = False
                self.returning_to_normal = True  # Start returning after firing

            if self.returning_to_normal:
                # Smoothly return to lean angle
                target_angle = self.player1.lean_angle
                if self.angle < target_angle:
                    self.angle += self.return_speed
                    if self.angle > target_angle:
                        self.angle = target_angle
                        self.returning_to_normal = False
                elif self.angle > target_angle:
                    self.angle -= self.return_speed
                    if self.angle < target_angle:
                        self.angle = target_angle
                        self.returning_to_normal = False
            else:
                # Not returning: always match the player's lean!
                self.angle = self.player1.lean_angle

    def start_bullet_animation(self):
        self.firing = True
        self.current_bullet_frame = 0
        self.bullet_timer = 0
        self.bullet_angle = self.angle

    def update_bullet_animation(self):
        if self.firing:
            self.bullet_timer += 1
            if self.bullet_timer >= self.bullet_frame_delay:
                self.bullet_timer = 0
                self.current_bullet_frame += 1
                if self.current_bullet_frame >= len(self.bullet_frames):
                    self.firing = False

    def draw_bullet(self):
        if self.firing:
            frame = self.bullet_frames[self.current_bullet_frame]
            pivot = [self.x, self.y]
            offset = pygame.math.Vector2(198, 390)

            rotated_frame = pygame.transform.rotozoom(frame, self.bullet_angle, 1)
            rotated_offset = offset.rotate(-self.bullet_angle)
            rect = rotated_frame.get_rect(center=pivot + rotated_offset)
            self.screen.blit(rotated_frame, rect)

    def draw(self):
        self.draw_bullet()

        pivot = [self.x, self.y]
        offset = pygame.math.Vector2(5, 15)

        rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1)
        rotated_offset = offset.rotate(-self.angle)
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        self.screen.blit(rotated_image, rect)

    def apply_gun_movement(self):
        self.update_position()
        self.shoot()
        self.update_bullet_animation()

    def get_data(self):
        return {
            'angle': self.angle,
            'firing': self.firing,
            'bullet_frame': self.current_bullet_frame
        }