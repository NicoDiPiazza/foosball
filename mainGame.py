from math import pi, sin
import pygame

pygame.init()

## function naming

def arrow(spot):
    spacingX = (tableWidth / Npaddles)
    tip = [tableStartX + spacingX * (spot + 0.5), tableStartY + tableHeight + (tableHeight/30)]
    br = [tableStartX + spacingX * (spot + 0.5) + (tableHeight/70), tableStartY + tableHeight + (tableHeight/10)]
    bl = [tableStartX + spacingX * (spot + 0.5) - (tableHeight/70), tableStartY + tableHeight + (tableHeight/10)]
    pygame.draw.polygon(screen, UpaddleColor, [tip, br, bl], 0)
    
# User paddle Coordinate generation

def newPaddleGen(spot, N, pW, order, depth):
    spacingX = (tableWidth / Npaddles)
    spacingY = tableHeight / (N + 1)
    
    paddleTL = [tableStartX + spacingX * (spot + 0.5) - paddleWidth / 2, tableStartY + (((order + 1) * spacingY) - (paddleHeight/2)) + depth]
    paddleTR = [(tableStartX + spacingX * (spot + 0.5) - paddleWidth / 2) + pW, tableStartY + (((order + 1) * spacingY) - (paddleHeight/2)) + depth]
    paddleBR = [(tableStartX + spacingX * (spot + 0.5) - paddleWidth / 2) + pW, (tableStartY + (((order + 1) * spacingY) - (paddleHeight/2))) + paddleHeight + depth]
    paddleBL = [tableStartX + spacingX * (spot + 0.5) - paddleWidth / 2, (tableStartY + (((order + 1) * spacingY) - (paddleHeight/2))) + paddleHeight + depth]

    paddleCoords = [paddleTL, paddleTR, paddleBR, paddleBL]
    return(paddleCoords)

## class initialization

class Collide():
    _registry = []
    # x, y, width, height, whether or not the object is being used
    def __init__(self, objX, objY, objWid, objHei, bool, name, type):
        self.objX = objX
        self.objY = objY
        self.objWid = objWid
        self.objHei = objHei
        self.objX = objX
        self.bool = bool
        self.type = type
        self._registry.append(name)

class Wall(Collide):
    thickness = 1
    wallOn = True



#screen parameters

screenWidth = 1000
screenHeight = 600
screen_size = [ screenWidth, screenHeight]

screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

pygame.event.get()
keys = pygame.key.get_pressed()

dt = 10

YELLOW = [255, 255, 0]



#the velocities of the ball in the X and Y directions respectively
ballVX = 0
ballVY = 0

# how much the ball slows down after a collision
ballSlowRate = 0.6
# how quickly the ball is served
serveSpeed = -1

paddleUnoFresh = 0
paddleDosFresh = 0
paddleTresFresh = 0
paddleQuatroFresh = 0

unoDepth = 0
dosDepth = 0
tresDepth = 0
quatroDepth = 0



while (keys[pygame.K_q] != True):
    pygame.event.get()
    keys = pygame.key.get_pressed()

    screenWidth = screen.get_width()
    screenHeight = screen.get_height()

    screenRatio = screenHeight / screenWidth

    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

## Calculations

    Collide._registry = []

# Table Calculations

    #table parameters

# ratio of table: width/length = 3/2
    tableRatio = 5/3
    #Horizontal table
    tableVert = False
    lookAtWidth = True
    if (screenHeight > screenWidth):
       #Vertical table
        tableVert = True
    if ((tableVert == False) and (screenRatio < tableRatio)) or ((tableVert == True) and ((screenRatio** (-1)) > tableRatio)):
       lookAtWidth = False

    if (tableVert == False and lookAtWidth == False):
        
        tableHeight = screenHeight * 1/2
        tableWidth = tableHeight * tableRatio
    if (tableVert == False and lookAtWidth == True):
        
        tableWidth = screenWidth * 5 / 6
        tableHeight = tableWidth * (tableRatio ** (-1))
    if (tableVert == True and lookAtWidth == False):
        
        tableHeight = screenHeight * 5 / 6
        tableWidth = tableHeight * (tableRatio ** (-1))
    if (tableVert == True and lookAtWidth == True):
        
        tableWidth = screenWidth * 1/2
        tableHeight = tableWidth * tableRatio

    tableStartX = (screenWidth / 2) - (tableWidth / 2)
    tableStartY = (screenHeight / 2) - (tableHeight / 2)

    tableCoords = [(tableStartX, tableStartY), (tableStartX + tableWidth, tableStartY), (tableStartX + tableWidth, tableStartY + tableHeight), (tableStartX, tableStartY + tableHeight)]

