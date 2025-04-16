import pygame, player, gun

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rooftop Snipers - Ofir G")

# Colors
BACKGROUND_COLOR = (135, 206, 235)  # Light blue sky
ROOF_COLOR = (0, 0, 0)  # Black for the roof

# Roof settings
ROOF_WIDTH = 700
ROOF_HEIGHT = HEIGHT // 3  # Height of the roof
ROOF_X = (WIDTH - ROOF_WIDTH) // 2
ROOF_Y = HEIGHT - ROOF_HEIGHT  # Position the roof at the bottom


def main():
    """Main game loop."""

    clock = pygame.time.Clock()
    player1 = player.Player(ROOF_X + 20, ROOF_Y)  # Player starts on the left side of the roof
    player_gun = gun.Gun(player1, screen)
    running = True
    while running:
        clock.tick(60)  # 60 FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                player1.jump()

        # Drawing
        screen.fill(BACKGROUND_COLOR)  # Sky
        pygame.draw.rect(screen, ROOF_COLOR, (ROOF_X, ROOF_Y, ROOF_WIDTH, ROOF_HEIGHT))  # Draw the roof
        # Game logic
        player1.apply_gravity()
        player1.lean_and_move()  # Leaning movement
        player1.update_position()  # Apply smooth horizontal movement
        player_gun.update_position()
        player_gun.shoot()
        player1.draw(screen)
        player_gun.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
