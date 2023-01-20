import random
import copy
from graphics import *
import pygame
pygame.init()
win = GraphWin('pokemon',600,600)
SCREEN_SIZE = (603,603)#Multiple of 9
SQUARE_SCALE = (SCREEN_SIZE[0] // 9,SCREEN_SIZE[1] // 9)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
FIRE = ['fire','grass','water']#first is name, then what its super effective against, then what its weak to
WATER = ['water','fire','grass']
GRASS = ['grass','water','fire']
NORMAL = ['normal','none','none']
font = pygame.font.Font('freesansbold.ttf', 42)



FIRE_BITE = ['fire bite',30,FIRE,1.0,'none']#[0] = move name, power, type, accuracy, then stat boost or effect (not always there)
WATER_SUCK = ['water suck',30,WATER,1.0,'none']
GRASS_GUN = ['grass gun',30,GRASS,1.0,'none']
WHACK = ['whack',15,NORMAL,1.0,'none']
BLOW = ["blow",50,NORMAL,1.0,'none']
GYM = ['gym',0, FIRE,1.0,'powerUp']


#TSANGAR
TSANGAR = [[5,5,90,5,90,FIRE,True,'tsangar',32],[FIRE_BITE,WHACK,GYM],[(BLOW,6),(BLOW,7),(BLOW,8)],[5,5,90,5,90,FIRE,True,'tsangar'],[1,1]] #for stats, first attack, then speed, then health, then level, then current Health, then typing, then if alive or not, then xp. Next is current movepool. Next is available moves to learn with corresponding level (tuple). Next is base stats (copy of first stats but doesnt change). Next is stat boosts during a battle (attack then speed)
CHONGAR = [[5,5,90,5,90,WATER,True,'chongar',32],[WATER_SUCK,WHACK],[],[5,5,90,5,90,WATER,True,'chongar'],[1,1]]
BJANGMON = [[5,5,90,5,90,GRASS,True,'bjangmon',32],[GRASS_GUN,WHACK],[(BLOW,6),(BLOW,7),(BLOW,8)],[5,5,90,5,90,GRASS,True,'bjangmon'],[1,1]]
STANISAURUS = [[5,5,90,5,90,FIRE,True,'stanisaurus',32],[GRASS_GUN,WHACK],[(BLOW,6),(BLOW,7),(BLOW,8)],[8,5,90,5,90,GRASS,True,'stanisaurus'],[1,1]]
ETHANT = [[5,5,90,5,90,NORMAL,True,'ethant',32],[GRASS_GUN,WHACK],[(BLOW,6),(BLOW,7),(BLOW,8)],[8,5,90,5,90,NORMAL,True,'ethant'],[1,1]]
TEAM = [copy.deepcopy(TSANGAR)]










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
AREA1ENCOUNTERS = [[ETHANT,STANISAURUS],(3,6)]#first is pokemon, then level range
AREA1 = []
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
         [0,0,0,"P",0,0]],

         AREA1

         ]
AREA1 = [[[0,0,0,0,0,0,'W','W','W','W','W'],
         [0,0,0,0,0,0,'W','W','W','W','W'],
         [0,0,0,0,0,0,'W','W','W','W','W'],
         [0,0,0,0,0,0,'W','W','D','W','W'],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,"P",0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0]],[],AREA2,AREA1ENCOUNTERS]#first is actual grid, then is grass grid, then is the area it teleports to, then the area spawns
AREA2[2] = AREA1


AREA1[1] = copy.deepcopy(AREA1[0])
for i in range(11):
    for j in range(3):
        AREA1[1][j+9][i] = "G"
print(AREA1)





def battleSequence(enemyPokemon,currentTeam,enemyTeam):
    global battleOver

    textBox('',False)
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
    learnMoveCount = 0
    for learnableMove in currentTeam[0][2]:
        if learnableMove[1] == currentTeam[0][0][3]: #FIX LEARN NEW MOVE, MAKE ONLY LEVEL UP WHEN WIN
            currentTeam[0] = learnNewMove(currentTeam[0],learnableMove[0],currentTeam)
            currentTeam[0][2][learnMoveCount] = (learnableMove[0],0)
            learnMoveCount += 1

    for i in range(len(currentPokemon[4])): #resetting stat boosts
        currentPokemon[4][i] = 1
    return(currentTeam)


