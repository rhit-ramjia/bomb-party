import socket
import sys
import threading
import asyncio

# qq = asyncio.Queue()
# import pygame

from graphics import *
win = GraphWin('Bomb Party', 600, 600)
queue = []
        

def client_program():
    
    if (len(sys.argv) != 3):
        print("Usage: python client.py <ServerIP> <ServerPort>")
        sys.exit()
    
    port = int(sys.argv[2])
    server_ip = socket.gethostbyname(sys.argv[1])
    # server_ip = socket.gethostbyname('172.22.47.255')

    print("Server IP:", server_ip)

    server_addr = (server_ip, port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(server_addr)

    t1 = threading.Thread(target=listener_thread, args=(client_socket,))
    t1.start()

    c = Circle(Point(290,290), 60)
    c.draw(win)
    # while True:
    #     while (len(queue) != 0):
    #         g_name = Text(Point(290,100), queue[0])
    #         queue.pop(0)
    #         g_name.draw(win)

    message = input("Choose a username: ")
    message = "Username: " + message
    client_socket.send(message.encode())
    t2 = threading.Thread(target=messager_thread, args=(client_socket, message))
    t2.start()
    while True:
        while (len(queue) != 0):
            client_names = queue[0].split(':')
            print(str(client_names))
            for i in range(len(client_names)):
                
                g_name = Text(Point(100 + (i * 50), 100), client_names[i])
                g_name.draw(win)
    
            queue.pop(0)
    
    
    # while (message.lower().strip() != ';;;'):

    #     message = input("")
    #     client_socket.send(message.encode())
    #     # in_data = client_socket.recv(1024).decode()

    #     # print("Received from server:", str(in_data))
    #     while (len(queue) != 0):
    #         g_name = Text(Point(290,100), queue[0])
    #         queue.pop(0)
    #         g_name.draw(win)
    
    # client_socket.close()

def listener_thread(client_socket,):
    while(True):
        in_data = client_socket.recv(1024).decode()
        client_num_name = in_data.split(';')
        if (client_num_name[0] == 'client_num_name'):
            queue.append(client_num_name[1])
            
            # print('yay')
        # print(str(in_data[0:3]))
        if not in_data[0:3] == '!!!': 
            print(str(in_data))

def messager_thread(client_socket, message):
    while (message.lower().strip() != ';;;'):

        message = input("")
        client_socket.send(message.encode())
    client_socket.close()
    

if __name__ == '__main__':
    client_program()