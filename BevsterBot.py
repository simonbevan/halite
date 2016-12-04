from hlt import *
from networking import *
import logging
import math

myID, gameMap = getInit()

logging.basicConfig(filename=str(myID) + '.log', level=logging.DEBUG)

sendInit("BevsterBot")

def inCluster(location):
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        if neighbour_site.owner != myID:
            return False
    return True

def find_nearest_edge(location,ownerMatrix):
    direction = 1
    max_distance = min(gameMap.width, gameMap.height)

    for d in CARDINALS:
        distance = 0
        current = location
        site = gameMap.getSite(current, d)

        while site.owner == myID and distance < max_distance:
            distance += 1
            current = gameMap.getLocation(current, d)
            site = gameMap.getSite(current)

        if distance < max_distance:
            direction = d
            max_distance = distance


    # logging.debug("Moving: " + str(direction))
    return direction



def find_nearest_enemy(location,ownerMatrix):
    direction = NORTH
    max_distance = min(gameMap.width, gameMap.height)
    site = gameMap.getSite(location)

    bestAngle = 0

    for y in range(gameMap.height):
        for x in range(gameMap.width):
            testLocation = Location(x, y)
            #testLocation = gameMap.getSite(location)
            dist = gameMap.getDistance(location,testLocation)
            if dist < max_distance and ownerMatrix[y][x]!=myID and ownerMatrix[y][x]!=0:
                max_distance = dist

                bestAngle = gameMap.getAngle(location,testLocation)*(180/math.pi)
                if bestAngle < 0.0:
                    bestAngle += 360.0

    if bestAngle < 90:
        direction = [1,2]
    elif bestAngle < 180 and bestAngle >= 90:
        direction = [2,3]
    elif bestAngle >= 180 and bestAngle < 270:
        direction = [3,4]
    else:
        direction = [4,1]

    bestDir=0
    maxRatio = 0
    for d in direction:

        neighbour_site = gameMap.getSite(location, d)

        if inCluster(location)==False:
            if neighbour_site.owner != myID and neighbour_site.strength < site.strength:
                if neighbour_site.strength == 0:
                    return d
                else:
                    ratio = float(neighbour_site.production) / float(neighbour_site.strength)
                    if ratio > maxRatio:
                        maxRatio = ratio
                        bestDir = d
                        foundSite = True
        else:
            if neighbour_site.strength == 0:
                return d
            else:
                ratio = float(neighbour_site.production) / float(neighbour_site.strength)
                if ratio > maxRatio:
                    maxRatio = ratio
                    bestDir = d
                    foundSite = True

    return bestDir




def findHighestAvailableRatioNeighbour(location,ownerMatrix):
    site = gameMap.getSite(location)

    maxRatio = 0.0
    maxRatioCardinal = -1.0
    foundSite = False

    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)

        if neighbour_site.owner != myID and neighbour_site.strength < site.strength:
            if neighbour_site.strength == 0:
                return d
            else:
                ratio = float(neighbour_site.production) / float(neighbour_site.strength)
                if ratio > maxRatio:
                    maxRatio = ratio
                    maxRatioCardinal = d
                    foundSite = True




    if foundSite:
        neighbour_site = gameMap.getSite(location, maxRatioCardinal)
        # if float(neighbour_site.strength) + site.strength > 255:
        #
        #     if maxRatioCardinal==1:
        #         maxRatioCardinal = 3
        #     else:
        #         maxRatioCardinal = 4

        return maxRatioCardinal
    else:
        d = find_nearest_edge(location,ownerMatrix)
        return d

def move(location,ownerMatrix):
    site = gameMap.getSite(location)

    strength = site.strength
    production = site.production

    must_move = False
    if strength > 100:
        must_move = True


    if inCluster(location):

        must_move = False
        if strength > 50:
            must_move = True

        if strength < production * 4 and must_move == False:
            return Move(location, STILL)
        # If in middle of cluster move to nearest edge site
        return Move(location, find_nearest_edge(location,ownerMatrix))
        #return Move(location, findBestDirection(location))
    else:

        if strength < production * 5 and must_move == False:
            return Move(location, STILL)

        availableCardinal = findHighestAvailableRatioNeighbour(location,ownerMatrix)

        if availableCardinal > 0:

            neighbour = gameMap.getSite(location, availableCardinal)
            myLocation = gameMap.getSite(location)
            if neighbour.strength > myLocation.strength and must_move == False:
                return Move(location, STILL)

            return Move(location, availableCardinal)


    #logging.debug("Staying still..")
    return Move(location, STILL)


while True:
    moves = []
    gameMap = getFrame()

    ownerMatrix = []
    # for y in range(gameMap.height):
    #     ownerMatrix.append([])
    #     for x in range(gameMap.width):
    #         location = Location(x, y)
    #         ownerMatrix[-1].append(gameMap.getSite(location).owner)

    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            #logging.debug(gameMap.getSite(location).owner)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location,ownerMatrix))
    sendFrame(moves)