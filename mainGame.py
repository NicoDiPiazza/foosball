from math import sqrt
import pygame

pygame.init()

## function naming

# User paddle Coordinate generation

def paddleGen(spot):
    
    paddleCoords = [((paddleWidth * spot) + tableStartX, tableStartY), ((paddleWidth * ( spot + 1)) + tableStartX, tableStartY)]
    if tableVert:
        paddleCoords = [(tableStartX, (paddleHeight * spot) + tableStartY), (tableStartX, (paddleHeight * ( spot + 1)) + tableStartY)]
    bottomCoords =((paddleWidth * (spot + 1)) + tableStartX, tableStartY + tableHeight)
    if tableVert:
        bottomCoords =(tableStartX + tableWidth, (paddleHeight * (spot + 1)) + tableStartY)
    finalCoords = ((paddleWidth * spot) + tableStartX, tableStartY + tableHeight)
    if tableVert:
        finalCoords = (tableStartX + tableWidth, (paddleHeight * spot) + tableStartY)
    paddleCoords.append(bottomCoords)
    paddleCoords.append(finalCoords)
    return paddleCoords

## class initialization


class Collide():
    _registry = []
    # x, y, width, height, whether or not the object is being used
    def __init__(self, objX, objY, objWid, objHei, bool, name):
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


ballVX = 0
ballVY = 0

ballSlowRate = 0.6

serveSpeed = -1

paddleUnoFresh = 0
paddleDosFresh = 0
paddleTresFresh = 0
paddleQuatroFresh = 0





while (keys[pygame.K_q] != True):
    pygame.event.get()
    keys = pygame.key.get_pressed()

    screenWidth = screen.get_width()
    screenHeight = screen.get_height()

    screenRatio = screenHeight / screenWidth


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

    wallOne = Wall(tableStartX, tableStartY, Wall.thickness, tableHeight, Wall.wallOn, 'wallOne')
    wallTwo = Wall(tableStartX, tableStartY, tableWidth, Wall.thickness, Wall.wallOn, 'wallTwo')
    wallThree = Wall(tableStartX + tableWidth, tableStartY, Wall.thickness, tableHeight, Wall.wallOn, 'wallThree')
    wallFour = Wall(tableStartX, tableStartY + tableHeight, tableWidth, Wall.thickness, Wall.wallOn, 'wallFour')







#ball variables
    startBallX = screenWidth /2
    startBallY = screenHeight /2
    #size of ball, derived from A = k(pi)r^2, where A is the area of the table, and x = k(pi), resulting in: sqrt(l * w / x), x is chosen arbitrarily
    #A = k(pi)r^2 is found as: 1/k = (pi)r^2/A, relating the ball's area to the table's area
    ballRad = sqrt((tableHeight * tableWidth) / 500)


# paddle variables
    Npaddles = 8
    UpaddleColor = (100, 100, 100)
    paddleWidth = tableWidth / Npaddles
    paddleHeight = tableHeight

    paddleUnoOn = False
    paddleDosOn = False
    paddleTresOn = False
    paddleQuatroOn = False




    if (tableVert):
        paddleWidth = tableWidth
        paddleHeight = tableHeight / Npaddles