#game variables

## walls

    wallOne = Wall(tableStartX, tableStartY, Wall.thickness, tableHeight, Wall.wallOn, 'wallOne', 'wall')
    wallTwo = Wall(tableStartX, tableStartY, tableWidth, Wall.thickness, Wall.wallOn, 'wallTwo', 'wall')
    wallThree = Wall(tableStartX + tableWidth, tableStartY, Wall.thickness, tableHeight, Wall.wallOn, 'wallThree', 'wall')
    wallFour = Wall(tableStartX, tableStartY + tableHeight, tableWidth, Wall.thickness, Wall.wallOn, 'wallFour', 'wall')

#ball variables
    startBallX = screenWidth /2
    startBallY = screenHeight /2
    #size of ball, derived from d = 1/50 of the width of the table
    ballRad = tableWidth / 50

    if tableWidth < tableHeight:
        ballRad = tableHeight/50

# paddle variables

# how many total paddles are expected to be on the table
    Npaddles = 8
    testColor = [0, 0, 250]
    #color of the user's paddles
    UpaddleColor = (100, 100, 100)

#dimensions of the paddle for a horizontal table
    paddleHeight = ballRad *2
    paddleWidth = ballRad

#whether or not the paddle is selected
    paddleUnoOn = False
    paddleDosOn = False
    paddleTresOn = False
    paddleQuatroOn = False

#how many guys there are per pole
    NpartsUno = 1
    NpartsDos = 2
    NpartsTres = 5
    NpartsQuatro = 3

    if (tableVert):
        paddleWidth = tableWidth
        paddleHeight = tableHeight / Npaddles

