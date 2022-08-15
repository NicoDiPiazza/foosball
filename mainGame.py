from math import sqrt
import pygame

pygame.init()

## function naming

# User paddle Coordinate generation

def paddleGen(spot):   
    paddleCoords = [((paddleWidth * spot) + tableStartX, tableStartY), ((paddleWidth * ( spot + 1)) + tableStartX, tableStartY)]
    bottomCoords =((paddleWidth * (spot + 1)) + tableStartX, tableStartY + tableHeight)
    finalCoords = ((paddleWidth * spot) + tableStartX, tableStartY + tableHeight)
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
        self._registry.append(name)
        

class Wall(Collide):
    thickness = 1
    wallOn = True




#screen parameters

screenWidth = 1000
screenHeight = 600
screen_size = [ screenWidth, screenHeight]

screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

dt = 10


pygame.event.get()
keys = pygame.key.get_pressed()



ballVX = 5
ballVY = 1





while (keys[pygame.K_q] != True):
    pygame.event.get()
    keys = pygame.key.get_pressed()

    screenWidth = screen.get_width()
    screenHeight = screen.get_height()

    screenRatio = screenHeight / screenWidth


## Calculations


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

    wallList = [wallOne, wallTwo, wallThree, wallFour]






#ball variables
    startBallX = screenWidth /2
    startBallY = screenHeight /2
    #size of ball, derived from A = k(pi)r^2, where A is the area of the table, and x = k(pi), resulting in: sqrt(l * w / x), x is chosen arbitrarily
    #A = k(pi)r^2 is found as: 1/k = (pi)r^2/A, relating the ball's area to the table's area
    ballRad = sqrt((tableHeight * tableWidth) / 500)


# paddle variables
    Npaddles = 8
    UpaddleColor = (100, 100, 100)
    paddleWidth = tableWidth / 8
    paddleHeight = tableHeight

    paddleUno = False
    paddleDos = False
    paddleTres = False
    paddleQuatro = False

    if (tableVert):
        paddleWidth = tableWidth
        paddleHeight = tableHeight / 8




## Game Logic

    if keys[pygame.K_a]:
        paddleUno = True
    if keys[pygame.K_s]:
        paddleDos = True
    if keys[pygame.K_d]:
        paddleTres = True
    if keys[pygame.K_f]:
        paddleQuatro = True
    if keys[pygame.K_r]:
        ballX = startBallX
        ballY = startBallY


# ball bouncing of colliders

    if 'ballX' in locals() and 'ballY' in locals():
        ballX = ballX + ballVX
        ballY = ballY + ballVY
    else:
        ballX = startBallX
        ballY = startBallY


    for i in Collide._registry:
        if ballX <= eval(i).objX + ballRad and ballX >= eval(i).objX - ballRad:
            ballVX = -ballVX
        if ballY <= eval(i).objY + ballRad and ballY >= eval(i).objY - ballRad:
            ballVY = -ballVY








## Displays

    pygame.draw.polygon(screen, (0, 250, 0), tableCoords, 0)
    pygame.draw.circle(screen, (250, 250, 250), [ballX, ballY], ballRad, 0)


    if(paddleUno):
        drawPaddle = paddleGen(0)
        pygame.draw.polygon(screen, UpaddleColor, drawPaddle, 0)
    if(paddleDos):
        drawPaddle = paddleGen(1)
        pygame.draw.polygon(screen, UpaddleColor, drawPaddle, 0)
    if(paddleTres):
        drawPaddle = paddleGen(3)
        pygame.draw.polygon(screen, UpaddleColor, drawPaddle, 0)
    if(paddleQuatro):
        drawPaddle = paddleGen(5)
        pygame.draw.polygon(screen, UpaddleColor, drawPaddle, 0)



    pygame.display.update()
