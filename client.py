import socket
import sys
import threading
import asyncio

# qq = asyncio.Queue()
# import pygame

from graphics import *
win = GraphWin('Bomb Party', 600, 600)
win.setBackground('white')
loading = Text(Point(290, 290), 'Please enter your username')
loading.draw(win)
client_names = []
arrow = ''
queue = []
arrows=[]
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w','x','y','z']


def red_cross(x, y):
    rect1 = Line(Point(x + 10, y - 10), Point(x - 10, y + 10))
    rect2 = Line(Point(x + 10, y + 10), Point(x - 10, y - 10))
    rect1.setWidth(3)
    rect2.setWidth(3)
    rect1.setFill('red')
    rect2.setFill('red')
    rect1.draw(win)
    rect2.draw(win)

def lil_red_cross(x, y):
    rect1 = Line(Point(x + 5, y - 5), Point(x - 5, y + 5))
    rect2 = Line(Point(x + 5, y + 5), Point(x - 5, y - 5))
    # rect1.setWidth(3)
    # rect2.setWidth(3)
    rect1.setFill('red')
    rect2.setFill('red')
    rect1.draw(win)
    rect2.draw(win)
    
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
                # print(str(client_names))
                # print('adding names\n')
                # i = 1
                for i in range(1, len(client_names) - 1):
                    
                    
                    g_name = Text(Point((i * 100), 100), client_names[i])
                    g_name.draw(win)
                    
            elif queue[0].find('used_letters:') != -1:
                letter_list = queue[0].split('used_letters:')
                letter_list = letter_list[1].split(':')
                # letters = letters[1].split('[')
                # letters = letters[0].split(']')
                # letters = letters[0].split(', ')
                # print(letter_list)
                for x in range(0, len(alphabet)):
                    if letter_list[0].find(alphabet[x]) != -1:
                        lil_red_cross(10+23*x,530)
                    
                
                
            if queue[0].find('game start') != -1:
                # print('yay')
                wait_for_start.undraw()
                bomb = Circle(Point(290,290), 80)
                bomb.setFill('black')
                bomb.draw(win)
                
                for x in range (0, len(alphabet)):
                    text_letter = Text(Point(10 + 23*x,530), alphabet[x])
                    text_letter.draw(win)
                # arrow = Line(Point(290,290), Point(100,110))
                
                # arrow.setArrow('last')
                # arrow.draw(win)
                # 
            
            if queue[0].find('winner:') != -1:
                winner = queue[0].split(':')
                clear(win)
                win_text = Text(Point(290,290), winner[1])
                win_text.draw(win)
                
            if queue[0].find('loser:') != -1:
                loser = queue[0].split(':')
                for x in arrows:
                    x.undraw()
                # print(len(client_names))
                for i in range(1, len(client_names) - 1):
                    if client_names[i] == loser[1]:
                        # g_loser = Circle(Point((i * 100), 100), 20)
                        
                        # g_loser = Text(Point((i * 100), 100), client_names[i])
                        # g_loser.setTextColor('red')
                        # g_loser.draw(win)
                        red_cross(i*100, 100)
                        
                        if i == len(client_names) - 2:
                            arrow = Line(Point(290,280), Point(100,110))
                        else:
                            arrow = Line(Point(290,280), Point((i + 1) * 100,110))
                        arrows.append(arrow)
                        arrow.setArrow('last')
                        arrow.draw(win)
                # win_text = Text(Point(290,290), winner[1])
                # win_text.draw(win)
                
            if queue[0].find('substr:') != -1:
                substr = queue[0].split(':')
                black_out = Circle(Point(290,290), 80)
                black_out.setFill('black')
                black_out.draw(win)
                # substring.undraw()
                for x in arrows:
                    x.undraw()
                substring = Text(Point(290,300), substr[1])
                substring.setTextColor('white')
                substring.draw(win)
                for i in range(1, len(client_names) - 1):
                    if client_names[i] == substr[2]:
                        
                        arrow = Line(Point(290,280), Point(i * 100,110))
                        arrows.append(arrow)
                        arrow.setArrow('last')
                        arrow.draw(win)
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
        # print(cmd)
        if (cmd[0] == '!!!client_num_name'):
            queue.append('client_names:' + cmd[1])
            
        if (cmd[0].find('Game has started') != -1):
            queue.append('game start')
            
        if(cmd[0].find('!!!winner') != -1):
            queue.append('winner:' + cmd[1])
       
        if(cmd[0].find('loses the game') != -1):
            loser = cmd[0].split(' loses')
            queue.append('loser:' + loser[0])
            
        if(cmd[0].find('Substring:') != -1):
            substring = cmd[0].split('Substring:')
            player_name = cmd[0].split('\'')
            queue.append('substr:' + substring[1] +':' + player_name[0])
            
        if(cmd[0].find('used_letters:') != -1):
            letters = cmd[0].split('used_letters:')
            queue.append('used_letters:' + letters[1])
            
        if in_data.find('!!!') == -1: 
            print(str(in_data))

def messager_thread(client_socket, message):
    while (message.lower().strip() != ';;;'):

        message = input("")
        client_socket.send(message.encode())
    client_socket.close()
    

if __name__ == '__main__':
    client_program()