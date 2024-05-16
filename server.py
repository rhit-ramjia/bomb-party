import socket
import sys
import threading
import random

lock = threading.Lock()

# global client_info
client_info = {}
player_start_num = 1

# cur_client_num = 2
substring = ''
global cur_client
global players_left
turn_event = threading.Event()
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w','x','y','z']
alphabet = ['e', 'a']
# substring = generate_substring()

# max_client_num = 0

# def Game(address, client_num):
#     while (True):
#         cur_client_num = client_info[address]['cur_player']
#         if (cur_client_num == client_num and client_info[address]['lives'] > 0):
#             print("client num: ", client_num)
#             print("cur client num: ", cur_client_num)
#             if (len(cur_client['players_remaining']) == 1):
#                 print(cur_client['name'] + " wins!")
#                 for client in client_info:
#                     client_info[client]['conn_socket'].send((cur_client['name'] + " wins!\n").encode())
#                 turn_event.set()
                
#                 break
#             substring = generate_substring()
#             name = ''
#             for client in client_info:
#                 if client_info[client]['client_num'] == cur_client_num:
#                     name = client_info[client]['name']
#             for client in client_info:
#                 client_info[client]['conn_socket'].send((name + "'s turn\n").encode())
#                 client_info[client]['conn_socket'].send((substring + "\n").encode())
#             # cur_client['conn_socket'].send((substring + "\n").encode())
#             # print(cur_client['lives'])
#             # timer = threading.Timer(8.0, lose_life, args=(cur_client,))
#             cur_client['conn_socket'].settimeout(8)
#             try:
#                 while True:
#                     data = cur_client['conn_socket'].recv(1024).decode()
#                     print (data.upper().find(substring))
#                     if (not data.upper().find(substring) == -1) and data.upper() not in usedList:
#                         # timer.cancel()
#                         usedList.append(data.upper())
#                         for client in client_info:
#                             client_info[client]['conn_socket'].send((name + " said: " + data).encode())
#                         for letter in data:
#                             print(letter)
#                             if letter in cur_client['unused_letters']:
#                                 cur_client['unused_letters'].remove(letter)
#                         if len(cur_client['unused_letters']) == 0:
#                             cur_client['lives'] += 1
#                             print(cur_client['name'] + "'s lives increased to " + str(cur_client['lives']))
#                             cur_client['unused_letters'] = alphabet

#                         print(cur_client['unused_letters'])
#                         break
#                     else:
#                         if data.upper().find(substring) == -1:
#                             cur_client['conn_socket'].send(('Substring is not in the word\n').encode())
#                         elif data.upper() in usedList:
#                             cur_client['conn_socket'].send(('Word has already been used\n').encode())
                            
#                         cur_client['conn_socket'].send((substring + "\n").encode())
                    
#             except socket.timeout:
#                 lose_life(cur_client)
#                 for client in client_info:
#                     client_info[client]['conn_socket'].send((name + " has " + str(cur_client['lives']) + " lives remaining\n").encode())
#                     if cur_client['lives'] == 0:
#                         client_info[client]['conn_socket'].send((name + " loses the game.\n").encode())
#                         remove_client_num(client_info,cur_client_num)
#                         # if (len(cur_client['players_remaining']) == 1):
#                         #     print("we have a winner!")
#                         #     break

#             cur_client['conn_socket'].settimeout(None)
#             with lock:
#                 for client in client_info:
#                     print(client_info[client]['players_remaining'])
#                     client_info[client]['cur_player'] += 1
#                     while client_info[client]['cur_player'] <= len(client_info) and client_info[client]['cur_player'] not in client_info[client]['players_remaining']:
#                         client_info[client]['cur_player'] += 1
#                     if client_info[client]['cur_player'] > len(client_info):
#                         client_info[client]['cur_player'] = 1
#                     # while client_info[client]['cur_player'] <= len(client_info) and client_info[client]['cur_player'] not in client_info[client]['players_remaining']:
#                     #     client_info[client]['cur_player'] += 1
#             print("cur_client_num: " + str(client_info[client]['cur_player']))
#             turn_event.set()
#         else:
#             turn_event.wait()
#             print('thread cleared')     
    
        
                       
                

def Convert(str): 
    dictList = list(str.split("\n")) 
    return dictList

def generate_substring():
    random_word = random.choice(dictList)
    if (len(random_word) < 3):
        return random_word
    if (len(random_word) == 3):
        start_index = 0
    else:
        start_index = random.randint(0, len(random_word)-3)
    end_index = start_index + random.randint(2, 3)
    random_substring = random_word[start_index:end_index]
    return random_substring