def defendingPlayerTurn(currentPokemon,enemyPokemon,currentTeam,enemyTeam):
    global battleOver
    print("Your pokemon is",currentPokemon, "and the enemy pokemon is",enemyPokemon)
    chosenAction = displayBattle(currentPokemon, enemyPokemon, currentTeam, enemyTeam, ['ATTACK', 'SWITCH', 'THROW'],True,'',True)
    #chosenAction = input("Choose an action, [ATTACK, SWITCH, THROW]").lower()  # later will work with a screen input







    if chosenAction == 'attack':
        MOVES = []
        for MOVE in currentPokemon[1]:

            MOVES.append(MOVE[0])
        chosenMove = displayBattle(currentPokemon, enemyPokemon, currentTeam, enemyTeam, MOVES,True,'',True)
        #chosenMove = input("Choose a move " + str(MOVES)).lower()





        for MOVE in currentPokemon[1]:
            moveName = MOVE[0]
            moveDamage = MOVE[1]
            if moveName == chosenMove:
                currentPokemonDamageDealt,currentPokemon = damageCalc(currentPokemon[0], MOVE, enemyPokemon[
                    0],currentPokemon)  # finds how much damage should be dealt,inputs the stats
                enemyPokemon[0][4] -= currentPokemonDamageDealt



                print("the move", moveName, "was chosen and", currentPokemonDamageDealt, "damage was dealt.")
                textBox(moveName + " dealt " + str(currentPokemonDamageDealt),True)
                if enemyPokemon[0][4] <= 0:
                    enemyPokemon[0][4] = 0
                    enemyPokemon[0][6] = False
                    numOfAlivePokemon = 0
                    for POKEMON in enemyTeam:
                        if POKEMON[0][6]:
                            numOfAlivePokemon += 1
                    if numOfAlivePokemon == 0:
                        print("battle over")
                        textBox('You won!',True)
                        currentTeam[0][0][3] += 1
                        battleOver = True
                    else:
                        enemyChoices = []
                        for pokemonOption in enemyTeam:
                            if pokemonOption[0][4] != 0:
                                enemyChoices.append(pokemonOption)
                        pokemonChoice = enemyChoices[random.randint(0,len(enemyChoices)-1)]
                        textBox("the enemy's " + enemyPokemon[0][7]+" fainted and "+pokemonChoice[0][7]+ " was switched in",True)
                        enemyPokemon = pokemonChoice
    elif chosenAction == 'switch':
        currentPokemon, currentTeam = pokemonSwap(currentPokemon,currentTeam,enemyPokemon,enemyTeam)
    elif chosenAction == "throw":
        caught = catchChanceCalc("red",enemyPokemon[0][2],enemyPokemon[0][4])
        if caught:
            textBox('the pokemon was caught!',True)
            print('the pokemon was caught!')
            battleOver = True
            currentTeam.append(enemyPokemon)
        else:
            textBox('the pokemon broke free!',True)
            print('the pokemon broke free!')
    return currentPokemon,enemyPokemon,currentTeam,enemyTeam


def enemyPlayerTurn(currentPokemon,enemyPokemon,currentTeam,enemyTeam):
    global battleOver

    enemyMoveChoices = enemyPokemon[1]
    enemyMoveChoice = enemyMoveChoices[random.randint(0, len(enemyMoveChoices) - 1)]

    enemyDamageDealt,enemyPokemon = damageCalc(enemyPokemon[0], enemyMoveChoice,
                                  currentPokemon[0],enemyPokemon)  # finds how much damage should be dealt
    currentPokemon[0][4] -= enemyDamageDealt
    textBox('The enemy pokemon used ' + enemyMoveChoice[0] + " and " + str(enemyDamageDealt) + " was dealt.",True)
    print("the enemy move", enemyMoveChoice[0], "was chosen and", enemyDamageDealt, "damage was dealt.")


    if currentPokemon[0][4] <= 0:
        currentPokemon[0][4] = 0
        currentPokemon[0][6] = False
        numOfAlivePokemon = 0
        for POKEMON in currentTeam:
            if POKEMON[0][6]:
                numOfAlivePokemon += 1
        if numOfAlivePokemon == 0:
            print("battle over")
            textBox('You lost.',True)
            battleOver = True
        else:
            print("your pokemon fainted lol")
            textBox('choose the next pokemon',True)
            currentPokemon, currentTeam = pokemonSwap(currentPokemon, currentTeam,enemyPokemon,enemyTeam)

    return currentPokemon, enemyPokemon, currentTeam, enemyTeam

