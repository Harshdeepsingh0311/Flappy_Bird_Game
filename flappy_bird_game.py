import random as rd  # For generating random number
import pygame as pg  # Main library for the game
from pygame.locals import *  # Basic pygame imports
import sys  # To exit the program

# Global Variables
fps = 40
screenWidth = 289
screenHeight = 511
baseY = screenHeight * 0.8
gameSprites = {}
gameSounds = {}
player = 'gallery/sprites/bird.png'
background = 'gallery/sprites/background.png'
pipe = 'gallery/sprites/pipe.png'
icon = pg.image.load('icon.ico')

# Initializing the screen
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_icon(icon)


def welcomeScreen():
    """
    Shows welcome screen
    """
    playerX = int(screenWidth / 5)
    playerY = int((screenHeight - gameSprites['player'].get_height()) / 2)
    messageX = int((screenWidth - gameSprites['message'].get_width()) / 2)
    messageY = int(screenHeight * 0.13)
    baseX = 0

    while True:
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                screen.blit(gameSprites['background'], (0, 0))
                screen.blit(gameSprites['player'], (playerX, playerY))
                screen.blit(gameSprites['message'], (messageX, messageY))
                screen.blit(gameSprites['base'], (baseX, baseY))

                pg.display.update()
                fpsClock.tick(fps)


def isCollide(playerX, playerY, upperPipe, lowerPipe):
    if playerY> baseY-25 or playerY<0:
        gameSounds['hit'].play()
        return True

    for pipe in upperPipe:
        pipeHeight = gameSprites['pipe'][0].get_height()
        if (playerY < pipeHeight + pipe['y'] and (abs(playerX - pipe['x']) < gameSprites['pipe'][0].get_width())):
            gameSounds['hit'].play()
            return True

    for pipe in lowerPipe:
        if (playerY + gameSprites['player'].get_height() > pipe['y']) and (abs(playerX - pipe['x']) < gameSprites['pipe'][0].get_width()):
            gameSounds['hit'].play()
            return True

    return False


def mainGame():
    score = 0
    playerX = int(screenWidth/5)
    playerY = int(screenHeight/2)
    baseX = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipe = [
        {'x':screenWidth+200, 'y':newPipe1[0]['y']},
        {'x':screenWidth+200+ (screenWidth/2) , 'y':newPipe2[0]['y']}
    ]

    lowerPipe = [
        {'x': screenWidth + 200, 'y': newPipe1[1]['y']},
        {'x': screenWidth + 200 + (screenWidth / 2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4

    playervelY = -9
    playerMaxvelY = 10
    playerMinvelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False


    while True:
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE ):
                pg.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE  or event.key == K_UP):
                if playerY > 0:
                    playervelY = playerFlapAccv
                    playerFlapped = True
                    gameSounds['wing'].play()

        crashTest = isCollide(playerX, playerY, upperPipe, lowerPipe)

        if crashTest:
            return

        playerMidPos = playerX + gameSprites['player'].get_width()/2
        for pipe in upperPipe:
            pipeMidPos = pipe['x'] + gameSprites['pipe'][0].get_width()/2

            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score += 1
                

                gameSounds['point'].play()

        if playervelY < playerMaxvelY and not playerFlapped:
            playervelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = gameSprites['player'].get_height()
        playerY = playerY +  min(playervelY, baseY- playerY - playerHeight)

        for upperPip, lowerPip in zip(upperPipe, lowerPipe):
            upperPip['x'] += pipeVelX
            lowerPip['x'] += pipeVelX

        if 0<upperPipe[0]['x']<5:
            newPipe = getRandomPipe()
            upperPipe.append(newPipe[0])
            lowerPipe.append(newPipe[1])

        if upperPipe[0]['x'] < - gameSprites['pipe'][0].get_width():
            upperPipe.pop(0)
            lowerPipe.pop(0)



        screen.blit(gameSprites['background'], (0, 0))

        for upperPip, lowerPip in zip(upperPipe, lowerPipe):
            screen.blit(gameSprites['pipe'][0], (upperPip['x'], upperPip['y']))
            screen.blit(gameSprites['pipe'][1], (lowerPip['x'], lowerPip['y']))

        screen.blit(gameSprites['base'], (baseX, baseY))
        screen.blit(gameSprites['player'], (playerX, playerY))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += gameSprites['numbers'][digit].get_width()

        xOffset = (screenWidth- width)/2

        for digit in myDigits:
            screen.blit(gameSprites['numbers'][digit], (xOffset, screenHeight*0.12))
            xOffset += gameSprites['numbers'][digit].get_width()

        pg.display.update()
        fpsClock.tick(fps)




def getRandomPipe():
    """
    Generates positions of two pipes for blitting on the screen
    :return:
    """
    pipeHeight = gameSprites['pipe'][0].get_height()
    offset = screenHeight/3
    # pipeWidth = gameSprites['pipe'][1].get_width()
    y2 = offset + rd.randrange(0, int(screenHeight - gameSprites['base'].get_height() - 1.2*offset))
    y1 = pipeHeight - y2 + offset
    pipeX = screenWidth+10
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe


if __name__ == '__main__':
    # Main function
    pg.init()  # Initializing all packages
    fpsClock = pg.time.Clock()
    pg.display.set_caption('Flappy Bird by Harshdeep Singh')

    # Game sprites
    gameSprites['numbers'] = (
        pg.image.load('gallery/sprites/0.png').convert_alpha(),
        pg.image.load('gallery/sprites/1.png').convert_alpha(),
        pg.image.load('gallery/sprites/2.png').convert_alpha(),
        pg.image.load('gallery/sprites/3.png').convert_alpha(),
        pg.image.load('gallery/sprites/4.png').convert_alpha(),
        pg.image.load('gallery/sprites/5.png').convert_alpha(),
        pg.image.load('gallery/sprites/6.png').convert_alpha(),
        pg.image.load('gallery/sprites/7.png').convert_alpha(),
        pg.image.load('gallery/sprites/8.png').convert_alpha(),
        pg.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    gameSprites['message'] = (pg.image.load('gallery/sprites/message.png').convert_alpha())
    gameSprites['base'] = (pg.image.load('gallery/sprites/base.png').convert_alpha())
    gameSprites['pipe'] = (pg.transform.rotate(pg.image.load(pipe).convert_alpha(), 180),
                           pg.image.load(pipe).convert_alpha())
    gameSprites['background'] = pg.image.load(background).convert()
    gameSprites['player'] = pg.image.load(player).convert_alpha()

    # Game sounds
    gameSounds['die'] = pg.mixer.Sound('gallery/audio/die.wav')
    gameSounds['hit'] = pg.mixer.Sound('gallery/audio/hit.wav')
    gameSounds['point'] = pg.mixer.Sound('gallery/audio/point.wav')
    gameSounds['swoosh'] = pg.mixer.Sound('gallery/audio/swoosh.wav')
    gameSounds['wing'] = pg.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreen()
        mainGame()


