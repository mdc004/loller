import socket
import threading
import time

HEADER = 64
FORMAT = "utf-8"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

playerQueque = 0

def handleClient(conn, addr):
    global playerQueque
    print(f"[NEW CONNECTION] {addr} playOn")
    playOn = True
    conn.send(b"Ciao! Benvenuto benvenuto su loller!")
    conn.send(f"\nPlayerID: {playerQueque}".encode())
    
    while playOn:
        msg = conn.recv(64)
        conn.send(b"\nAttendi, stiamo cercando un giocatore...")
        while playerQueque % 2 != 0:
            conn.send(b".")
            time.sleep(1)
        if msg == "!DISCONNECT":
            playOn = False
        # print(f"[{addr}] {msg}")
    conn.close()

def start():
    global playerQueque
    server.listen()
    print(f"[LISTENING] Server listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        playerQueque += 1
        print(f"[INSTANCE playOn] {playerQueque}")

print("[STARTING] server is starting...")
start()