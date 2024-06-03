
import socket
import threading

HEADER = 64
PORT = 5050
SERVER = "10.30.13.82"
# Another way to get the local IP address automatically
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
print(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Lista para armazenar os clientes conectados
connections = []

# Função para lidar com a conexão de um cliente
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connections.append(conn)
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                else:
                    for connection in connections:
                        if connection != conn:
                            connection.send(msg.encode(FORMAT))
                    print(f"[{addr}] {msg}")
                conn.send("Msg received".encode(FORMAT))
        except Exception as e:
            print(f"Erro ao processar mensagem de {addr}: {e}")
            connected = False

    conn.close()
    if conn in connections:
        connections.remove(conn)

# Função para iniciar o servidor
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

# Inicia o servidor
print("[STARTING] server is starting...")
start()
