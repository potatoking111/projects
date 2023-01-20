import random
import copy

import pygame

FAINTED = False
FIRST_BATTLE = True
pygame.init()
FIRST_SHOP = True
FIRST_TURN = True
tutorial2Start = False
SCREEN_SIZE = (603,603)#Multiple of 9
SQUARE_SCALE = (SCREEN_SIZE[0] / 9,SCREEN_SIZE[1] / 9)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
FIRE = ['fire','grass',['water'],["grass",'fire']]#first is name, then what its super effective against, then what its weak to, then resistances
WATER = ['water','fire',['grass'],["fire",'water']]
GRASS = ['grass','water',['fire'],["water",'grass']]
NORMAL = ['normal','none',['none'],[]]
BUG = ['bug','none',['fire','flying'],['bug']]
DARK = ['dark','none',['bug','fairy','fighting'],['ghost','psychic']]
font = pygame.font.Font('freesansbold.ttf', 42)
PLAYER_SKIN = "Assets/player_front.png"


FIRE_BITE = ['fire bite',30,FIRE,1.0,'none']#[0] = move name, power, type, accuracy, then stat boost or effect (not always there)
WATER_SUCK = ['water suck',30,WATER,1.0,'none']
GRASS_GUN = ['grass gun',30,GRASS,1.0,'none']
WHACK = ['whack',20,NORMAL,1.0,'none']
WATER_BLOW = ["water blow",50,WATER,.75,'none']
GYM = ['gym',0, NORMAL,1.0,'powerUp']
STARE = ['stare',0,NORMAL,1.0,'none']
RAGE = ['rage',60,NORMAL,.25,'none']
NIBBLE = ['nibble',20,NORMAL,1.0,'none']
CRUNCH = ['crunch',50,NORMAL,1.0,'none']
BUG_BITE = ['bug bite',10,BUG,1.0,'none']
ANGRY_LOOK  = ['angry look',30,DARK,1.0,'powerUp']
PUNCH = ['punch',80,DARK,.90,'none']
WOODEN_HAMMER = ['wooden hammer',50,GRASS,.75,'none']
FIRE_BLAST = ['fire blast',50,FIRE,.75,'none']

#SECOND STAGE EVOLUTIONS
DINGALINGLE = [[8,10,110,9,110,BUG,True,'dingalingle',0],[NIBBLE,WATER_BLOW],[],[8,10,110,9,110,BUG,True,'dingalingle'],[1,1],[("none","none")],0]#
WANGADANGLE = [[5,5,200,9,200,WATER,True,'wangadangle',0],[WATER_BLOW,WATER_SUCK],[],[5,5,200,9,200,WATER,True,'wangadangle'],[1,1],[("none","none")],0]
#TSANGAR
TSANGAR = [[5,5,90,5,90,FIRE,True,'tsangar',0],[WHACK],[(FIRE_BITE,8),(FIRE_BLAST,16)],[5,5,90,5,90,FIRE,True,'tsangar'],[1,1],[("none","none")]] #for stats, first attack, then speed, then health, then level, then current Health, then typing, then if alive or not, then xp. Next is current movepool. Next is available moves to learn with corresponding level (tuple). Next is base stats (copy of first stats but doesnt change). Next is stat boosts during a battle (attack then speed),then evolution info
CHONGAR = [[5,5,90,5,90,WATER,True,'chongar',0],[WHACK],[(WATER_SUCK,8),(WATER_BLOW,16)],[5,5,90,5,90,WATER,True,'chongar'],[1,1],[("none","none")],0]
BJANGMON = [[5,5,90,5,90,GRASS,True,'bjangmon',0],[WHACK],[(GRASS_GUN,8),(WOODEN_HAMMER,16)],[5,5,90,5,90,GRASS,True,'bjangmon'],[1,1],[("none","none")],0]
STANISAURUS = [[5,5,90,5,90,FIRE,True,'stanisaurus',0],[FIRE_BITE,WHACK],[],[5,5,90,5,90,FIRE,True,'stanisaurus'],[1,1],[("none","none")],0]
ETHANT = [[5,3.5,90,5,90,BUG,True,'ethant',0],[NIBBLE,GYM],[(CRUNCH,10)],[5,3.5,90,5,90,BUG,True,'ethant'],[1,1],[("none","none")],0]
LENNY = [[10,1,50,5,50,NORMAL,True,'lenny',0],[RAGE],[],[10,1,50,5,50,NORMAL,True,'lenny'],[1,1],[("none","none")],0]
WANGAR = [[3,4,145,5,145,WATER,True,'wangar',0],[WATER_SUCK,STARE],[],[3,4,145,5,145,WATER,True,'wangar'],[1,1],[(WANGADANGLE,15)],0]
DINGLE = [[1,1,30,1,30,BUG,True,'dingle',0],[BUG_BITE,NIBBLE],[],[1,1,30,1,30,BUG,True,'dingle'],[1,1],[(DINGALINGLE,13)],0]
DYLANDO = [[8,1,110,1,110,DARK,True,'dylando',0],[PUNCH,ANGRY_LOOK],[],[8,1,110,1,110,DARK,True,'dylando'],[1,1],[('none','none')],0]
PEANUTTY = [[5,6,80,1,80,GRASS,True,'peanutty',0],[WOODEN_HAMMER,WHACK],[],[5,1,110,1,110,GRASS,True,'peanutty'],[1,1],[('none','none')],0]


TEAM = [copy.deepcopy(TSANGAR)]

TAG_NUM = 0
LEADER2 = [copy.deepcopy(DINGALINGLE), copy.deepcopy(DYLANDO), copy.deepcopy(WANGADANGLE)]
LEADER2[0][0][3] = 18
LEADER2[1][0][3] = 20
LEADER2[2][0][3] = 22


WHITE = (255,255,255)
BLACK = (0,0,0)

CASH = 5


