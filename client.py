import socket
import sys
import threading
import asyncio

# qq = asyncio.Queue()
# import pygame

from graphics import *
win = GraphWin('Bomb Party', 600, 600)
loading = Text(Point(290, 290), 'Please enter your username')
loading.draw(win)

queue = []
        
def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()
    
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

    # c = Circle(Point(290,290), 60)
    # c.draw(win)
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
    
    clear(win)
    # c = Circle(Point(290,290), 60)
    wait_for_start = Text(Point(290,290), "Waiting for all players to type \"start\"")
    wait_for_start.draw(win)
    
    # print('hi')
    while True:
        while (len(queue) != 0):
            # print(queue[0])
            if queue[0].find('client_names:') != -1:
                
                client_names = queue[0].split(':')
                print(str(client_names))
                # print('adding names\n')
                # i = 1
                for i in range(1, len(client_names) - 1):
                    
                    
                    g_name = Text(Point((i * 100), 100), client_names[i])
                    g_name.draw(win)
            elif queue[0].find('game start') != -1:
                # print('yay')
                wait_for_start.undraw()
                bomb = Circle(Point(290,290), 60)
                bomb.draw(win)

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
        cmd = in_data.split(';')
        # print(cmd[0])
        if (cmd[0] == '!!!client_num_name'):
            queue.append('client_names:' + cmd[1])
            # print('addedd to queue\n')
            
            # print('yay')
        # print(str(in_data[0:3]))
        elif (cmd[0].find('Game has started') != -1):
            queue.append('game start')
        if not in_data[0:3] == '!!!': 
            print(str(in_data))

def messager_thread(client_socket, message):
    while (message.lower().strip() != ';;;'):

        message = input("")
        client_socket.send(message.encode())
    client_socket.close()
    

if __name__ == '__main__':
    client_program()