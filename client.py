import socket
import sys
import threading
from graphics import *

win = GraphWin('Bomb Party', 600, 600)
win.setBackground('white')
loading = Text(Point(290, 290), 'Please enter your username')
loading.draw(win)
entry = Entry(Point(290, 320), 20) 
entry.draw(win)
client_names = []
arrow = ''
queue = []
arrows=[]
lives_list=[]
xs=[]
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w','x','y','z']

# creates a red cross to indicate dead players
def red_cross(x, y):
    rect1 = Line(Point(x + 10, y - 10), Point(x - 10, y + 10))
    rect2 = Line(Point(x + 10, y + 10), Point(x - 10, y - 10))
    rect1.setWidth(3)
    rect2.setWidth(3)
    rect1.setFill('red')
    rect2.setFill('red')
    rect1.draw(win)
    rect2.draw(win)

# creates a little red cross to indicate used letters
def lil_red_cross(x, y):
    rect1 = Line(Point(x + 5, y - 5), Point(x - 5, y + 5))
    rect2 = Line(Point(x + 5, y + 5), Point(x - 5, y - 5))
    rect1.setFill('red')
    rect2.setFill('red')
    rect1.draw(win)
    rect2.draw(win)
    xs.append(rect1)
    xs.append(rect2)
    
# clears the graphics window
def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()
    
# client program
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

    t1 = threading.Thread(target=listener_thread, args=(client_socket,))
    t1.start()

    # enter username
    while True:
        key = win.getKey()
        if key == "Return": 
            break
        
    username = entry.getText()
    message = "Username: " + username
    client_socket.send(message.encode())
    t2 = threading.Thread(target=messager_thread, args=(client_socket, message))
    t2.start()
    
    # waiting for start screen
    clear(win)
    wait_for_start = Text(Point(290,290), "Waiting for all players to type \"start\"")
    wait_for_start.draw(win)

    # waits for graphics queue to update so graphics can be drawn
    while True:
        while (len(queue) != 0):
            
            # draws client names
            if queue[0].find('client_names:') != -1:
                
                client_names = queue[0].split(':')
                lives_list.clear()
                
                for i in range(1, len(client_names) - 1):
                    g_name = Text(Point((i * 100), 100), client_names[i])
                    g_name.draw(win)
                    lives = Text(Point((i * 100), 70), 'Lives: 3')
                    lives.setTextColor('pink')
                    lives_list.append(lives)
                    
            # draws x's on used letters
            elif queue[0].find('used_letters:') != -1:
                letter_list = queue[0].split('used_letters:')
                letter_list = letter_list[1].split(':')
                
                for x in range(0, len(alphabet)):
                    if letter_list[0].find(alphabet[x]) != -1:
                        lil_red_cross(10+23*x,530)
            
            # changes to game screen
            if queue[0].find('game start') != -1:
                wait_for_start.undraw()
                bomb = Circle(Point(290,290), 80)
                bomb.setFill('black')
                bomb.draw(win)
                
                for x in range (0, len(lives_list)):
                    lives_list[x].draw(win)
                for x in range (0, len(alphabet)):
                    text_letter = Text(Point(10 + 23*x,530), alphabet[x])
                    text_letter.draw(win)
            
            # changes to winner screen
            if queue[0].find('winner:') != -1:
                winner = queue[0].split(':')
                clear(win)
                win_text = Text(Point(290,290), winner[1])
                win_text.draw(win)
                
            # draws x's on dead players
            if queue[0].find('loser:') != -1:
                loser = queue[0].split(':')
                for x in arrows:
                    x.undraw()
                    
                for i in range(1, len(client_names) - 1):
                    if client_names[i] == loser[1]:
                        red_cross(i*100, 100)
                        
                        if i == len(client_names) - 2:
                            arrow = Line(Point(290,280), Point(100,110))
                        else:
                            arrow = Line(Point(290,280), Point((i + 1) * 100,110))
                        arrows.append(arrow)
                        arrow.setArrow('last')
                        arrow.draw(win)
                
            # updates the substring in the bomb
            if queue[0].find('substr:') != -1:
                substr = queue[0].split(':')
                black_out = Circle(Point(290,290), 80)
                black_out.setFill('black')
                black_out.draw(win)
                substring = Text(Point(290,300), substr[1])
                substring.setTextColor('white')
                substring.draw(win)
            
            # updates the bomb arrow
            if queue[0].find('player_name:') != -1:
                player_name = queue[0].split(':')
                for x in arrows:
                    x.undraw()
                    
                for i in range(1, len(client_names) - 1):
                    if client_names[i] == player_name[1]:
                        arrow = Line(Point(290,280), Point(i * 100,110))
                        arrows.append(arrow)
                        arrow.setArrow('last')
                        arrow.draw(win)

            # removes all x's if player uses every letter in alphabet and increases life count
            if queue[0].find('reset_letters:') != -1:
                reset_letters = queue[0].split(':')                
                if reset_letters[1] == username:
                    for x in xs:
                        x.undraw()
                        
                for x in range(1, len(client_names)-1):
                    if client_names[x] == reset_letters[1]:
                        lives_list[x-1].setText("Lives: " + reset_letters[2])
            
            # decreases life count
            if queue[0].find('life_msg:') != -1:
                life_msg = queue[0].split(':')
                for x in range(1, len(client_names)-1):
                    if life_msg[1] == (client_names[x]):
                        lives_list[x-1].setText("Lives: " + life_msg[2])
                        
            queue.pop(0)
    
# constantly listens for msgs from server
def listener_thread(client_socket,):
    while(True):
        in_data = client_socket.recv(1024).decode()
        
        # parse messages from server
        split_msg = in_data.split('\n')
        for msg in split_msg:
            cmd = msg.split(';')
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
                queue.append('substr:' + substring[1])
            
            if (cmd[0].find('\'s turn') != -1):
                player_name = cmd[0].split('\'')
                queue.append('player_name:' + player_name[0])

            if(cmd[0].find('used_letters:') != -1):
                letters = cmd[0].split('used_letters:')
                queue.append('used_letters:' + letters[1])
            
            if(cmd[0].find('lives remaining') != -1):
                life_msg = cmd[0].split(' lives remaining')
                life_msg = life_msg[0].split(' has ')
                queue.append('life_msg:' + life_msg[0] + ":" + life_msg[1])

            if(cmd[0].find('\'s lives increased to ') != -1):
                reset_letters = cmd[0].split('\'s lives increased to ')
                queue.append('reset_letters:' + reset_letters[0] + ":" + reset_letters[1])

        # does not print any message with !!!
        if in_data.find('!!!') == -1: 
            print(str(in_data))

# constantly allows users to send msgs to server
def messager_thread(client_socket, message):
    while (message.lower().strip() != ';;;'):

        message = input("")
        client_socket.send(message.encode())
    client_socket.close()
    

if __name__ == '__main__':
    client_program()