import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 12345

    client_socket.connect((host,port))
    print("Connected to the server")

    #user input
    action = input("Enter 'create' to create a room or 'join' to join a room: ").strip().lower()
    while True:
        if action == 'create':
            client_socket.send("CREATEROOM".encode())
            response = client_socket.recv(1024).decode()
            print(f"SERVER RESPONSE: {response}")
            break

        elif action == 'join':
            room_code = input("Enter the room code: ").strip().upper()
            client_socket.send(f"JOINROOM {room_code}".encode())
            response = client_socket.recv(1024).decode()
            print(f"SERVER RESPONSE: {response}")

            if "JOINED" in response:
                print("Successfully joined the room!")
                break
            else:
                print("Please try again!")



    client_socket.close()

if __name__ == "__main__":
    main()