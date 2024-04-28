import socket
import sys

def client_program():
    if (len(sys.argv) != 3):
        print("Usage: python client.py <ServerIP> <ServerPort>")
        sys.exit()
    
    port = int(sys.argv[2])
    server_ip = socket.gethostbyname(sys.argv[1])

    print("Server IP:", server_ip)

    server_addr = (server_ip, port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(server_addr)

    message = input("Choose a username: ")
    message = "Username: " + message
    while (message.lower().strip() != ';;;'):
        client_socket.send(message.encode())

        in_data = client_socket.recv(1024).decode()

        print("Received from server:", str(in_data))

        # if (in_data == "Choose a username."):

        #     message = input("Username: ")
        # else:
        message = input(" -> ")
    
    client_socket.close()

if __name__ == '__main__':
    client_program()