## Game Logic

    if keys[pygame.K_a]:
        paddleUnoOn = True
    if keys[pygame.K_s]:
        paddleDosOn = True
    if keys[pygame.K_d]:
        paddleTresOn = True
    if keys[pygame.K_f]:
        paddleQuatroOn = True
    if keys[pygame.K_r]:
        if serveSpeed > -200:
            serveSpeed = serveSpeed - 1
        ballX = startBallX
        ballY = tableStartY + tableHeight - ballRad
        ballVX = 0
        
        ballVY = serveSpeed/(5 * dt)
    #ideally change this to a round guage, eventually
        bottomCoord = tableStartY + tableHeight
        guageCoord = [[tableStartX - tableWidth/5, bottomCoord + serveSpeed], [tableStartX - tableWidth/4, bottomCoord + serveSpeed], [tableStartX - tableWidth/4, bottomCoord], [tableStartX - tableWidth/5, bottomCoord]]
        pygame.draw.polygon(screen, YELLOW, guageCoord, 0)
    else:
        serveSpeed = 0

    if(paddleUnoOn):
        paddleUnoFresh = paddleUnoFresh + 1
        pUW = paddleWidth
        if paddleUnoFresh < 12:
            pUW = sin(pi * paddleUnoFresh / 4) * tableWidth / (2 * Npaddles)
        arrow(0)
        unoTop = newPaddleGen(0, NpartsUno, pUW, 0, unoDepth)[0][1] - tableStartY
        unoBottom = tableStartY + tableHeight - (newPaddleGen(0, NpartsUno, pUW, NpartsUno - 1, unoDepth)[0][1] + paddleHeight)
        if keys[pygame.K_UP] and unoTop > 0:
            unoDepth = unoDepth - tableHeight / 30
        if keys[pygame.K_DOWN] and unoBottom > 0:
            unoDepth = unoDepth + tableHeight / 30

    else:
        paddleUnoFresh = 0
        pUW = paddleWidth
    if(paddleDosOn):
        paddleDosFresh = paddleDosFresh + 1
        pDW = paddleWidth
        if paddleDosFresh < 12:
            pDW = sin(pi * paddleDosFresh / 4) * tableWidth / (2 * Npaddles)
        arrow(1)
        dosTop = newPaddleGen(0, NpartsDos, pDW, 0, dosDepth)[0][1] - tableStartY
        dosBottom = tableStartY + tableHeight - (newPaddleGen(0, NpartsDos, pDW, NpartsDos - 1, dosDepth)[0][1] + paddleHeight)
        if keys[pygame.K_UP] and dosTop > 0:
            dosDepth = dosDepth - tableHeight / 30
        if keys[pygame.K_DOWN] and dosBottom > 0:
            dosDepth = dosDepth + tableHeight / 30
    else:
        paddleDosFresh = 0
        pDW = paddleWidth
    if(paddleTresOn):
        paddleTresFresh = paddleTresFresh + 1
        pTW = paddleWidth
        if paddleTresFresh < 12:
            pTW = sin(pi * paddleTresFresh / 4) * tableWidth / (2 * Npaddles)
        arrow(3)
        tresTop = newPaddleGen(0, NpartsTres, pTW, 0, tresDepth)[0][1] - tableStartY
        tresBottom = tableStartY + tableHeight - (newPaddleGen(0, NpartsTres, pTW, NpartsTres - 1, tresDepth)[0][1] + paddleHeight)
        if keys[pygame.K_UP] and tresTop > 0:
            tresDepth = tresDepth - tableHeight / 30
        if keys[pygame.K_DOWN] and tresBottom > 0:
            tresDepth = tresDepth + tableHeight / 30
    else:
        paddleTresFresh = 0
        pTW = paddleWidth
    if(paddleQuatroOn):
        paddleQuatroFresh = paddleQuatroFresh + 1
        pQW = paddleWidth
        if paddleQuatroFresh < 12:
            pQW = sin(pi * paddleQuatroFresh / 4) * tableWidth / (2 * Npaddles)
        arrow(5)
        quatroTop = newPaddleGen(0, NpartsQuatro, pQW, 0, quatroDepth)[0][1] - tableStartY
        quatroBottom = tableStartY + tableHeight - (newPaddleGen(0, NpartsQuatro, pQW, NpartsQuatro - 1, quatroDepth)[0][1] + paddleHeight)
        if keys[pygame.K_UP] and quatroTop > 0:
            quatroDepth = quatroDepth - tableHeight / 30
        if keys[pygame.K_DOWN] and quatroBottom > 0:
            quatroDepth = quatroDepth + tableHeight / 30
    else:
        paddleQuatroFresh = 0
        pQW = paddleWidth


    class Uno(Collide):
        time = paddleUnoFresh

    class Dos(Collide):
        time = paddleDosFresh

    class Tres(Collide):
        time = paddleTresFresh

    class Quatro(Collide):
        time = paddleQuatroFresh


