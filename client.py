import socket
import select 
import errno
import sys

Host = "192.168.1.95"
Port = 5000
FORMAT = 'utf-8'
HEADER_LENGTH = 1024

my_username = input("Username: ")

# create socket
#socket.AF_INET for IPv4 address
#socket.SOCK_STREAM for TCP connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((Host, Port))

#don't block the recv_msg() call
client.setblocking(False)

#encode to byte
username = my_username.encode(FORMAT)
username_header = f"{len(username):<{HEADER_LENGTH}}".encode(FORMAT)
client.send(username_header + username)

while True:
    #wait for username input
    message = input(f"[{my_username}] => ")
   
    # if empty msg send it
    if message:
        # encode to byte
        message = message.encode(FORMAT)
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode(FORMAT)
        client.send(message_header + message)
    try:
        # loopover received messages and print them
        while True:
            #receive our username header
            username_header = client.recv(HEADER_LENGTH)

            # if no data ,closeconnection
            if not len (username_header):
                print("Connexion fermée par le serveur.")
                sys.exit()
             #convert header into int
            username_length = int(username_header.decode(FORMAT).strip())
            #reiceive and decode username
            username = client.recv(username_length).decode(FORMAT)

            #receive and decode message
            message_header = client.recv(HEADER_LENGTH)
            message_length = int(message_header.decode(FORMAT).strip())
            message = client.recv(message_length).decode(FORMAT)
            #print message
            print(f"[{username}] > {message}")

    except IOError as e:
        #continue connection for no icoming data
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Lecture d'erreur", str(e))
            sys.exit()
        continue

    except Exception as e:
        # other exception exit
        print("Erreur générale", str(e))
        sys.exit()


