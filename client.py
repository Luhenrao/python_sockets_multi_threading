
import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# Whatever IP address you found from running ipconfig in terminal.
SERVER = "10.30.13.82"
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Officially connecting to the server.
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    while True:
        try:
            message = client.recv(2048).decode(FORMAT)
            if message:
                print(f"[SERVER] {message}")
        except OSError:
            print("Socket error occurred.")
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

while True:
    msg = input()
    send(msg)
    if msg == DISCONNECT_MESSAGE:
        break

receive_thread.join()
client.close()
