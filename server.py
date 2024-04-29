import socket
import sys
import threading
import random

client_info = {}

def Convert(str): 
    dictList = list(str.split("\n")) 
    return dictList

def generate_substring():
    random_word = random.choice(dictList)
    start_index = random.randint(0, len(random_word)-3)
    end_index = start_index + random.randint(2, 3)
    random_substring = random_word[start_index:end_index]
    return random_substring

def server_thread(my_client_socket, client_num, address):
    client_info[address] = {'name': '', 'lives': 3, 'client_num': client_num}
    while True:
        data = my_client_socket.recv(1024).decode()
        if not data:
            break
        else:
            print("Data from client:", str(client_num), ":", str(data))
            if data[0:10] == "Username: ":
                username = data[10:]
                client_info[address]['name'] = username
                print(client_info)

            if data == "start" and client_num == 1:
                print("leader client started the game")
            my_client_socket.send(data.encode())
        
    my_client_socket.close()    

def server_program():
    file = open('dict.txt', 'r')
    data = file.read()
    global dictList
    dictList = Convert(data)
    # print(dictList[1])    
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
        conn_socket, address = server_socket.accept()

        print("Connection", str(client_num), "made from ", str(address))

        t = threading.Thread(target=server_thread, args=(conn_socket, client_num, address,))
        t.start()

        client_num += 1


if __name__ == '__main__':
    server_program()