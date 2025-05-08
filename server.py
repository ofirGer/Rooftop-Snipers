import socket
import threading
import pickle  # To send dictionaries easily
import protocol

# Server setup
SERVER_IP = "0.0.0.0"  # Listen to all IPs (can change to your computer's IP later)
PORT = 5555

# Start server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen(2)  # Max 2 players
print(f"Server started on {SERVER_IP}: {PORT}. Waiting for players...")

# Player data storage
players = [{}, {}]  # Two slots for two players


def handle_client(client_socket, player_id):
    global players
    print(f"Player {player_id} connected.")

    pro = protocol.Protocol(client_socket)
    #pro.send_data(player_id)
    client_socket.send(str(player_id).encode())
    #try:
    while True:
        data = pro.get_data()
        if data is None:
            print(f"Player {player_id} disconnected.")
            break

        players[player_id] = data
        enemy_data = players[1 - player_id]
        pro.send_data(enemy_data)

    #except Exception as e:
     #   print(f"Player {player_id} caused error: {e}")

    players[player_id] = {}
    client_socket.close()

def start_server():
    player_count = 0

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")

        # Start a thread for this client
        thread = threading.Thread(target=handle_client, args=(client_socket, player_count))
        thread.start()

        player_count += 1
        if player_count >= 2:
            print("Two players connected. No more players accepted.")
            client_socket.send(b'Server full')
            client_socket.close()

start_server()
