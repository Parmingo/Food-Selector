import socket
import threading
import random
import string

# Room management 
rooms = {}

# helper function to create a random room code
def generate_room_code(length = 5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)for _ in range(length))

# client thread function
def client_thread(connection, addr):
    try:
        while True:
            command = connection.recv(1024).decode()
            if not command:
                break

            parts = command.split()
            action = parts[0].upper()

            if action == 'CREATEROOM':
                room_code = generate_room_code()
                rooms[room_code] = [connection]
                connection.send(f"ROOM {room_code}".encode())

            elif action == 'JOINROOM' and len(parts) > 1:
                room_code = parts[1].upper()

                # Join the room if it exists and not full
                if room_code in rooms and len(rooms[room_code]) < 5:
                    rooms[room_code].append(connection)

                    # to notify if room exists
                    for client in rooms[room_code]:
                        if client != connection:
                            client.send(f"NOTIFY {addr} has joined the room: {room_code}")
                    connection.send(f"JOINED {room_code}".encode())

                elif room_code in rooms:
                    connection.send("ERROR: Room is full!".encode())

                else:
                    connection.send("ERROR: Room does not exist! Please try again!".encode())

    finally:
        for room_code, clients in rooms.items():
            if connection in clients:
                clients.remove(connection)

                for client in clients:
                    client.send(f"NOTIFY {addr} has left the room {room_code}".encode())
        connection.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server is listening on {host}:{port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        threading.Thread(target=client_thread, args=(client_socket, addr)).start()

if __name__ == "__main__":
    main()