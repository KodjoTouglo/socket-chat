import socket
import select

Port = 5000
#Host = socket.gethostname()
Host = "192.168.1.95"
FORMAT = 'utf-8'

# create socket
#socket.AF_INET for IPv4 address
#socket.SOCK_STREAM for TCP connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((Host, Port))

#listen for new connection
server.listen()

#list for socket
socket_list = [server]

# list of clients connected
clients = {}


#handle message receive
def recv_message(client_socket):
    try:
        message_header = client_socket.recv(1024)
        # if there is no data received, client close connection
        if not len(message_header):
            return False
        message_length = int(message_header.decode(FORMAT).strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        #if ctrl+c or client close connection socket.close()
        return False


while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

    for notified_socket in read_sockets:
        if notified_socket == server:
            client_socket, client_address = server.accept()

            #client send his username
            user = recv_message(client_socket)
            if user is False:
                continue
            
            #add accepted socket to select.select() list
            socket_list.append(client_socket)

            #save username and username header
            clients[client_socket] = user

            print(f"Connexion acceptée de {client_address[0]}:{client_address[1]} username:{user['data'].decode(FORMAT)}") 
        
        else:
            #receive msg
            message = recv_message(notified_socket)

            #if no msg , block connection
            if message is False:
                print(f" Connexion fermée par {clients[notified_socket]['data'].decode(FORMAT)}")
                #delete from list socket.socket()
                socket_list.remove(notified_socket)
                #delete from users list
                del clients[notified_socket]
                continue

            #get username by notified socket to know about who send message
            user = clients[notified_socket]
            print(f"Message reçu de {user['data'].decode(FORMAT)}: {message['data'].decode(FORMAT)}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    
    #handling some socket exceptions
    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]










