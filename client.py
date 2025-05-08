import pygame
import socket
import pickle
import player
import gun
import config
import protocol

class GameClient:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Rooftop Snipers - Ofir G")
        self.clock = pygame.time.Clock()

        self.local_player = player.Player(config.ROOF_X + 20, config.ROOF_Y)
        self.local_gun = gun.Gun(self.local_player, self.screen)

        self.running = True

        # Networking setup
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pro = protocol.Protocol(self.client_socket)
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.client_socket.connect((config.SERVER_IP, config.PORT))
            self.player_id = self.client_socket.recv(1).decode()
            print(f"Connected to server as Player {self.player_id}")
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            self.running = False

    def send_and_receive_data(self):
        try:
            player_data = self.local_player.get_data()
            gun_data = self.local_gun.get_data()
            combined_data = {
                "player": player_data,
                "gun": gun_data
            }

            self.client_socket.send(pickle.dumps(combined_data))

            enemy_data = self.pro.get_data()
        except Exception as e:
            print(f"Connection error: {e}")
            self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.local_player.jump()

    def update_game_logic(self):
        self.local_player.apply_movement()
        self.local_gun.apply_gun_movement()

    def draw(self):
        self.screen.fill(config.BACKGROUND_COLOR)
        pygame.draw.rect(
            self.screen, config.ROOF_COLOR,
            (config.ROOF_X, config.ROOF_Y, config.ROOF_WIDTH, config.ROOF_HEIGHT)
        )
        self.local_player.draw(self.screen)
        self.local_gun.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(config.FPS)
            self.handle_events()
            self.update_game_logic()
            self.send_and_receive_data()
            self.draw()
        pygame.quit()

if __name__ == "__main__":
    game = GameClient()
    game.run()
