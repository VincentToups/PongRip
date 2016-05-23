import pygame, sys
from pygame.locals import *

FPS = 200

WINDOWWIDTH = 400
WINDOWHEIGHT = 300

LINETHICKNESS = 12
PADDLESIZE = 50
PADDLEOFFSET = 20

BLACK = (0  , 0  , 0  )
WHITE = (255, 255, 255)

def drawArena():
    DISPLAYSURF.fill(BLACK)
    #outline
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), (LINETHICKNESS*2))
    #center line
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2),0),((WINDOWWIDTH/2), WINDOWHEIGHT), int((LINETHICKNESS/4)))

def drawPaddle(paddle):
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)


def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY *= -1
    if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirX *= -1
    return ballDirX, ballDirY

def AI(ball, ballDirX, paddle2):
    if ballDirX == -1:
        if paddle2.centery < (WINDOWHEIGHT/2):
            paddle2.y += 1
        elif paddle2.centery > (WINDOWHEIGHT/2):
            paddle2.y -= 1
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        elif paddle2.centery > ball.centery:
            paddle2.y -= 1
    return paddle2
        
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else:
        return 1

def checkPointScored(ball, score):
    if ball.left == LINETHICKNESS or ball.right == LINETHICKNESS:
        score +=1
    return score
    
        

def main():
    pygame.init()
    global DISPLAYSURF

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('PongRip')

    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2

    player1score = 0
    player2score = 0

    # right +
    # down +
    # left -
    # up -

    ballDirX = -1
    ballDirY = -1

    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    pygame.mouse.set_visible(0)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)
        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        paddle2 = AI(ball, ballDirX, paddle2)
        if ballDirX == -1:
            player1score = checkPointScored(ball, player1score)
        elif ballDirX == 1:
            player2score = checkPointScored(ball, player2score)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)

        pygame.display.update()
        FPSCLOCK.tick(FPS)  

if __name__ == '__main__':
    main()



        