#MAPS
# AREA1 = [[],[]]#first is actual map that player moves on, second is map of objects like grass
# row = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# for i in range(12):
#     AREA1[0].append(copy.deepcopy(row))
# for i in range(12):
#     AREA1[1].append(copy.deepcopy(row))
# AREA1[0][6][6] = 'P'
# AREA1[0][3][4] = "W" #wall
# AREA1[1][8][8] = "G"
# AREA1[0][4][8] = -1
AREA1ENCOUNTERS = [[ETHANT,STANISAURUS,LENNY,DINGLE],(2,8)]#first is pokemon, then level range
AREA3ENCOUNTERS = [[ETHANT,STANISAURUS,DYLANDO,DINGLE,DINGLE,WANGAR,WANGAR],(9,14)]
AREA1 = []
POKECENTER =  [[[0,0,0,"D2",0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         ["H",0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,"P",0,0]],


         [[0,0,0,"D2",0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         ["H",0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,"P",0,0]],
        AREA1,
        AREA1,
         AREA1,'',
               (5,3)

         ]
AREA2 = [[[0,0,0,"D",0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         ["L",0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,"P",0,0]],


         [[0,0,0,"D",0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0],
         ["L",0,0,0,0,0],
         [0,0,0,0,0,0],
         [0,0,0,0,0,0]],

         AREA1,'',POKECENTER,'',(5,3)

         ]

AREA3 = []
AREA1 = [[[0,0,0,0,0,0,'W','W','W','W','W'],
         [0,0,0,0,0,0,'W','W','W','W','W'],
         [0,0,0,0,0,0,'W','W','W','W','W'],
         [0,0,0,0,0,0,'W','W','D','W','W'],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         ["D2",0,0,0,0,0,"P",0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0]],[],AREA2,AREA1ENCOUNTERS,POKECENTER,AREA3,(7,6)]#first is actual grid, then is grass grid, then is the area it teleports to, then the area spawns

AREA2[2] = AREA1
POKECENTER[3] = AREA1
POKECENTER[4] = AREA1
AREA3 = [[['G','G','G','G','G','G','G','G','G','G','G'],
         ['G','G','G','G','G','G','G','G','G','G','G'],
         ['G','G','G','G','G','G','G','G','G','G','G'],
         ['G','G','G','G','G','G','G','G','G','G','G'],
         ['G','G','G','G','G','G','G','G','G','G','G'],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         ["D3",0,0,0,0,0,"P",0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
          [-1,0,0,0,0,0,0,0,0,0,-1],
          [-1,-1,0,0,0,0,0,0,0,-1,-1],
          [-1,-1,-1,0,0,"L2",0,0,-1,-1,-1]],[],AREA2,AREA3ENCOUNTERS,POKECENTER,AREA1,(7,6)]
AREA1[5] = AREA3

AREA3[1] = copy.deepcopy(AREA3[0])
AREA1[1] = copy.deepcopy(AREA1[0])
for i in range(11):
    for j in range(3):
        AREA1[1][j+9][i] = "G"
print(AREA1)
RED_CALE_BALL = ['red ball',0]#first is name of ball, then how many of each item
BLUE_CALE_BALL = ['blue ball',7]

INVENTORY = [RED_CALE_BALL,BLUE_CALE_BALL]



def battleSequence(enemyPokemon,currentTeam,enemyTeam):
    global battleOver,FIRST_BATTLE,wonBattle
    wonBattle = False
    for pokemonCount in range(len(enemyTeam)):
        enemyTeam[pokemonCount] = healPokemon(enemyTeam[pokemonCount],1000)
    textBox('',False,'')
    currentPokemon = currentTeam[0]
    print(enemyTeam,"enemyTeam")
    enemyPokemon = enemyTeam[0]
    battleOver = False
    currentPokemon = levelToStats(currentPokemon)
    enemyPokemon = levelToStats(enemyPokemon)
    print(enemyPokemon,'enemy')
    displayBattle(currentPokemon, enemyPokemon, currentTeam, enemyTeam, [], True, '', False)

    while not battleOver:

        if currentPokemon[0][1] * currentPokemon[4][1] >= enemyPokemon[0][1] * currentPokemon[4][1]: #checks speed stats


            currentPokemon,enemyPokemon,currentTeam,enemyTeam = defendingPlayerTurn(currentPokemon,enemyPokemon,currentTeam,enemyTeam)
            if battleOver:
                break
            currentPokemon,enemyPokemon,currentTeam,enemyTeam = enemyPlayerTurn(currentPokemon,enemyPokemon,currentTeam,enemyTeam)
            if battleOver:
                break

        else:
            currentPokemon, enemyPokemon, currentTeam, enemyTeam = enemyPlayerTurn(currentPokemon, enemyPokemon,
                                                                                   currentTeam, enemyTeam)
            if battleOver:
                break

            currentPokemon, enemyPokemon, currentTeam, enemyTeam = defendingPlayerTurn(currentPokemon, enemyPokemon,
                                                                                       currentTeam, enemyTeam)

            if battleOver:
                break


        print("the enemy health is", enemyPokemon[0][4], "your health is", currentPokemon[0][4])
    currentTeam[0] = evolutionCheck(currentTeam[0])
    learnMoveCount = 0
    for learnableMove in currentTeam[0][2]:
        if learnableMove[1] == currentTeam[0][0][3]: #FIX LEARN NEW MOVE, MAKE ONLY LEVEL UP WHEN WIN
            currentTeam[0] = learnNewMove(currentTeam[0],learnableMove[0],currentTeam)
            currentTeam[0][2][learnMoveCount] = (learnableMove[0],0)
            learnMoveCount += 1

    for i in range(len(currentPokemon[4])): #resetting stat boosts
        currentPokemon[4][i] = 1
    currentTeam[0] = levelToStats(currentTeam[0])
    return(currentTeam)


def defendingPlayerTurn(currentPokemon,enemyPokemon,currentTeam,enemyTeam):
    global battleOver,FIRST_BATTLE,FAINTED,AREA1,wonBattle,CASH,tutorial2Start,FIRST_TURN,TAG_NUM

    print("Your pokemon is",currentPokemon, "and the enemy pokemon is",enemyPokemon)

    #chosenAction = input("Choose an action, [ATTACK, SWITCH, THROW]").lower()  # later will work with a screen input






    turnOver = False
    if FIRST_BATTLE and FIRST_TURN:
        prompt = 'Try choosing "ATTACK"!'
    else:
        prompt = ''
    while not turnOver:
        chosenAction = displayBattle(currentPokemon, enemyPokemon, currentTeam, enemyTeam,
                                     ['ATTACK', 'SWITCH', 'THROW'], True, prompt, True)
        if chosenAction == 'attack':
            MOVES = []
            for MOVE in currentPokemon[1]:

                MOVES.append(MOVE[0])
            MOVES.append("BACK")
            if FIRST_BATTLE and FIRST_TURN:
                prompt2 = 'Great job! Now, choose an attack!'
                FIRST_TURN = False
                print(FIRST_TURN)
            else:
                prompt2 = ''
            chosenMove = displayBattle(currentPokemon, enemyPokemon, currentTeam, enemyTeam, MOVES,True,prompt2,True)
            #chosenMove = input("Choose a move " + str(MOVES)).lower()


            if chosenMove == "BACK":
                turnOver = False


            for MOVE in currentPokemon[1]:
                moveName = MOVE[0]
                moveDamage = MOVE[1]
                if moveName == chosenMove:

                    if MOVE[3]*100 >= random.randint(1,100):
                        currentPokemonDamageDealt,currentPokemon = damageCalc(currentPokemon[0], MOVE, enemyPokemon[
                            0],currentPokemon)  # finds how much damage should be dealt,inputs the stats
                        enemyPokemon[0][4] -= currentPokemonDamageDealt



                        print("the move", moveName, "was chosen and", currentPokemonDamageDealt, "damage was dealt.")
                        textBox(moveName + " dealt " + str(currentPokemonDamageDealt),True,'')
                        if enemyPokemon[0][4] <= 0:
                            enemyPokemon[0][4] = 0
                            enemyPokemon[0][6] = False
                            numOfAlivePokemon = 0
                            for POKEMON in enemyTeam:
                                if POKEMON[0][6]:
                                    numOfAlivePokemon += 1
                            if numOfAlivePokemon == 0:
                                print("battle over")
                                wonBattle = True
                                cashAmount = random.randint(1,5)
                                textBox('You won and got '+str(cashAmount)+" cash!",True,'')
                                CASH += cashAmount


                                currentTeam[0][0][8] += enemyPokemon[0][3] * 5



                                battleOver = True
                                if FIRST_BATTLE:
                                    textBox("Congrats on your first battle win!",True,'')
                                    textBox("Try to train and then beat the gym leader!",True,'')
                                    textBox("By the way, you can press 't' to enter the shop and spend your cash!", True, '')
                                    textBox('Now, go to the top of the map where the gray box is!',True,'')
                                    textBox('There, you can heal by standing next to the healer and pressing "e"',True,'')

                                    FIRST_BATTLE = False
                            else:
                                enemyTeam[0] = enemyPokemon
                                enemyChoices = []
                                for pokemonOption in enemyTeam:
                                    if pokemonOption[0][4] != 0:
                                        enemyChoices.append(pokemonOption)
                                pokemonChoice = enemyChoices[random.randint(0,len(enemyChoices)-1)]
                                textBox("the enemy's " + enemyPokemon[0][7]+" fainted and "+pokemonChoice[0][7]+ " was switched in",True,'')

                                enemyPokemon = pokemonChoice
                                enemyPokemon = levelToStats(enemyPokemon)
                        turnOver = True
                    else:
                        textBox("The move missed!",True,'')
                elif chosenMove == "back":
                    turnOver = False
        elif chosenAction == 'switch':
            currentPokemon, currentTeam,turnOver  = pokemonSwap(currentPokemon,currentTeam,enemyPokemon,enemyTeam)
        elif chosenAction == "throw":

            if len(enemyTeam) == 1:
                inventoryTemp = []
                for itemInven in INVENTORY:
                    if itemInven[1] >= 1:
                        inventoryTemp.append(itemInven[0])
                inventoryTemp.append("BACK")
                response = displayBattle('','','','',inventoryTemp,False,'Choose an item to use',True)
                invenCount = 0
                invenFinalCount = 100
                for item in INVENTORY:
                    if item[0] == response:

                        invenFinalCount = invenCount
                    invenCount += 1
                print(response,'response')
                if response == 'red ball':
                    caught = catchChanceCalc("red",enemyPokemon[0][4],enemyPokemon[0][2])
                    INVENTORY[invenFinalCount][1] -= 1
                    print("RED CALE BALL CHOSEN")
                    turnOver = True
                elif response == 'blue ball':
                    caught = catchChanceCalc("blue", enemyPokemon[0][4], enemyPokemon[0][2])
                    INVENTORY[invenFinalCount][1] -= 1
                    turnOver = True
                elif response == "BACK":
                    turnOver = False

                if turnOver:
                    print("RANN D")
                    if caught:
                        textBox('the pokemon was caught!',True,'')
                        print('the pokemon was caught!')
                        battleOver = True
                        if len(currentTeam) < 3:

                            currentTeam.append(copy.deepcopy(enemyPokemon))
                            position = len(currentTeam)-1
                            currentTeam[position][6] += TAG_NUM
                            TAG_NUM+=1
                        else:
                            availableOptions = []
                            for pokemon in currentTeam:
                                availableOptions.append(pokemon[0][7]+" "+ str(pokemon[6]))
                            availableOptions.append("PASS")
                            response = displayBattle('','','','',availableOptions,False,'What pokemon will you replace?',True)
                            for i in range(len(currentTeam)):
                                if currentTeam[i][0][7]+" "+str(currentTeam[i][6]) == response:
                                    currentTeam[i] = copy.deepcopy(enemyPokemon)
                                    currentTeam[i][6] += TAG_NUM
                                    TAG_NUM += 1
                            if response == "pass":
                                textBox("You did not add the pokemon to your party.",True,'')
                    else:
                        textBox('the pokemon broke free!',True,'')
                        print('the pokemon broke free!')
            else:
                textBox("'Yo that's my pokemon !'",True,"Try attacking!")

    return currentPokemon,enemyPokemon,currentTeam,enemyTeam


def enemyPlayerTurn(currentPokemon,enemyPokemon,currentTeam,enemyTeam):
    global battleOver,FIRST_BATTLE,FAINTED,AREA1
    chosenAction = displayBattle(currentPokemon, enemyPokemon, currentTeam, enemyTeam,
                                 [], True, '', False)
    enemyMoveChoices = enemyPokemon[1]
    enemyMoveChoice = enemyMoveChoices[random.randint(0, len(enemyMoveChoices) - 1)]
    print(enemyMoveChoice)
    if enemyMoveChoice[3] * 100 >= random.randint(1, 100):


        enemyDamageDealt,enemyPokemon = damageCalc(enemyPokemon[0], enemyMoveChoice,
                                      currentPokemon[0],enemyPokemon)  # finds how much damage should be dealt
        currentPokemon[0][4] -= enemyDamageDealt
        textBox('The enemy pokemon used ' + enemyMoveChoice[0] + " and " + str(enemyDamageDealt) + " was dealt.",True,'')
        print("the enemy move", enemyMoveChoice[0], "was chosen and", enemyDamageDealt, "damage was dealt.")
    else:
        textBox("The opponent's move missed!", True, '')


    if currentPokemon[0][4] <= 0:
        currentPokemon[0][4] = 0
        currentPokemon[0][6] = False
        numOfAlivePokemon = 0
        for POKEMON in currentTeam:
            if POKEMON[0][6]:
                numOfAlivePokemon += 1
        if numOfAlivePokemon == 0:
            print("battle over")
            textBox('You lost and were rushed to the CALE-center.',True,'')
            for pokemonCount in range(len(currentTeam)):
                currentTeam[pokemonCount] = healPokemon(currentTeam[pokemonCount],100000)
            FAINTED = True
            if FIRST_BATTLE:
                textBox("Congrats on your first battle!", True, '')
                textBox("It's fine that you did not win, try to train more", True, 'and then battle the final gym!')




                FIRST_BATTLE = False
            battleOver = True
        else:
            print("your pokemon fainted lol")
            textBox('choose the next pokemon',True,'')
            currentTeam[0] = currentPokemon
            currentPokemon, currentTeam,placeholder = pokemonSwap(currentPokemon, currentTeam,enemyPokemon,enemyTeam)
            currentPokemon = levelToStats(currentPokemon)
    return currentPokemon, enemyPokemon, currentTeam, enemyTeam

def damageCalc(STATS,MOVE,DEFENDINGSTATS,POKEMON):
    POKEMON = statusEffectCheck(MOVE,POKEMON)
    enemyType = DEFENDINGSTATS[5]
    attackMult = (STATS[0]*2/100) + 1
    superEffectiveMult = 1
    for enemyTypeOne in enemyType[2]:
        if MOVE[2][0] == enemyTypeOne:
            print('it was super effective!')

            superEffectiveMult *= 2
    for enemyTypeResistance in enemyType[3]:
        if MOVE[2][0] == enemyTypeResistance:
            superEffectiveMult *= .5
    if superEffectiveMult >= 2:
        textBox("the " + POKEMON[0][7] + "'s move was super effective!", True,'')
    elif superEffectiveMult <= .5:
        textBox("the " + POKEMON[0][7] + "'s move was not very effective...", True,'')
    attackDamage = (MOVE[1] * superEffectiveMult * attackMult * POKEMON[4][0])//1

    return attackDamage,POKEMON
def catchChanceCalc(BALLUSED,DEFENDINGHP,DEFENDINGMAXHP):
    if BALLUSED == 'red':
        odds = (((DEFENDINGMAXHP - DEFENDINGHP) / DEFENDINGMAXHP)+.1 ) *50
        print(odds)
        if random.randint(1,100) <= odds:
            return True
        else:
            return False
    if BALLUSED == 'blue':
        odds = (((DEFENDINGMAXHP - DEFENDINGHP) / DEFENDINGMAXHP)+.1 ) * 100
        print(odds)
        if random.randint(1,100) <= odds:
            return True
        else:
            return False


def pokemonSwap(currentPokemon,currentTeam,enemyPokemon,enemyTeam):


    listOfPokemon = []
    for pokemon in currentTeam:
        if pokemon[0][6]:
            listOfPokemon.append(pokemon[0][7]+" "+str(pokemon[6]))
    listOfPokemon.append('BACK')

    pokemonSelection = displayBattle(currentPokemon, enemyPokemon, currentTeam, enemyTeam, listOfPokemon,False,'',True)
    #pokemonSelection = input("what pokemon do u want to switch " + str(listOfPokemon))
    count = 0
    if pokemonSelection == "back":
        print("ABACK RAN")
        return currentPokemon, currentTeam,False
    for POKEMON in currentTeam:
        if POKEMON[0][7]+" "+str(POKEMON[6]) == pokemonSelection and POKEMON[0][6]:
            print(currentTeam)
            tempPokemon = currentTeam[0]

            currentTeam[count] = tempPokemon
            currentTeam[0] = POKEMON


        count += 1
    currentPokemon = currentTeam[0]
    print(currentTeam,"CURRENT TEAM")
    return currentPokemon, currentTeam,True
def displayBattle(currentPokemon,enemyPokemon,currentTeam,enemyTeam,text,displayHealth,prompt,wait):
    global win, SCREEN,STARTER_SCREEN
    prevOption = ''
    prevSelectedPy = ''


    clearPy = pygame.Surface((SCREEN_SIZE[0],SCREEN_SIZE[1] - SCREEN_SIZE[0]//450))
    clearPy.fill(WHITE)
    SCREEN.blit(clearPy,(0,0))
    if STARTER_SCREEN:
        startingScreen = pygame.image.load('Assets\StarterScreen.png')
        startingScreen = pygame.transform.scale(startingScreen, (SCREEN_SIZE[0], 710 / 900 * SCREEN_SIZE[0]))
        SCREEN.blit(startingScreen, (0, 0))
        pygame.display.flip()


    textBox(prompt, False,'')
    ran = 0
    for OPTION in text:


        newFont = pygame.font.Font('pixel.ttf', int(35/900 * SCREEN_SIZE[0])//1)
        print(OPTION)
        textPy = newFont.render(OPTION, True, BLACK,WHITE)  # first color is text, second if rectangle color

        optionDrawPy = textPy.get_rect()
        optionDrawPy.center = (7.75/9*SCREEN_SIZE[0],330/900 * SCREEN_SIZE[0] + (ran*90/900*SCREEN_SIZE[0]))
        SCREEN.blit(textPy, optionDrawPy)
        pygame.display.flip()


        ran += 1

    if displayHealth:
        healthDisplay(currentPokemon[0][4],currentPokemon[0][2],(100/900*SCREEN_SIZE[0],550/900*SCREEN_SIZE[0]),(400/900*SCREEN_SIZE[0],580/900*SCREEN_SIZE[0]),currentPokemon)
        healthDisplay(enemyPokemon[0][4], enemyPokemon[0][2], (500/900*SCREEN_SIZE[0], 200/900*SCREEN_SIZE[0]),(800/900*SCREEN_SIZE[0], 230/900*SCREEN_SIZE[0]), enemyPokemon)
    pygame.display.flip()
    optionNotSelected = True
    if wait:
        while optionNotSelected:


            if STARTER_SCREEN:

                SCREEN.blit(startingScreen, (0, 0))
            else:
                SCREEN.blit(clearPy, (0, 0))
            textBox(prompt, False,'')
            if displayHealth:
                healthDisplay(currentPokemon[0][4], currentPokemon[0][2],
                              (100 / 900 * SCREEN_SIZE[0], 550 / 900 * SCREEN_SIZE[0]),
                              (400 / 900 * SCREEN_SIZE[0], 580 / 900 * SCREEN_SIZE[0]), currentPokemon)
                healthDisplay(enemyPokemon[0][4], enemyPokemon[0][2],
                              (500 / 900 * SCREEN_SIZE[0], 200 / 900 * SCREEN_SIZE[0]),
                              (800 / 900 * SCREEN_SIZE[0], 230 / 900 * SCREEN_SIZE[0]), enemyPokemon)
            mouseClick = False

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePy = (pygame.mouse.get_pos())
                    mouseClick = True
            ran = 0
            if mouseClick:
                mouseXPy = mousePy[0] / SQUARE_SCALE[0]
                mouseYPy = mousePy[1] / SQUARE_SCALE[0]
                print(mouseXPy, mouseYPy)
                for OPTION in text:
                    textPy = font.render(OPTION, True, (10, 50, 50),
                                       (100, 100, 100))  # first color is text, second if rectangle color



                    if mouseXPy >= 7.2 and mouseXPy <=8.8 and mouseYPy >= 3.1 + ran*.86 and mouseYPy <= 3.56 +ran*.86:

                        newFont = pygame.font.Font('pixel.ttf', int(35 / 900 * SCREEN_SIZE[0]) // 1)
                        textPy = newFont.render(OPTION, True, BLACK,
                                                (200, 200, 200))  # first color is text, second if rectangle color

                        optionDrawPy = textPy.get_rect()
                        optionDrawPy.center = (
                        7.75 / 9 * SCREEN_SIZE[0], 330 / 900 * SCREEN_SIZE[0] + (ran * 90 / 900 * SCREEN_SIZE[0]))




                        SCREEN.blit(textPy, optionDrawPy)
                        if OPTION == prevSelectedPy:
                            STARTER_SCREEN = False
                            return (OPTION).lower()
                        prevSelectedPy = OPTION


                    else:
                        newFont = pygame.font.Font('pixel.ttf', int(35 / 900 * SCREEN_SIZE[0]) // 1)
                        textPy = newFont.render(OPTION, True, BLACK,
                                                WHITE)  # first color is text, second if rectangle color

                        optionDrawPy = textPy.get_rect()
                        optionDrawPy.center = (
                        7.75 / 9 * SCREEN_SIZE[0], 330 / 900 * SCREEN_SIZE[0] + (ran * 90 / 900 * SCREEN_SIZE[0]))



                        SCREEN.blit(textPy, optionDrawPy)





                    ran += 1
                pygame.display.flip()




    #         if mouse != None:
    #             clear = Rectangle(Point(0, 0), Point(600, 400))
    #             clear.setFill('white')
    #             clear.draw(win)
    #
    #
    #             mouseX = mouse.getX() / 60
    #             mouseY = mouse.getY() / 60
    #
    #
    #             ran = 0
    #             if displayHealth:
    #                 healthDisplay(currentPokemon[0][4], currentPokemon[0][2], (50, 350), (350, 370),currentPokemon)
    #                 healthDisplay(enemyPokemon[0][4], enemyPokemon[0][2], (250, 100), (550, 120), enemyPokemon)
    #             for OPTION in text:
    #                 optionDraw = Text(Point(500, 200 + (ran * 60)), OPTION)
    #                 optionDraw.setSize(25)
    #                 optionDraw.draw(win)
    #                 print(mouseX,mouseY)
    #                 if mouseX >= 7 and mouseX <= 9 and mouseY >= ran + 3 and mouseY <= ran + 4:
    #                     optionDraw.setFill("green")
    #
    #                     if prevOption == OPTION:
    #
    #                         return (OPTION).lower()
    #                     prevOption = OPTION
    #                 else:
    #                     optionDraw.setFill("black")
    #                 ran += 1
    #             update(10)
    # clear = Rectangle(Point(0, 0), Point(600, 600))
    # clear.setFill('white')
    # clear.draw(win)




def healthDisplay(pokemonHealth,pokemonMaxHp,point1,point2,pokemon):
    global win

    barLength = point2[0] - point1[0]
    barWidth = point2[1] - point1[1]
    emptyBarPy = pygame.Surface((barLength,barWidth))
    emptyBarPy.fill((100,100,100))



    hpLength = barLength*(pokemonHealth/pokemonMaxHp)
    fullHpBar = pygame.Surface((hpLength,barWidth))

    SCREEN.blit(emptyBarPy,point1)
    SCREEN.blit(fullHpBar, point1)



    newFont = pygame.font.Font('pixel.ttf', int(20 / 900 * SCREEN_SIZE[0]) // 1)
    textPy = newFont.render(("lvl "+str(pokemon[0][3])+", "+pokemon[0][5][0]+" type"+", "+pokemon[0][7] +" "+ str(pokemonHealth)+"/"+str(pokemonMaxHp)), True, BLACK,
                            WHITE)  # first color is text, second if rectangle color

    optionDrawPy = textPy.get_rect()
    optionDrawPy.center = (point1[0]+(point2[0] - point1[0])/2,point1[1]-10)

    SCREEN.blit(textPy, optionDrawPy)


    pokemonImage = pygame.image.load("Assets/"+pokemon[0][7]+".png")
    pokemonImage = pygame.transform.scale(pokemonImage, (150 / 900 * SCREEN_SIZE[0], 150 / 900 * SCREEN_SIZE[0]))

    SCREEN.blit(pokemonImage, (
    point1[0] + (point2[0] - point1[0]) / (8 / 900 * SCREEN_SIZE[0]), point1[1] - (200 / 900 * SCREEN_SIZE[0])))








    # emptyBar = Rectangle(point1,point2)
    # emptyBar.setFill('grey')
    # emptyBar.draw(win)
    # dividerPoint = Point((point2.getX() - point1.getX())*(pokemonHealth / pokemonMaxHp) + point1.getX(),point2.getY())
    # healthBar = Rectangle(point1,dividerPoint)
    # healthBar.setFill('green')
    # healthBar.draw(win)
    # pokemonInfoText = pokemon[0][7], str(pokemonHealth)+'/'+str(pokemonMaxHp)
    #
    # pokemonInfo = Text(Point(point1.getX()+140,point1.getY()-10),pokemonInfoText).draw(win)
    #
    #
    #
    # pokemonArt = Image(Point(point1.getX()+140,point1.getY()-50),pokemon[0][7]+".png").draw(win)
def xpToLevel(XP):
     pass #bro this shit is complicated like jake can make this
def levelToStats(POKEMON):
    print(POKEMON)
    XP_REQ = POKEMON[0][3] * 5
    if POKEMON[0][8] >= XP_REQ:
        POKEMON[0][3] += 1
        textBox(POKEMON[0][7]+" leveled up to level "+str(POKEMON[0][3]),True,'')

        POKEMON[0][8] = 0
    POKEMON[0][0] = POKEMON[3][0] + (POKEMON[0][3]*2)#attack
    POKEMON[0][1] = POKEMON[3][1] + (POKEMON[0][3]*2.5)#speed
    POKEMON[0][2] = (POKEMON[3][2] + (POKEMON[0][3]*6))//1#health

    return POKEMON
for i in range(len(LEADER2)):
    LEADER2[i] = levelToStats(LEADER2[i])
def healPokemon(pokemon,healAmount):
    pokemon[0][4] += healAmount
    pokemon[0][6] = True
    if pokemon[0][4] > pokemon[0][2]:
        pokemon[0][4] = pokemon[0][2]
    return pokemon
def textBox(text,wait,secondLine):
    if wait:
        text +=" (click to continue)"

    if len(text) >= 48:
        tempText = ''
        secondLine = ''
        nextLine = False
        for i in range(len(text)):
            if i > 30 and text[i] == " ":
                nextLine = True
            if i <= 48 and not nextLine:
                tempText += text[i]


            else:
                secondLine += text[i]
        text = tempText
    clearPyOutline = pygame.Surface(
        (SCREEN_SIZE[0] , 200 / 900 * SCREEN_SIZE[0] ))
    clearPyOutline.fill(BLACK)
    SCREEN.blit(clearPyOutline, (0, 700 / 900 * SCREEN_SIZE[0]  ))



    clearPy = pygame.Surface((SCREEN_SIZE[0]-12.5/900*SCREEN_SIZE[0],200/900 * SCREEN_SIZE[0]-12.5/900*SCREEN_SIZE[0]))
    clearPy.fill(WHITE)
    SCREEN.blit(clearPy,(6.25/900*SCREEN_SIZE[0],700/900 * SCREEN_SIZE[0]+6.25/900*SCREEN_SIZE[0]))

    newFont = pygame.font.Font('pixel.ttf', int((25/900 * SCREEN_SIZE[0])//1))
    textPy = newFont.render(text, True, BLACK,
                         WHITE)
    optionDrawPy = textPy.get_rect()


    optionDrawPy.center = ((SCREEN_SIZE[0] / 2,SCREEN_SIZE[0] - 100/900 * SCREEN_SIZE[0]))

    SCREEN.blit(textPy, optionDrawPy)

    newFont = pygame.font.Font('pixel.ttf', int((25 / 900 * SCREEN_SIZE[0]) // 1))
    textPy = newFont.render(secondLine, True, BLACK,
                            WHITE)
    optionDrawPy = textPy.get_rect()

    optionDrawPy.center = ((SCREEN_SIZE[0] / 2, SCREEN_SIZE[0] - 100 / 900 * SCREEN_SIZE[0]+40/900*SCREEN_SIZE[0]))

    SCREEN.blit(textPy, optionDrawPy)

    if wait:
        pygame.display.flip()
        notOver = True
        while notOver:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    SCREEN.blit(clearPy, (0, 700/900 * SCREEN_SIZE[0]))
                    notOver = False






    # clear = Rectangle(Point(0, 400), Point(600, 600))
    # clear.setFill('white')
    # clear.draw(win)
    #
    #
    # textBoxArea = Rectangle(Point(50,450),Point(550,550))
    # textBoxArea.setFill('white')
    # textBoxArea.setWidth(2)
    # textBoxArea.setOutline('black')
    # textBoxArea.draw(win)
    # text = Text(Point(300,500),text + " (click to continue)")
    # text.setStyle('bold')
    # text.setSize(10)
    #
    # text.draw(win)
    # if wait:
    #     win.getMouse()
def learnNewMove(pokemon,newMove,team):
    global win
    if len(pokemon[1]) == 4:


        answer = displayBattle(pokemon,"",team,"",['Yes','No'],False,'Do you want to learn the new move '+str(newMove[0]),True)
        moveNames = []
        print("the answer was",answer)
        for move in pokemon[1]:
            moveNames.append(move[0])

        if answer == "yes":
            answer = displayBattle(pokemon,'',team,'',moveNames,False,'What move will you replace?',True)
            print(answer, "oldmoveactually")
            for i in range(len(pokemon[1])):
                if answer == pokemon[1][i][0]:
                    print(pokemon[1][i],"old move")
                    pokemon[1][i] = newMove

        textBox("",False,'')
    else:
        textBox("The new move "+str(newMove[0])+" was added",True,'')
        pokemon[1].append(newMove)
    return pokemon
def statusEffectCheck(MOVE,POKEMON): #haha balls theyre funny

    if MOVE[4] == 'powerUp':
        textBox(str(POKEMON[0][7])+ "'s attack was boosted",True,'')
        POKEMON[4][0] += .5
    return POKEMON


def overWorldMovement(map,team):
    global TEAM, RUN,PLAYER_SKIN,FAINTED,wonBattle,LEADER2

    moved = False
    key = 'none'
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                key = "w"
                PLAYER_SKIN = "Assets/player_back.png"
            if event.key == pygame.K_a:
                key = "a"
                PLAYER_SKIN = "Assets/player_left.png"
            if event.key == pygame.K_s:
                key = "s"
                PLAYER_SKIN = "Assets/player_front.png"
            if event.key == pygame.K_d:
                key = "d"
                PLAYER_SKIN = "Assets/player_right.png"
            if event.key == pygame.K_e:
                key = "e"

            if event.key == pygame.K_ESCAPE:
                key = 'menu'
            if event.key == pygame.K_t:
                key = 't'

        if event.type == pygame.QUIT:
            RUN = False







    rowCount = 0
    squareCount = 0
    playerLocation = ()
    for rowCount in range(len(map[0])):

        for squareCount in range(len(map[0][0])):

            if map[0][rowCount][squareCount] == "P":
                playerLocation = (rowCount,squareCount)
                if key == "w":
                    if squareCount != 0 and map[0][rowCount][squareCount-1] != "W"and map[0][rowCount][squareCount-1] != -1 and map[0][rowCount][squareCount-1] !="H":
                        map[0][rowCount][squareCount] = 0
                        map[0][rowCount][squareCount-1] = "P"
                        playerLocation = (rowCount, squareCount-1)
                    key = ''
                    moved = True
                elif key == "a":
                    if rowCount - 1 != -1 and map[0][rowCount-1][squareCount] != "W"and map[0][rowCount-1][squareCount] != -1 and map[0][rowCount-1][squareCount] !="H":

                        map[0][rowCount][squareCount] = 0
                        map[0][rowCount-1][squareCount] = "P"
                        playerLocation = (rowCount-1, squareCount)
                    key = ''
                    moved = True
                elif key == "s":

                    if squareCount != len(map[0][0]) - 1 and map[0][rowCount][squareCount+1] != "W" and map[0][rowCount][squareCount+1] != -1 and map[0][rowCount][squareCount+1] !="H":
                        map[0][rowCount][squareCount] = 0
                        map[0][rowCount][squareCount+1] = "P"
                        playerLocation = (rowCount, squareCount+1)
                    key = ''
                    moved = True
                elif key == "d":
                    if rowCount != len(map[0])-1 and map[0][rowCount+1][squareCount] != "W" and map[0][rowCount+1][squareCount] != -1 and map[0][rowCount+1][squareCount] !="H":

                        map[0][rowCount][squareCount] = 0
                        map[0][rowCount+1][squareCount] = "P"
                        playerLocation = (rowCount+1, squareCount)
                    key = ''
                    moved = True
    if key == "t":
        shop()
    if FAINTED:
        print("went to center?")
        tempMap = map
        map[0][playerLocation[0]][playerLocation[1]] = 0

        map = POKECENTER
        map[0][map[6][0]][map[6][1]] = "P"

        FAINTED = False




    for rowCount in range(len(map[0])):

        for squareCount in range(len(map[0][0])):

            if map[0][rowCount][squareCount] == "P":
                if checkTouching(map,rowCount,squareCount):
                    if key == "e":
                        for pokemoncount in range(len(team)):
                            textBox("Your Cale-mon were healed!",True,'')
                            team[pokemoncount] = healPokemon(team[pokemoncount],10000)

    viewingGrid = [[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1]]
    grassGrid = copy.deepcopy(viewingGrid)
    row = 0
    square = 0
    startingSquare = 0
    if playerLocation[0] <= 4:
        row = abs(playerLocation[0] - 4)
    squaresNeeded = 9
    if abs(playerLocation[1] - len(map[0][0]) ) <= 4:
        squaresNeeded = 3 + abs(playerLocation[1] - len(map[0][0]) - 1)

    if playerLocation[1] <= 4:
        square = abs(playerLocation[1] - 4)
        startingSquare = abs(playerLocation[1] - 4)
    for rowCount in range(len(map[0])):#x

        for squareCount in range(len(map[0][0])):#y

            if abs(rowCount - playerLocation[0]) <= 4 and abs(squareCount - playerLocation[1]) <= 4:
                viewingGrid[row][square] = map[0][rowCount][squareCount]
                grassGrid[row][square] = map[1][rowCount][squareCount]
                square += 1

                if square == squaresNeeded:
                    row += 1
                    square = startingSquare#bro im so fucking confused why not working like wtf dude this is so balls


    if moved:

        if map[1][playerLocation[0]][playerLocation[1]] == "G":
            print("IN GRASS")
            if random.randint(1,6) == 1:
                encounter = pokemonEncounter(map)
                TEAM = battleSequence(encounter,TEAM,encounter) #remember for each specific pokemon u need a deepcopy so they are own individual

        if map[1][playerLocation[0]][playerLocation[1]] == "D":
            map[0][playerLocation[0]][playerLocation[1]] = 0
            map = map[2]

            map[0][map[6][0]][map[6][1]] = "P"
            print(map,"MAP")
        elif map[1][playerLocation[0]][playerLocation[1]] == "D2":
            map[0][playerLocation[0]][playerLocation[1]] = 0
            tempMap = map
            print(map[4], "NEWMAP")
            map = map[4]
            print(map)
            print(map[4])
            map[4] = tempMap
            map[0][map[6][0]][map[6][1]] = "P"

            print(map,"MAP")
        elif map[1][playerLocation[0]][playerLocation[1]] == "D3":
            map[0][playerLocation[0]][playerLocation[1]] = 0
            tempMap = map
            print(map[5], "NEWMAP")
            map = map[5]
            print(map[5])
            map[5] = tempMap

            map[0][map[6][0]][map[6][1]] = "P"
            print(map, "MAP")
        elif map[1][playerLocation[0]][playerLocation[1]] == "L":
            leaderTeam = [copy.deepcopy(ETHANT),copy.deepcopy(STANISAURUS)]
            leaderTeam[0][0][3] = 11
            leaderTeam[1][0][3] = 13
            leaderTeam[0] = levelToStats(leaderTeam[0])
            leaderTeam[1] = levelToStats(leaderTeam[1])
            TEAM = battleSequence('', TEAM,
                                  leaderTeam)
            print(map[1][0][0],'testing')
            if wonBattle:


                map[2][1][0][0] = 'D3'
                textBox("Now, go to the top left of the map and enter the door",True,'')
                textBox("In that new area, there are new CALE-mon and a brand new leader to fight!",True,'')
                textBox("Good luck!",True,'')
        elif map[1][playerLocation[0]][playerLocation[1]] == "L2":

            TEAM = battleSequence('', TEAM,
                                  LEADER2)
            print(map[1][0][0], 'testing')
            #map[2][0][0][0] = "D3"


    if key == "menu":
        menu(TEAM)


    mapDisplay(viewingGrid,grassGrid)

    return map,team
def mapDisplay(map,grassGrid):
    global playerSkin


    backgroundPy = pygame.Surface((SCREEN_SIZE[0],SCREEN_SIZE[1]))
    backgroundPy.fill((0,0,100))
    SCREEN.blit(backgroundPy,(0,0))
    background = pygame.image.load("Assets/background.png")
    background = pygame.transform.scale(background,(SCREEN_SIZE[0]*2,SCREEN_SIZE[1]*2))
    SCREEN.blit(background,(0,0))
    yLocation = 0
    xLocation = 0
    for row in map:

        yLocation = 0
        for square in row:
            if square != -1:
                #squareDraw = Rectangle(Point(xLocation*66.6666,yLocation*66.6666),Point(xLocation*66.6666+66.6666,yLocation*66.6666+66.6666))
                #squareDraw.setFill('white')
                #squareDraw.draw(win)
                #squareTexture = Image(Point(xLocation*66.6666 + 33.3333,yLocation*66.6666+33.3333),"dirt.png").draw(win)

                squareTexturePy = pygame.image.load('Assets/moon.png')
                squareTexturePy = pygame.transform.scale(squareTexturePy,SQUARE_SCALE)
                SCREEN.blit(squareTexturePy,(xLocation*SQUARE_SCALE[0] ,yLocation*SQUARE_SCALE[1]))
                if grassGrid[xLocation][yLocation] == "G":
                    grassSprite = pygame.image.load("Assets/grass.png")
                    grassSprite = pygame.transform.scale(grassSprite, SQUARE_SCALE)
                    SCREEN.blit(grassSprite,(xLocation *SQUARE_SCALE[0], yLocation *SQUARE_SCALE[0]))
                    #grassTexture = Image(Point(xLocation*66.6666 + 33.3333,yLocation*66.6666+33.3333),"grass.png").draw(win)
                    pass
                if grassGrid[xLocation][yLocation] == "D" or grassGrid[xLocation][yLocation] == "D2" or grassGrid[xLocation][yLocation] == "D3":
                    grassSprite = pygame.image.load("Assets/door.png")
                    grassSprite = pygame.transform.scale(grassSprite, SQUARE_SCALE)
                    SCREEN.blit(grassSprite,(xLocation *SQUARE_SCALE[0], yLocation *SQUARE_SCALE[0]))
                    #grassTexture = Image(Point(xLocation*66.6666 + 33.3333,yLocation*66.6666+33.3333),"grass.png").draw(win)
                    pass
                if grassGrid[xLocation][yLocation] == "L":
                    grassSprite = pygame.image.load("Assets/leader.png")
                    grassSprite = pygame.transform.scale(grassSprite, SQUARE_SCALE)
                    SCREEN.blit(grassSprite,(xLocation *SQUARE_SCALE[0], yLocation *SQUARE_SCALE[0]))
                    #grassTexture = Image(Point(xLocation*66.6666 + 33.3333,yLocation*66.6666+33.3333),"grass.png").draw(win)
                    pass
                elif grassGrid[xLocation][yLocation] == "L2":
                    grassSprite = pygame.image.load("Assets/leader2.png")
                    grassSprite = pygame.transform.scale(grassSprite, SQUARE_SCALE)
                    SCREEN.blit(grassSprite,(xLocation *SQUARE_SCALE[0], yLocation *SQUARE_SCALE[0]))
                    #grassTexture = Image(Point(xLocation*66.6666 + 33.3333,yLocation*66.6666+33.3333),"grass.png").draw(win)
                    pass

                if square == "P":


                    playerTexture = pygame.image.load(PLAYER_SKIN)
                    playerTexture = pygame.transform.scale(playerTexture, SQUARE_SCALE)

                    SCREEN.blit(playerTexture, (xLocation *SQUARE_SCALE[0], yLocation *SQUARE_SCALE[0]))


                elif square == "W":
                    #wall = Image(Point(xLocation*66.6666 + 33.3333,yLocation*66.6666+33.3333),"wall.png").draw(win)
                    wallSprite = pygame.image.load("Assets/wall.png")
                    wallSprite = pygame.transform.scale(wallSprite, SQUARE_SCALE)
                    SCREEN.blit(wallSprite,(xLocation *SQUARE_SCALE[0], yLocation *SQUARE_SCALE[0]))
                    pass
                elif square == "H":
                    healSprite = pygame.image.load("Assets/healer.png")
                    healSprite = pygame.transform.scale(healSprite, SQUARE_SCALE)
                    SCREEN.blit(healSprite, (xLocation * SQUARE_SCALE[0], yLocation * SQUARE_SCALE[0]))




            yLocation += 1

        xLocation += 1
    pygame.display.flip()

def introScene():
    global TAG_NUM,STARTER_SCREEN
    STARTER_SCREEN = True
    startingScreen = pygame.image.load('Assets\IntroScreen.png')
    startingScreen = pygame.transform.scale(startingScreen,(SCREEN_SIZE[0],710/900*SCREEN_SIZE[0]))
    SCREEN.blit(startingScreen,(0,0))
    pygame.display.flip()
    textBox("Welcome to CALE-MON",True,'')
    startingScreen = pygame.image.load('Assets\StarterScreen.png')
    startingScreen = pygame.transform.scale(startingScreen, (SCREEN_SIZE[0], 710 / 900 * SCREEN_SIZE[0]))
    SCREEN.blit(startingScreen, (0, 0))
    pygame.display.flip()
    textBox("What CALE-MON will you choose?",True,'')
    pokemonChoice = displayBattle('','','','',["tsangar","chongar","bjangmon"],False,'',True)
    TEAM =[]
    if pokemonChoice == "tsangar":
        TEAM.append(copy.deepcopy(TSANGAR))
        TEAM[0][6] += TAG_NUM
        TAG_NUM += 1
    elif pokemonChoice == "bjangmon":
        TEAM.append(copy.deepcopy(BJANGMON))
        TEAM[0][6] += TAG_NUM
        TAG_NUM += 1
    else:
        TEAM.append(copy.deepcopy(CHONGAR))
        TEAM[0][6] += TAG_NUM
        TAG_NUM += 1

    TEAM[0] = levelToStats(TEAM[0])
    TEAM[0] = healPokemon(TEAM[0],10000)
    # TEAM.append(copy.deepcopy(CHONGAR))
    # TEAM[1][6] += TAG_NUM
    # TAG_NUM += 1
    # TEAM.append(copy.deepcopy(CHONGAR))
    # TEAM[2][6] += TAG_NUM
    #TAG_NUM += 1

    return TEAM

def pokemonEncounter(AREA):

    encounterInfo = AREA[3]

    encounter = copy.deepcopy(encounterInfo[0][random.randint(0,len(encounterInfo[0])-1)])
    print(encounterInfo)
    level = random.randint(encounterInfo[1][0],encounterInfo[1][1])

    encounter[0][3] = level
    encounter[3][3] = level
    encounter = levelToStats(encounter)
    encounterTeam = [encounter]
    return encounterTeam
RUN = True
TEAM = introScene()
def tutorial(AREA1,TEAM):
    AREA1, TEAM = overWorldMovement(AREA1, TEAM)
    textBox("Hey by the way, you can use 'WASD' to move!",True,'')
    textBox("Try going into that grass over "
            , True,"there and see what happens!")
    return AREA1
def tutorial2(AREA1,TEAM):

    AREA1,TEAM = overWorldMovement(AREA1,TEAM)
    textBox("Now, go to the little entrance at the top of the map! (use 'e' to heal!) ",True,'')
    return AREA1
def menu(TEAM):
    menuOpen = True
    while menuOpen:
        response = displayBattle('','','','',["CALEMON","PLACEGHOLDER","QUIT"],False,'',True)
        print(response)
        if response == "quit":
            menuOpen = False
        elif response == "calemon":

            temp,TEAM,placeholder = pokemonSwap(TEAM[0],TEAM,'','')
def checkTouching(map,rowCount,squareCount):

    try:
        if map[0][rowCount + 1][squareCount] == "H":
            touchingHealer = True

            return True

    except:
        pass
    try:
        if  map[0][rowCount - 1][squareCount] == "H":
            return True



    except:
        pass
    try:
        if  map[0][rowCount][
            squareCount + 1] == "H":

            return True


    except:
        pass
    try:
        if map[0][rowCount][squareCount - 1] == "H":

            return True


    except:
        pass
def evolutionCheck(pokemon):
    print(pokemon)
    if pokemon[5][0][1] != "none":
        if pokemon[0][3] >= pokemon[5][0][1]:
            answer = displayBattle(pokemon,'','','',["Yes","No"],False,"Do you want to evolve your Cale-mon?",True)
            if answer == "yes":
                oldPokemon = pokemon
                pokemon = pokemon[5][0][0]
                pokemon[1] = oldPokemon[1]

    return pokemon


AREA1=tutorial(AREA1,TEAM)
def shop():
    global CASH,INVENTORY,FIRST_SHOP
    inShop = True
    if FIRST_SHOP:
        textBox("Try buying a ball, then using it in battle with the 'throw' button!",True,'')
        textBox('Oh also the odds of catching a CALE-mon go up as their health goes down!',True,'')
        FIRST_SHOP = False
    while inShop:
        response = displayBattle('','','','',["5: RED BALL","15: BLUE BALL","BACK"],False,"What would you like to buy? (you have "+str(CASH)+" cash)",True)
        if response == "5: red ball":
            if CASH >= 5:
                CASH -= 5
                INVENTORY[0][1] += 1
                textBox("A red ball was bought!", True, '')
            else:
                textBox("You do not have enough cash.", True, '')
        elif response == "15: blue ball":
            if CASH >= 15:
                CASH -= 15
                INVENTORY[1][1] += 1
                textBox("A blue ball was bought!",True,'')
            else:
                textBox("You do not have enough cash.", True, '')
                print('not enough cash')
        elif response == "back":
            inShop = False

while RUN:
    # TEAM = battleSequence(copy.deepcopy(CHONGAR),TEAM,'') #remember for each specific pokemon u need a deepcopy so they are own individual
    # for pokemonCount in range(len(TEAM)):
    #     TEAM[pokemonCount] = healPokemon(TEAM[pokemonCount],100)
    AREA1,TEAM = overWorldMovement(AREA1,TEAM)



#TODO make moves able to learn, healing, better level scaling, text box that shows what is happening (like certain attacks or leveling)