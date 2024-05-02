import socket
import sys
import threading
import random

client_info = {}

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

def server_thread(my_client_socket, client_num, address):
    client_info[address] = {'name': '', 'lives': 3, 'client_num': client_num, 'conn_socket': my_client_socket}
    # for client in client_info:
    #     print(str(client['conn_socket']))
    while True:
        data = my_client_socket.recv(1024).decode()
        cur_client = client_info[address]
        if not data:
            break
        else:
            print("Data from client:", str(client_num), ":", str(data))
            if data[0:10] == "Username: ":
                username = data[10:]
                client_info[address]['name'] = username

            if data == "start" and client_num == 1:
                print("leader client started the game")
                
                
                # while(True):

                # one run through of the game. Add loop later
                cur_client_num = random.randint(1, len(client_info))
                cur_client_num = 1
                substring = generate_substring()
                for client in client_info:
                    # print(client_info[client]['conn_socket'])
                    client_info[client]['conn_socket'].send("Game has Started\n".encode())
                    if client_info[client]['client_num'] == cur_client_num:
                        cur_client = client_info[client]
                    client_info[client]['conn_socket'].send((cur_client['name'] + "'s turn\n").encode())
                    client_info[client]['conn_socket'].send((substring + "\n").encode())


                #     client_info[client]['conn_socket'].recv(1024).decode()
                #     print(cur_client_num)
                # # print(client_num)
                # if client_num == cur_client_num:
                #     print("yay")

                # take turns being the client that answers
                # print('1\n')
                data = cur_client['conn_socket'].recv(1024).decode()
                print(data.upper() + '\n')
                print(data.upper().find(substring))
                # if (data.upper()).find(substring) != -1:
                if (data.upper()).find(substring) != -1 and cur_client['client_num'] == cur_client_num:

                    print('yayayayayayayayayayay')
                # print('1\n')
                cur_client_num += 1
                if cur_client_num > len(client_info):
                    cur_client_num = 1
                print("cur_client_num: " + str(cur_client_num))
            else:
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
        # cur_client_num = random.randint(1, len(client_info))
        # substring = generate_substring()
        # cur_client = 0

        conn_socket, address = server_socket.accept()

        print("Connection", str(client_num), "made from ", str(address))
        
        t = threading.Thread(target=server_thread, args=(conn_socket, client_num, address,))
        t.start()
        # client_info[address] = {'name': '', 'lives': 3, 'client_num': client_num, 'conn_socket': conn_socket}


        client_num += 1
        # max_client_num += 1


if __name__ == '__main__':
    server_program()