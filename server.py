import socket
import sys
import threading
import random

lock = threading.Lock()

# global client_info
client_info = {}
# cur_client_num = 2
substring = ''
global cur_client
global players_left
turn_event = threading.Event()
# substring = generate_substring()

# max_client_num = 0

def Convert(str): 
    dictList = list(str.split("\n")) 
    return dictList

def generate_substring():
    random_word = random.choice(dictList)
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

def server_thread(my_client_socket, client_num, address, client_info):
    client_info[address] = {'name': '', 'lives': 3, 'client_num': client_num, 'conn_socket': my_client_socket, 'started': False, 'cur_player': 1}
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

            if data == "start":
                cur_client['started'] = True

                while (not all_clients_started(client_info)):
                    continue

                print("all clients started")
                players_left = len(client_info)
                print('aaaaaaaaaaaaa', players_left)
                cur_client['conn_socket'].send("Game has Started\n".encode())

                while (True):
                    cur_client_num = client_info[address]['cur_player']
                    if (cur_client_num == client_num and client_info[address]['lives'] > 0):
                        print("client num: ", client_num)
                        print("cur client num: ", cur_client_num)
                        substring = generate_substring()
                        name = ''
                        for client in client_info:
                            if client_info[client]['client_num'] == cur_client_num:
                                name = client_info[client]['name']
                        for client in client_info:
                            client_info[client]['conn_socket'].send((name + "'s turn\n").encode())
                            client_info[client]['conn_socket'].send((substring + "\n").encode())
                        # cur_client['conn_socket'].send((substring + "\n").encode())
                        print(cur_client['lives'])
                        # timer = threading.Timer(8.0, lose_life, args=(cur_client,))
                        cur_client['conn_socket'].settimeout(2)
                        try:
                            data = cur_client['conn_socket'].recv(1024).decode()
                            if (data.upper()).find(substring) != -1 and data.upper() not in usedList:
                                # timer.cancel()
                                usedList.append(data.upper())
                                print('valid word')
                        except socket.timeout:
                            lose_life(cur_client)
                            for client in client_info:
                                client_info[client]['conn_socket'].send((name + " has " + str(cur_client['lives']) + " lives remaining").encode())
                            if cur_client['lives'] == 0:
                                with lock:
                                    players_left -= 1
                                print('players left', players_left)
                                for client in client_info:
                                    client_info[client]['conn_socket'].send((name + " has died").encode())

                            if players_left == 1:
                                print('game over')
                                break
                        cur_client['conn_socket'].settimeout(None)
                        with lock:
                            for client in client_info:
                                client_info[client]['cur_player'] += 1
                                if client_info[client]['cur_player'] > len(client_info):
                                    client_info[client]['cur_player'] = 1
                        print("cur_client_num: " + str(client_info[client]['cur_player']))
                        turn_event.set()
                    else:
                        turn_event.wait()
                        print('thread cleared')
                        turn_event.clear()
            else:
                my_client_socket.send(data.encode())
        
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
        # cur_client_num = random.randint(1, len(client_info))
        # substring = generate_substring()
        # cur_client = 0

        conn_socket, address = server_socket.accept()

        print("Connection", str(client_num), "made from ", str(address))
        
        t = threading.Thread(target=server_thread, args=(conn_socket, client_num, address, client_info, ))
        t.start()
        # client_info[address] = {'name': '', 'lives': 3, 'client_num': client_num, 'conn_socket': conn_socket}


        client_num += 1
        # max_client_num += 1


if __name__ == '__main__':
    server_program()