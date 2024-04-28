import socket
import sys
import threading

def Convert(str): 
    dictList = list(str.split("\n")) 
    return dictList

def server_thread(my_client_socket, client_num):
    while True:
        data = my_client_socket.recv(1024).decode()

        if not data:
            break
        else:
            print(data[0:10])
            if data[0:10] == "Username: ":
                username = data[0:10]
                # print('yay')
            print("Data from client:", str(client_num), ":", str(data))
            data = str(data).upper()
            my_client_socket.send(data.encode())
        
    my_client_socket.close()    

def server_program():
    file = open('dict.txt', 'r')
    data = file.read()
    dictList = Convert(data)
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

        t = threading.Thread(target=server_thread, args=(conn_socket, client_num,))
        t.start()

        client_num += 1


if __name__ == '__main__':
    server_program()