## Game Logic

    if keys[pygame.K_a]:
        paddleUnoOn = True
        paddleUnoFresh = paddleUnoFresh + 1
    else:
        paddleUnoFresh = 0
    if keys[pygame.K_s]:
        paddleDosOn = True
        paddleDosFresh = paddleDosFresh + 1
    else:
        paddleDosFresh = 0
    if keys[pygame.K_d]:
        paddleTresOn = True
        paddleTresFresh = paddleTresFresh + 1
    else:
        paddleTresFresh = 0
    if keys[pygame.K_f]:
        paddleQuatroOn = True
        paddleQuatroFresh = paddleQuatroFresh + 1
    else:
        paddleQuatroFresh = 0
    if keys[pygame.K_r]:
        ballX = startBallX
        ballY = tableHeight - ballRad
        ballVX = 0
        ballVY = serveSpeed


    drawPaddleUno = paddleGen(0)
    paddleUno = Collide(drawPaddleUno[0][0], drawPaddleUno[0][1], paddleWidth, paddleHeight, paddleUnoOn, 'paddleUno')
    drawPaddleDos = paddleGen(1)
    paddleDos = Collide(drawPaddleDos[0][0], drawPaddleDos[0][1], paddleWidth, paddleHeight, paddleDosOn, 'paddleDos')
    drawPaddleTres = paddleGen(3)
    paddleTres = Collide(drawPaddleTres[0][0], drawPaddleTres[0][1], paddleWidth, paddleHeight, paddleTresOn, 'paddleTres')
    drawPaddleQuatro = paddleGen(5)
    paddleQuatro = Collide(drawPaddleQuatro[0][0], drawPaddleQuatro[0][1], paddleWidth, paddleHeight, paddleQuatroOn, 'paddleQuatro')



# ball bouncing of colliders

    if 'ballX' in locals() and 'ballY' in locals():
        ballX = ballX + ballVX
        ballY = ballY + ballVY
    else:
        ballX = startBallX
        ballY = startBallY

    canFlipX = True
    canFlipY = True



    for i in Collide._registry:
        if ballX > eval(i).objX-ballRad and ballX <eval(i).objX+ballRad+eval(i).objWid and ballY > eval(i).objY and ballY < eval(i).objY+eval(i).objHei and eval(i).bool and canFlipX:
            if ballX > eval(i).objX + eval(i).objWid/2:
                ballX = eval(i).objX + eval(i).objWid + ballRad
            else:
                ballX = eval(i).objX - ballRad
            
            
            ballVX = - ballVX
            canFlipX = False
            ballVX = ballVX * ballSlowRate
            if ballVX >= 0:
                if i == 'paddleUno' and paddleUnoFresh < 4:
                    ballVX = ballVX + 5-paddleUnoFresh
                if i == 'paddleDos' and paddleDosFresh < 4:
                    ballVX = ballVX + 5 - paddleDosFresh
                if i == 'paddleTres' and paddleTresFresh < 4:
                    ballVX = ballVX + 5 - paddleTresFresh
                if i == 'paddleQuatro' and paddleQuatroFresh < 4:
                    ballVX = ballVX + 5 - paddleQuatroFresh
            if ballVX < 0:
                if i == 'paddleUno' and paddleUnoFresh < 4:
                    ballVX = ballVX - 5-paddleUnoFresh
                if i == 'paddleDos' and paddleDosFresh < 4:
                    ballVX = ballVX - 5 - paddleDosFresh
                if i == 'paddleTres' and paddleTresFresh < 4:
                    ballVX = ballVX - 5 - paddleTresFresh
                if i == 'paddleQuatro' and paddleQuatroFresh < 4:
                    ballVX = ballVX - 5 - paddleQuatroFresh
            print(i, ballVX, paddleUnoFresh)

        if ballY < eval(i).objY + ballRad and ballY > eval(i).objY - ballRad and eval(i).bool and canFlipY:
            if ballY > screenHeight/2:
                ballY = eval(i).objY - ballRad
            else:
                ballY = eval(i).objY + ballRad


            ballVY = -ballVY
            canFlipY = False
            ballVY = ballVY * ballSlowRate
            










## Displays
    pygame.draw.polygon(screen, (0, 250, 0), tableCoords, 0)
    pygame.draw.circle(screen, (250, 250, 250), [ballX, ballY], ballRad, 0)


    if(paddleUnoOn):
        pygame.draw.polygon(screen, UpaddleColor, drawPaddleUno, 0)
    if(paddleDosOn):
        pygame.draw.polygon(screen, UpaddleColor, drawPaddleDos, 0)
    if(paddleTresOn):
        pygame.draw.polygon(screen, UpaddleColor, drawPaddleTres, 0)
    if(paddleQuatroOn):
        pygame.draw.polygon(screen, UpaddleColor, drawPaddleQuatro, 0)

    pygame.time.delay(dt)
    pygame.display.update()
