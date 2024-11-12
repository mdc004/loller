import socket
import threading
import time
import json
# socket.gethostbyname(socket.gethostname())
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
ABILITY = ["autoattacco","guarigione","danno avanzato"]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Loading champions and abilities from abilities.json
f = open('./abilities.json')
champions = json.load(f)
f.close()
# Skills order
# "champion": 0
# "heal": 1
# "autoAttak": 2
# "abilityShield": 3
# "abilityDamage": 4

playerQueque = -1

#player stack structure: {... "playerID" = [choose(number), heal, lastAbility, myTurn], ...}
playersStack = []

def handleClient(conn, addr):
    # Taking global values
    global playerQueque, playersStack, champions

    # saving player id
    whoAmI = playerQueque

    print(f"[NEW CONNECTION] {addr} connected")
    conn.send(b"Ciao! Benvenuto benvenuto su loller!")

    # Attending  another connection to the server
    conn.send(b"\nAttendi, stiamo cercando un giocatore")
    while playerQueque % 2 == 0:
        conn.send(b".")
        time.sleep(1)
    
    # Starting condown
    conn.send(b"\nGiocatore trovato!")
    conn.send(b"\nSelezione campioni fra ")
    time.sleep(1)
    conn.send(b"3")
    time.sleep(0.25)
    conn.send(b".")
    time.sleep(0.25)
    conn.send(b".")
    time.sleep(0.25)
    conn.send(b".")
    time.sleep(0.25)
    conn.send(b"2")
    time.sleep(0.25)
    conn.send(b".")
    time.sleep(0.25)
    conn.send(b".")
    time.sleep(0.25)
    conn.send(b".")
    time.sleep(0.25)
    conn.send(b"1")
    time.sleep(0.25)

    # Champ selec
    conn.send(b"\nSeleziona un campione: \n\t1. Folletto \n\t2. Mago \n\t3. Strega \n\t4. Mastino\nScelta: ")
    playerChoose = int(conn.recv(64)) - 1

    # Saving the player data in the stack 
    if whoAmI % 2 != 0:
        enemyID = whoAmI - 1
        myTurn = False
    else:
        enemyID = whoAmI + 1
        myTurn = True

    playersStack.insert(whoAmI, [playerChoose, champions[playerChoose][1], 0, myTurn])
    print(f"whoAmI: {whoAmI}")
    print(f"enemy ID: {enemyID}")
    
    # Attending the enemy choose
    conn.send(b"\nAttendi che il giocatore 2 scelga")
    while len(playersStack) % 2 != 0:
        conn.send(b".")
        time.sleep(1)

    conn.send(f"\nIl tuo avversario: {champions[playersStack[enemyID][0]][0]}".encode())

    if playersStack[whoAmI][3] == False:
        conn.send(b"\n\nAttendi il tuo turno")

    while playersStack[whoAmI][1] > 0 and playersStack[enemyID][1] > 0:
        if playersStack[whoAmI][3] == True:
            conn.send(b"\n\nE' il tuo turno!")

            # Checking if is not first time
            if playersStack[enemyID][2] != 0:
                conn.send(f"\nIl tuo avversario ha usato abilita' {ABILITY[playersStack[enemyID][2] - 2]}".encode())

            conn.send(f"\nHai {playersStack[whoAmI][1]} punti salute".encode())
            conn.send(f"\nIl tuo avversario ha {playersStack[enemyID][1]} punti salute".encode())

            conn.send(b"\n\nLa tua mossa (1 autoattacco - 2 guarigione - 3 danno avanzato): ")
            ability = int(conn.recv(64)) + 1

            while ability == playersStack[enemyID][2] or ability > 4 or ability < 2:
                conn.send(b"\nNon puoi eseguire la stessa mossa per due turni di fila")
                conn.send(b"\nPuoi inserire solo 1, 2 o 3")
                conn.send(b"\nLa tua mossa (1 autoattacco - 2 guarigione - 3 danno avanzato): ")
                ability = int(conn.recv(64)) + 1

            playersStack[enemyID][2] = ability
            # Swapping turn
            playersStack[enemyID][3] = True
            playersStack[whoAmI][3] = False

            if ability == 3:
                # Incrementi player heal
                playersStack[whoAmI][1] += champions[playersStack[whoAmI][0]][ability]
            else:
                # Decrementing heal of the enemy
                playersStack[enemyID][1] -= champions[playersStack[whoAmI][0]][ability]

            conn.send(f"\nHai {playersStack[whoAmI][1]} punti salute".encode())
            conn.send(f"\nIl tuo avversario ha {playersStack[enemyID][1]} punti salute".encode())
            conn.send(b"\n\nAttendi ora il tuo turno")

    if playersStack[whoAmI][1] <= 0:
        conn.send(f"\nHai {playersStack[whoAmI][1]} punti salute".encode())
        conn.send(f"\nIl tuo avversario ha {playersStack[enemyID][1]} punti salute".encode())
        conn.send(b"\n\nMI DISPIACE HAI PERSO!")
        conn.close()
    elif playersStack[enemyID][1] <= 0:
        conn.send(f"\nHai {playersStack[whoAmI][1]} punti salute".encode())
        conn.send(f"\nIl tuo avversario ha {playersStack[enemyID][1]} punti salute".encode())
        conn.send(b"\n\nBRAVO HAI VINTO!")
        conn.close()

def start():
    global playerQueque
    server.listen()
    print(f"[LISTENING] Server listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        playerQueque += 1
        thread.start()
        print(f"[INSTANCE playOn] {playerQueque}")

print("[STARTING] server is starting...")
start()