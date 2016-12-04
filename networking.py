from hlt import *
import socket
import traceback
import struct
from ctypes import *
import sys
import time

_productions = []
_width = -1
_height = -1

def serializeMoveSet(moves):
    returnString = ""
    for move in moves:
        returnString += str(move.loc.x) + " " + str(move.loc.y) + " " + str(move.direction) + " "
    return returnString

def deserializeMapSize(inputString):
    splitString = inputString.split(" ")

    global _width, _height
    _width = int(splitString.pop(0))
    _height = int(splitString.pop(0))

def deserializeProductions(inputString):
    splitString = inputString.split(" ")

    for a in range(0, _height):
        row = []
        for b in range(0, _width):
            row.append(int(splitString.pop(0)))
        _productions.append(row)

def deserializeMap(inputString):
    splitString = inputString.split(" ")

    m = GameMap(_width, _height)

    y = 0
    x = 0
    counter = 0
    owner = 0
    while y != m.height:
        counter = int(splitString.pop(0))
        owner = int(splitString.pop(0))
        for a in range(0, counter):
            m.contents[y][x].owner = owner
            x += 1
            if x == m.width:
                x = 0
                y += 1

    for a in range(0, _height):
        for b in range(0, _width):
            m.contents[a][b].strength = int(splitString.pop(0))
            m.contents[a][b].production = _productions[a][b]

    return m

def sendString(toBeSent):
    toBeSent += '\n'

    sys.stdout.write(toBeSent)
    sys.stdout.flush()

def getString():
    return sys.stdin.readline().rstrip('\n')

def getInit():
    playerTag = int(getString())
    deserializeMapSize(getString())
    deserializeProductions(getString())
    m = deserializeMap(getString())

    startTime = time.time()
    ownerMatrix = []
    ratioMatrix = []
    #gameMap = getFrame()

    # for y in range(gameMap.height):
    #     ownerMatrix.append([])
    #     ratioMatrix.append([])
    #     for x in range(gameMap.width):
    #         location = Location(x, y)
    #         ownerMatrix[-1].append(gameMap.getSite(location).owner)
    #         if gameMap.getSite(location).strength > 0:
    #             ratioMatrix[-1].append(gameMap.getSite(location).production / gameMap.getSite(location).strength)

    timeNow = time.time()
    timeDiff = (timeNow - startTime)
    while timeDiff < 2:
        timeNow = time.time()
        timeDiff = (timeNow - startTime)


    return (playerTag, m)

def sendInit(name):
    sendString(name)

def getFrame():
    return deserializeMap(getString())

def sendFrame(moves):
    sendString(serializeMoveSet(moves))


