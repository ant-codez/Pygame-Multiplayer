import socket, sys, pickle
from _thread import *
from player import Player

# local ip address
server = "10.112.3.19"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Check if port is open
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# opens port for n-amount of clients
s.listen(2)
print("Waiting for connection, Server Started")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100,100, 50, 50, (0, 0, 255))]

# try to recieve data from connection
def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)
            
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0

# continuely look for new connections
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1