def damageCalc(STATS,MOVE,DEFENDINGSTATS,POKEMON):
    POKEMON = statusEffectCheck(MOVE,POKEMON)
    enemyType = DEFENDINGSTATS[5]
    attackMult = (STATS[0]**2/150) + 1

    if MOVE[2][0] == enemyType[2]:
        print('it was super effective!')
        superEffectiveMult = 2
    else:
        superEffectiveMult = 1
    attackDamage = (MOVE[1] * superEffectiveMult * attackMult * POKEMON[4][0])//1

    return attackDamage,POKEMON
def catchChanceCalc(BALLUSED,DEFENDINGHP,DEFENDINGMAXHP,):
    if BALLUSED == 'red':
        odds = (((DEFENDINGMAXHP - DEFENDINGHP) / DEFENDINGMAXHP)+ 1 * 1/2) *100
        if random.randint(1,100) <= odds:
            return True
        else:
            return False


def pokemonSwap(currentPokemon,currentTeam,enemyPokemon,enemyTeam):


    listOfPokemon = []
    for pokemon in currentTeam:

        listOfPokemon.append(pokemon[0][7])

    pokemonSelection = displayBattle(currentPokemon, enemyPokemon, currentTeam, enemyTeam, listOfPokemon,True,'',True)
    #pokemonSelection = input("what pokemon do u want to switch " + str(listOfPokemon))
    count = 0
    for POKEMON in currentTeam:
        if POKEMON[0][7] == pokemonSelection and POKEMON[0][6]:
            tempPokemon = currentPokemon
            currentPokemon = POKEMON
            currentTeam[count] = tempPokemon
            count += 1
    return currentPokemon, currentTeam
