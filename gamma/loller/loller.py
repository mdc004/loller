import json

# Loading champions and abilities from abilities.json
f = open('./abilities.json')
champions = json.load(f)
f.close()

# Iterating through the json
# list
# print(data[0]['champion'])

playerHeal = [100, 125, 150, 200]

# print('Ciao, benvenuto nel loller game!')
# print('Come prima cosa dovrai scegliere un personaggio tra quelli proposti, ognuno di essi si differenzia per abilità, punti attacco e salute')
# print('Una volta scelto il tuo personaggio la battaglia avrà inizio!')
# print('Dovrai scegliere ogni volta quale abilità usare contro il tuo avversario, di cui conoscerai solo salute e di conseguenza tipo')
# print('Il primo a perdere tutta la salute avrà perso!')
# print('3... 2... 1... Viaaaa!\n\n')

player1Choose = int(input('Giocatore 1 scegli:\n\t1. per folletto\n\t2. per mago\n\t3. per strega \n\t4. mastino\nScelta: ')) - 1
player2Choose = int(input('Giocatore 2 scegli:\n\t1. per folletto\n\t2. per mago\n\t3. per strega \n\t4. mastino\nScelta: ')) - 1

# Store the abilities used by the players
player1History = []
player2History = []

# Saving champions data 
##uso il metodo delle liste copy per non copiare per referenza e collegare quindi tutti gli array (uno cambia gli altri cambiano)
player1Parameters = champions[player1Choose].copy() 
player2Parameters = champions[player2Choose].copy()

## Skills order
# "champion": 0
# "heal": 1
# "autoAttak": 2 
# "abilityShield": 3
# "abilityDamage": 4

while player1Parameters[1] > 0 and player2Parameters[1] > 0:
    # fare il controllo della mossa con lo switch (tra due e quattro compresi)
    player1Choose = int(input('Giocatore 1 seleziona la tua mossa: '))
    player2Choose = int(input('Giocatore 2 seleziona la tua mossa: '))

    if player1Choose and player2Choose is 3:
        #stampa risultati uguali, entrambi scudo, nessun danno
        print('entrambi scudo')
    elif player1Choose is 3:
        player1Parameters[1] -= abs(player1Parameters[3] - player2Parameters[player2Choose])
    elif player2Choose is 3:
        player2Parameters[1] -= abs(player2Parameters[3] - player1Parameters[player2Choose])
    else:
        player1Parameters[1] -= player2Parameters[player2Choose]
        player2Parameters[1] -= player1Parameters[player1Choose]
    print("giocatore 1: ",player1Parameters[1])
    print("giocatore 2: ",player2Parameters[1])
else:
    print("end of the game")