def all_clients_started(client_data):
    for client in client_data:
        if not client_data[client]['started']:
            return False
    return True

def lose_life(client):
    if client['lives'] > 0:
        client['lives'] -= 1
        print(client['name'] + " num lives left: ", client['lives'])

def remove_client_num(client_data, num):
    for client in client_data:
        client_data[client]['players_remaining'].discard(num)

def server_thread(my_client_socket, client_num, address, client_info):
    # my_client_socket.send(("client_num: " + str(client_num)).encode())
    # my_client_socket.send(("client_num: " + str(client_num)).encode())
    with lock:
        client_info[address] = {'name': '', 'lives': 3, 'client_num': client_num, 'conn_socket': my_client_socket, 'started': False, 'cur_player': 1, 'players_remaining': set(), 'used_letters': []}
    while True:
        data = my_client_socket.recv(1024).decode()
        print("i received data: ", data)
        cur_client = client_info[address]
        if not data:
            break
        else:
            print("Data from client:", str(client_num), ":", str(data))
            if data[0:10] == "Username: ":
                username = data[10:]
                client_info[address]['name'] = username
                
                client_names = ''
                for client in client_info:
                    client_names += client_info[client]['name'] + ':'
                for client in client_info:
                    # client_names = ''
                    # client_names += '; ' + client_info[client]['name']
                    client_info[client]['conn_socket'].send(('!!!client_num_name;' + client_names + '\n').encode())
        
            if data == "start":
                cur_client['started'] = True
                # for client in client_info:
                #     client_info[client]['conn_socket'].send(('start:' + cur_client['name'] + ' started').encode())
                    
                with lock:
                    for client in client_info:
                        client_info[client]['players_remaining'].add(cur_client['client_num'])

                while (not all_clients_started(client_info)):
                    continue

                print("all clients started")
                cur_client['conn_socket'].send("Game has started\n".encode())
                print(cur_client['players_remaining'])
                
                ## this causes freezing sometimes?
                # with lock:
                    # player_start_num = random.randint(1, len(client_info))
                # player_start_num == 1
                for client in client_info:
                    client_info[client]['cur_player'] = player_start_num


                
                # while True:
                # Game(address, client_num)
                    # for client in client_info:
                    #     client_info[client]['lives'] = 3
                    #     client_info[client]['started'] = False
                    #     client_info[client]['unused_letters'] = alphabet
                    # for client in client_info:
                    #     client_info[client]['conn_socket'].send(("Play again?\n").encode())
                    # while True:
                    #     data = my_client_socket.recv(1024).decode()
        
                    #     if data == "start":
                    #         cur_client['started'] = True
                    #     while (not all_clients_started(client_info)):
                    #         continue

                while (True):
                    cur_client_num = client_info[address]['cur_player']
                    if (cur_client_num == client_num and client_info[address]['lives'] > 0):
                        # print("client num: ", client_num)
                        # print("cur client num: ", cur_client_num)
                        if (len(cur_client['players_remaining']) == 1):
                            print(cur_client['name'] + " wins!")
                            for client in client_info:
                                client_info[client]['conn_socket'].send((cur_client['name'] + " wins!\n").encode())
                            for client in client_info:
                                client_info[client]['conn_socket'].send(('!!!winner;' + cur_client['name'] + " wins!\n").encode())
                            turn_event.set()
                            
                            for client in client_info:
                                client_info[client]['lives'] = 3
                                client_info[client]['started'] = False
                                client_info[client]['used_letters'] = []
                            break
                        substring = generate_substring()
                        # for client in client_info:
                        #     client_info[client]['conn_socket'].send(('!!!substr;' + substring).encode())
                        
                        name = ''
                        
                        for client in client_info:
                            if client_info[client]['client_num'] == cur_client_num:
                                name = client_info[client]['name']
                        for client in client_info:
                            client_info[client]['conn_socket'].send((name + "'s turn\nSubstring: " + substring +'\n').encode())
                            # client_info[client]['conn_socket'].send((substring + "\n").encode())
                            
                        # cur_client['conn_socket'].send((substring + "\n").encode())
                        # print(cur_client['lives'])
                        # timer = threading.Timer(8.0, lose_life, args=(cur_client,))
                        cur_client['conn_socket'].settimeout(8)
                        try:
                            while True:
                                data = cur_client['conn_socket'].recv(1024).decode()
                                # print (data.upper().find(substring))
                                if (data.upper().find(substring) != -1) and data.upper() not in usedList and data.upper() in dictList:
                                    # timer.cancel()
                                    usedList.append(data.upper())
                                    for client in client_info:
                                        client_info[client]['conn_socket'].send((name + " said: " + data).encode())
                                    for letter in data:
                                        # print(letter)
                                        if letter not in cur_client['used_letters']:
                                            cur_client['used_letters'].append(letter)
                                    print(data)
                                    print(cur_client['used_letters'])
                                    print(alphabet)

                                    alpha_complete = True
                                    for alpha in alphabet:
                                        if alpha not in cur_client['used_letters']:
                                            alpha_complete = False

                                    if alpha_complete:
                                        cur_client['lives'] += 1
                                        for client in client_info:
                                            client_info[client]['conn_socket'].send((name + "\'s lives increased to " + str(cur_client['lives']) +'\n').encode())
                                        print(cur_client['name'] + "'s lives increased to " + str(cur_client['lives']))
                                        cur_client['used_letters'] = []
                                    letter_str = ''
                                    for letter in cur_client['used_letters']:
                                        letter_str += letter
                                    cur_client['conn_socket'].send(('!!!used_letters: ' + letter_str +'\n').encode())

                                    break
                                else:
                                    if data.upper().find(substring) == -1:
                                        cur_client['conn_socket'].send(('Substring is not in the word\n').encode())
                                    elif data.upper() in usedList:
                                        cur_client['conn_socket'].send(('Word has already been used\n').encode())
                                    elif data.upper() not in dictList:
                                        cur_client['conn_socket'].send(('Word is not in dictionary\n').encode())

                                        
                                    cur_client['conn_socket'].send(('Substring: ' + substring + ":\n").encode())
                                
                                    # print(cur_client['used_letters'])
                  
                                
                        except socket.timeout:
                            lose_life(cur_client)
                            
                            for client in client_info:
                                client_info[client]['conn_socket'].send((name + " has " + str(cur_client['lives']) + " lives remaining\n").encode())
                                if cur_client['lives'] == 0:
                                    client_info[client]['conn_socket'].send((name + " loses the game.\n").encode())
                                    # client_info[client]['conn_socket'].send((name + " loses the game.\n").encode())
                                    remove_client_num(client_info,cur_client_num)
                                    # if (len(cur_client['players_remaining']) == 1):
                                    #     print("we have a winner!")
                                    #     break

                        cur_client['conn_socket'].settimeout(None)
                        with lock:
                            for client in client_info:
                                print(client_info[client]['players_remaining'])
                                client_info[client]['cur_player'] += 1
                                while client_info[client]['cur_player'] <= len(client_info) and client_info[client]['cur_player'] not in client_info[client]['players_remaining']:
                                    client_info[client]['cur_player'] += 1
                                if client_info[client]['cur_player'] > len(client_info):
                                    client_info[client]['cur_player'] = 1
                                # while client_info[client]['cur_player'] <= len(client_info) and client_info[client]['cur_player'] not in client_info[client]['players_remaining']:
                                #     client_info[client]['cur_player'] += 1
                        print("cur_client_num: " + str(client_info[client]['cur_player']))
                        turn_event.set()
                    else:
                        turn_event.wait()
                        print('thread cleared')                        
                        turn_event.clear()
            elif data[0:10] == 'Username: ':
                continue
            else:
                my_client_socket.send(('Not a valid command\n').encode())        
    my_client_socket.close()    

def server_program():
    file = open('dict.txt', 'r')
    data = file.read()
    global dictList
    dictList = Convert(data)
    # print(dictList[1]) 
    global usedList   
    usedList = []
    
    host = socket.gethostname()
    # host = '172.22.47.255'
    host_ip = socket.gethostbyname(host)

    print("Host name:", str(host))
    print("Host ip:", str(host_ip))

    if (len(sys.argv) != 2):
        print("Usage: python server.py <port_number>")
        sys.exit()

    port = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))

    server_socket.listen(5)

    client_num = 1

    while True:
        conn_socket, address = server_socket.accept()

        print("Connection", str(client_num), "made from ", str(address))
        
        t = threading.Thread(target=server_thread, args=(conn_socket, client_num, address, client_info, ))
        t.start()
        # client_info[address] = {'name': '', 'lives': 3, 'client_num': client_num, 'conn_socket': conn_socket}


        client_num += 1
        # max_client_num += 1


if __name__ == '__main__':
    server_program()