def displayBattle(currentPokemon,enemyPokemon,currentTeam,enemyTeam,text,displayHealth,prompt,wait):
    global win, SCREEN
    prevOption = ''
    prevSelectedPy = ''
    clear = Rectangle(Point(0,0),Point(600,400))

    clearPy = pygame.Surface((SCREEN_SIZE[0],SCREEN_SIZE[1] - SCREEN_SIZE[0]//450))
    clearPy.fill((245,240,240))
    SCREEN.blit(clearPy,(0,0))

    clear.setFill('white')

    clear.draw(win)
    textBox(prompt, False)
    ran = 0
    for OPTION in text:
        optionDraw = Text(Point(5/9 * SCREEN_SIZE[0], 2/9*SCREEN_SIZE[0] + (ran * 60)), OPTION)#500, 200+RAN*60
        optionDraw.setSize(25)

        newFont = pygame.font.Font('freesansbold.ttf', int(42/900 * SCREEN_SIZE[0])//1)
        textPy = newFont.render(OPTION, True, (10, 50, 50),(100, 100, 100))  # first color is text, second if rectangle color

        optionDrawPy = textPy.get_rect()
        optionDrawPy.center = (8/9*SCREEN_SIZE[0],330/900 * SCREEN_SIZE[0] + (ran*90/900*SCREEN_SIZE[0]))
        SCREEN.blit(textPy, optionDrawPy)
        pygame.display.flip()

        optionDraw.draw(win)
        ran += 1

    if displayHealth:
        healthDisplay(currentPokemon[0][4],currentPokemon[0][2],(100/900*SCREEN_SIZE[0],550/900*SCREEN_SIZE[0]),(400/900*SCREEN_SIZE[0],580/900*SCREEN_SIZE[0]),currentPokemon)
        healthDisplay(enemyPokemon[0][4], enemyPokemon[0][2], (500/900*SCREEN_SIZE[0], 200/900*SCREEN_SIZE[0]),(800/900*SCREEN_SIZE[0], 230/900*SCREEN_SIZE[0]), enemyPokemon)
    pygame.display.flip()
    optionNotSelected = True
    if wait:
        while optionNotSelected:

            SCREEN.blit(clearPy, (0, 0))
            textBox(prompt, False)
            if displayHealth:
                healthDisplay(currentPokemon[0][4], currentPokemon[0][2],
                              (100 / 900 * SCREEN_SIZE[0], 550 / 900 * SCREEN_SIZE[0]),
                              (400 / 900 * SCREEN_SIZE[0], 580 / 900 * SCREEN_SIZE[0]), currentPokemon)
                healthDisplay(enemyPokemon[0][4], enemyPokemon[0][2],
                              (500 / 900 * SCREEN_SIZE[0], 200 / 900 * SCREEN_SIZE[0]),
                              (800 / 900 * SCREEN_SIZE[0], 230 / 900 * SCREEN_SIZE[0]), enemyPokemon)
            mouseClick = False
            mouse = win.checkMouse()
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

                        newFont = pygame.font.Font('freesansbold.ttf', int(42 / 900 * SCREEN_SIZE[0]) // 1)
                        textPy = newFont.render(OPTION, True, (10, 50, 50),
                                                (200, 200, 200))  # first color is text, second if rectangle color

                        optionDrawPy = textPy.get_rect()
                        optionDrawPy.center = (
                        8 / 9 * SCREEN_SIZE[0], 330 / 900 * SCREEN_SIZE[0] + (ran * 90 / 900 * SCREEN_SIZE[0]))




                        SCREEN.blit(textPy, optionDrawPy)
                        if OPTION == prevSelectedPy:
                            return (OPTION).lower()
                        prevSelectedPy = OPTION


                    else:
                        newFont = pygame.font.Font('freesansbold.ttf', int(42 / 900 * SCREEN_SIZE[0]) // 1)
                        textPy = newFont.render(OPTION, True, (10, 50, 50),
                                                (100, 100, 100))  # first color is text, second if rectangle color

                        optionDrawPy = textPy.get_rect()
                        optionDrawPy.center = (
                        8 / 9 * SCREEN_SIZE[0], 330 / 900 * SCREEN_SIZE[0] + (ran * 90 / 900 * SCREEN_SIZE[0]))



                        SCREEN.blit(textPy, optionDrawPy)





                    ran += 1
                pygame.display.flip()




            if mouse != None:
                clear = Rectangle(Point(0, 0), Point(600, 400))
                clear.setFill('white')
                clear.draw(win)


                mouseX = mouse.getX() / 60
                mouseY = mouse.getY() / 60


                ran = 0
                if displayHealth:
                    healthDisplay(currentPokemon[0][4], currentPokemon[0][2], (50, 350), (350, 370),currentPokemon)
                    healthDisplay(enemyPokemon[0][4], enemyPokemon[0][2], (250, 100), (550, 120), enemyPokemon)
                for OPTION in text:
                    optionDraw = Text(Point(500, 200 + (ran * 60)), OPTION)
                    optionDraw.setSize(25)
                    optionDraw.draw(win)
                    print(mouseX,mouseY)
                    if mouseX >= 7 and mouseX <= 9 and mouseY >= ran + 3 and mouseY <= ran + 4:
                        optionDraw.setFill("green")

                        if prevOption == OPTION:

                            return (OPTION).lower()
                        prevOption = OPTION
                    else:
                        optionDraw.setFill("black")
                    ran += 1
                update(10)
    clear = Rectangle(Point(0, 0), Point(600, 600))
    clear.setFill('white')
    clear.draw(win)



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



    newFont = pygame.font.Font('freesansbold.ttf', int(20 / 900 * SCREEN_SIZE[0]) // 1)
    textPy = newFont.render(("lvl "+str(pokemon[0][3])+" "+pokemon[0][7] +" "+ str(pokemonHealth)+"/"+str(pokemonMaxHp)), True, (10, 50, 50),
                            (200, 200, 200))  # first color is text, second if rectangle color

    optionDrawPy = textPy.get_rect()
    optionDrawPy.center = (point1[0]+(point2[0] - point1[0])/2,point1[1]-10)

    SCREEN.blit(textPy, optionDrawPy)









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
    POKEMON[0][0] = POKEMON[3][0] + (POKEMON[0][3] / 5)
    POKEMON[0][1] = POKEMON[3][1] + (POKEMON[0][3] / 2.5)
    POKEMON[0][2] = POKEMON[3][2] + (POKEMON[0][3] )
    POKEMON[0][4] = POKEMON[3][4] + (POKEMON[0][3])
    return POKEMON
def healPokemon(pokemon,healAmount):
    pokemon[0][4] += healAmount
    if pokemon[0][4] > pokemon[0][2]:
        pokemon[0][4] = pokemon[0][2]
    return pokemon
def textBox(text,wait):
    clearPy = pygame.Surface((SCREEN_SIZE[0],200/900 * SCREEN_SIZE[0]))
    clearPy.fill((250,250,250))
    SCREEN.blit(clearPy,(0,700/900 * SCREEN_SIZE[0]))

    newFont = font = pygame.font.Font('freesansbold.ttf', int((24/900 * SCREEN_SIZE[0])//1))
    textPy = newFont.render(text, True, (10, 50, 50),
                         (200, 200, 200))
    optionDrawPy = textPy.get_rect()

    optionDrawPy.center = ((SCREEN_SIZE[0] / 2,SCREEN_SIZE[0] - 100/900 * SCREEN_SIZE[0]))
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

        textBox("",False)
    else:
        textBox("The new move "+str(newMove[0])+" was added",True)
        pokemon[1].append(newMove)
    return pokemon
def statusEffectCheck(MOVE,POKEMON): #haha balls theyre funny
    if MOVE[4] == 'powerUp':
        textBox(str(POKEMON[0][7])+ "'s attack was boosted",True)
        POKEMON[4][0] += .5
    return POKEMON


def overWorldMovement(map):
    global TEAM, RUN
    key = win.checkKey()
    moved = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                key = "w"
            if event.key == pygame.K_a:
                key = "a"
            if event.key == pygame.K_s:
                key = "s"
            if event.key == pygame.K_d:
                key = "d"
            if event.key == pygame.K_ESCAPE:
                RUN = False
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
                    if squareCount != 0 and map[0][rowCount][squareCount-1] != "W"and map[0][rowCount][squareCount-1] != -1:
                        map[0][rowCount][squareCount] = 0
                        map[0][rowCount][squareCount-1] = "P"
                        playerLocation = (rowCount, squareCount-1)
                    key = ''
                    moved = True
                elif key == "a":
                    if rowCount - 1 != -1 and map[0][rowCount-1][squareCount] != "W"and map[0][rowCount-1][squareCount] != -1:

                        map[0][rowCount][squareCount] = 0
                        map[0][rowCount-1][squareCount] = "P"
                        playerLocation = (rowCount-1, squareCount)
                    key = ''
                    moved = True
                elif key == "s":
                    print("moved down")
                    if squareCount != len(map[0][0]) - 1 and map[0][rowCount][squareCount+1] != "W" and map[0][rowCount][squareCount+1] != -1:
                        map[0][rowCount][squareCount] = 0
                        map[0][rowCount][squareCount+1] = "P"
                        playerLocation = (rowCount, squareCount+1)
                    key = ''
                    moved = True
                elif key == "d":
                    if rowCount != len(map[0])-1 and map[0][rowCount+1][squareCount] != "W" and map[0][rowCount+1][squareCount] != -1:

                        map[0][rowCount][squareCount] = 0
                        map[0][rowCount+1][squareCount] = "P"
                        playerLocation = (rowCount+1, squareCount)
                    key = ''
                    moved = True

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
        print("ran")
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
                for pokemonCount in range(len(TEAM)):
                    TEAM[pokemonCount] = healPokemon(TEAM[pokemonCount],100)
        if map[1][playerLocation[0]][playerLocation[1]] == "D":
            map = map[2]
            print(map,"MAP")
        elif map[1][playerLocation[0]][playerLocation[1]] == "L":
            leaderTeam = [copy.deepcopy(ETHANT),copy.deepcopy(STANISAURUS)]
            leaderTeam[0][0][3] = 11
            leaderTeam[1][0][3] = 13
            TEAM = battleSequence('', TEAM,
                                  leaderTeam)




    mapDisplay(viewingGrid,grassGrid)

    return (map)
def mapDisplay(map,grassGrid):
    background = Rectangle(Point(0,0),Point(600,600))
    background.setFill("blue")
    background.draw(win)

    backgroundPy = pygame.Surface((900,900))
    backgroundPy.fill((0,0,100))
    SCREEN.blit(backgroundPy,(0,0))
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

                squareTexturePy = pygame.image.load('moon.png')
                squareTexturePy = pygame.transform.scale(squareTexturePy,SQUARE_SCALE)
                SCREEN.blit(squareTexturePy,(xLocation*SQUARE_SCALE[0] ,yLocation*SQUARE_SCALE[1]))
                if grassGrid[xLocation][yLocation] == "G":
                    grassSprite = pygame.image.load("grass.png")
                    grassSprite = pygame.transform.scale(grassSprite, SQUARE_SCALE)
                    SCREEN.blit(grassSprite,(xLocation *SQUARE_SCALE[0], yLocation *SQUARE_SCALE[0]))
                    #grassTexture = Image(Point(xLocation*66.6666 + 33.3333,yLocation*66.6666+33.3333),"grass.png").draw(win)
                    pass
                if grassGrid[xLocation][yLocation] == "D":
                    grassSprite = pygame.image.load("door.png")
                    grassSprite = pygame.transform.scale(grassSprite, SQUARE_SCALE)
                    SCREEN.blit(grassSprite,(xLocation *SQUARE_SCALE[0], yLocation *SQUARE_SCALE[0]))
                    #grassTexture = Image(Point(xLocation*66.6666 + 33.3333,yLocation*66.6666+33.3333),"grass.png").draw(win)
                    pass
                if grassGrid[xLocation][yLocation] == "L":
                    grassSprite = pygame.image.load("leader.png")
                    grassSprite = pygame.transform.scale(grassSprite, SQUARE_SCALE)
                    SCREEN.blit(grassSprite,(xLocation *SQUARE_SCALE[0], yLocation *SQUARE_SCALE[0]))
                    #grassTexture = Image(Point(xLocation*66.6666 + 33.3333,yLocation*66.6666+33.3333),"grass.png").draw(win)
                    pass

                if square == "P":

                    player = Image(Point(xLocation*100 + 50,yLocation*100+50),"player.png").draw(win)
                    playerTexture = pygame.image.load('player.png')
                    playerTexture = pygame.transform.scale(playerTexture, SQUARE_SCALE)

                    SCREEN.blit(playerTexture, (xLocation *SQUARE_SCALE[0], yLocation *SQUARE_SCALE[0]))


                elif square == "W":
                    #wall = Image(Point(xLocation*66.6666 + 33.3333,yLocation*66.6666+33.3333),"wall.png").draw(win)
                    wallSprite = pygame.image.load("wall.png")
                    wallSprite = pygame.transform.scale(wallSprite, SQUARE_SCALE)
                    SCREEN.blit(wallSprite,(xLocation *SQUARE_SCALE[0], yLocation *SQUARE_SCALE[0]))
                    pass




            yLocation += 1

        xLocation += 1
    pygame.display.flip()
def introScene():
    textBox("Welcome to CALE-MON",True)
    textBox("What CALE-MON will you choose?",True)
    pokemonChoice = displayBattle('','','','',["tsangar","chongar","bjangmon"],False)
    if pokemonChoice == "tsangar":
        TEAM = [(copy.deepcopy(TSANGAR))]
    elif pokemonChoice == "bjangmon":
        TEAM = [copy.deepcopy(BJANGMON)]
    else:
        TEAM = [copy.deepcopy(CHONGAR)]
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

while RUN:
    # TEAM = battleSequence(copy.deepcopy(CHONGAR),TEAM,'') #remember for each specific pokemon u need a deepcopy so they are own individual
    # for pokemonCount in range(len(TEAM)):
    #     TEAM[pokemonCount] = healPokemon(TEAM[pokemonCount],100)
    AREA1 = overWorldMovement(AREA1)
    update(10)


#TODO make moves able to learn, healing, better level scaling, text box that shows what is happening (like certain attacks or leveling)