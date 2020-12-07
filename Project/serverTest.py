import socket
import time
PORT = 8080
SERVER = "192.168.0.34"
ADDR = (SERVER, PORT)
HEADER = 128
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "Close"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
   # connected = True
   # while connected:
   print("Msg receiving....")
   msg = conn.recv(HEADER).decode(FORMAT)
   print(msg)
   print("[Msg RECEIVED ]")
   #if msg == DISCONNECT_MESSAGE:
       #connected = False
   conn.close()
   return msg


def send_to_client(conn, addr, sendmsg):
    message = sendmsg.encode(FORMAT)
    conn.send(message)
    conn.close()



if __name__ == '__main__':
    connected1 = True
    server.listen()
    print("[STARTING] server has started..")
    counter = 10
    while connected1:
        conn, addr = server.accept()
        print("Client Connected")
        recvdmsg = handle_client(conn, addr)
        sendmsg = str(counter)
        conn, addr = server.accept()
        print("Client Connected Again")
        send_to_client(conn, addr, sendmsg)
        if recvdmsg == DISCONNECT_MESSAGE:
            connected1 = False

