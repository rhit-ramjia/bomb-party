import socket
import sys
import threading

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

    t = threading.Thread(target=listener_thread, args=(client_socket,))
    t.start()


    message = input("Choose a username: ")
    message = "Username: " + message
    client_socket.send(message.encode())
    
    while (message.lower().strip() != ';;;'):

        message = input("")
        client_socket.send(message.encode())
        # in_data = client_socket.recv(1024).decode()

        # print("Received from server:", str(in_data))

    
    client_socket.close()

def listener_thread(client_socket):
    while(True):
        in_data = client_socket.recv(1024).decode()
        print("Received from server:", str(in_data))

if __name__ == '__main__':
    client_program()