#making the colliding parts of the paddles

    unoGenZero = newPaddleGen(0, NpartsUno, pUW, 0, unoDepth)[0]
    unoFirstCol = Uno(unoGenZero[0], unoGenZero[1], pUW, paddleHeight, paddleUnoOn, 'unoFirstCol', 'paddle')

    dosGenZero = newPaddleGen(1, NpartsDos, pDW, 0, dosDepth)[0]
    dosFirstCol = Dos(dosGenZero[0], dosGenZero[1], pDW, paddleHeight, paddleDosOn, 'dosFirstCol', 'paddle')
    dosGenOne = newPaddleGen(1, NpartsDos, pDW, 1, dosDepth)[0]
    dosSecondCol = Dos(dosGenOne[0], dosGenOne[1], pDW, paddleHeight, paddleDosOn, 'dosSecondCol', 'paddle')

    tresGenZero = newPaddleGen(3, NpartsTres, pTW, 0, tresDepth)[0]
    tresFirstCol = Tres(tresGenZero[0], tresGenZero[1], pTW, paddleHeight, paddleTresOn, 'tresFirstCol', 'paddle')
    tresGenOne = newPaddleGen(3, NpartsTres, pTW, 1, tresDepth)[0]
    tresSecondCol = Tres(tresGenOne[0], tresGenOne[1], pTW, paddleHeight, paddleTresOn, 'tresSecondCol', 'paddle')
    tresGentwo = newPaddleGen(3, NpartsTres, pTW, 2, tresDepth)[0]
    tresThirdCol = Tres(tresGentwo[0], tresGentwo[1], pTW, paddleHeight, paddleTresOn, 'tresThirdCol', 'paddle')
    tresGenthree = newPaddleGen(3, NpartsTres, pTW, 3, tresDepth)[0]
    tresFourthCol = Tres(tresGenthree[0], tresGenthree[1], pTW, paddleHeight, paddleTresOn, 'tresFourthCol', 'paddle')
    tresGenFour = newPaddleGen(3, NpartsTres, pTW, 4, tresDepth)[0]
    tresFifthCol = Tres(tresGenFour[0], tresGenFour[1], pTW, paddleHeight, paddleTresOn, 'tresFifthCol', 'paddle')

    quatroGenZero = newPaddleGen(5, NpartsQuatro, pQW, 0, quatroDepth)[0]
    quatroFirstCol = Quatro(quatroGenZero[0], quatroGenZero[1], pQW, paddleHeight, paddleQuatroOn, 'quatroFirstCol', 'paddle')
    quatroGenOne = newPaddleGen(5, NpartsQuatro, pQW, 1, quatroDepth)[0]
    quatroSecondCol = Quatro(quatroGenOne[0], quatroGenOne[1], pQW, paddleHeight, paddleQuatroOn, 'quatroSecondCol', 'paddle')
    quatroGenTwo = newPaddleGen(5, NpartsQuatro, pQW, 2, quatroDepth)[0]
    quatroThirdCol = Quatro(quatroGenTwo[0], quatroGenTwo[1], pQW, paddleHeight, paddleQuatroOn, 'quatroThirdCol', 'paddle')






# ball bouncing of colliders

    if 'ballX' in locals() and 'ballY' in locals():
        ballX = ballX + ballVX
        ballY = ballY + ballVY
    else:
        ballX = startBallX
        ballY = startBallY

    canFlipX = True
    canFlipY = True
    mightCollideX = False
    canCollideX = False
    for i in Collide._registry:
        if ballY > eval(i).objY - ballRad and ballY < eval(i).objY + eval(i).objHei + ballRad:
            canCollideX = True
        else:
            canCollideX = False

        if ballX - ballRad < eval(i).objX + eval(i).objWid and ballX + ballRad > eval(i).objX + eval(i).objWid:
            mightCollideX = True
        else:
            mightCollideX = False
        if mightCollideX and canCollideX and eval(i).bool and canFlipX:
            if ballVX > 0:
                ballX = eval(i).objX - ballRad
            else:
                ballX = eval(i).objX + eval(i).objWid + ballRad
            ballVX = - ballVX
            canFlipX = False
            ballVX = ballVX * ballSlowRate
            if eval(i).type == 'paddle':
                if eval(i).time <= 5:
                    ballX = eval(i).objX + eval(i).objWid + 1
                    if ballVX < 0:
                        ballVX = - ballVX 
                    ballVX = ballVX + 5 - eval(i).time

        if eval(i).type == 'wall':
            if ballY + ballRad >tableStartY + tableHeight:
                ballVY = - 0.9 *ballVY
                ballY = tableStartY + tableHeight - ballRad
                
            if ballY - ballRad < tableStartY:
                ballVY = - 0.9 * ballVY
                ballY = tableStartY + ballRad
                
            
            

## Displays

    pygame.draw.polygon(screen, (0, 250, 0), tableCoords, 0)
    pygame.draw.circle(screen, (250, 250, 250), [ballX, ballY], ballRad, 0)

# displaying the paddles
    for i in range(NpartsUno):
        pygame.draw.polygon(screen, testColor, newPaddleGen(0, NpartsUno, pUW, i, unoDepth), 0)
    for i in range(NpartsDos):
        pygame.draw.polygon(screen, testColor, newPaddleGen(1, NpartsDos, pDW, i, dosDepth), 0)
    for i in range(NpartsTres):
        pygame.draw.polygon(screen, testColor, newPaddleGen(3, NpartsTres, pTW, i, tresDepth), 0)
    for i in range(NpartsQuatro):
        pygame.draw.polygon(screen, testColor, newPaddleGen(5, NpartsQuatro, pQW, i, quatroDepth), 0)

    pygame.time.delay(dt)
    pygame.display.update()
