from hlt import *
from networking import *
import csv

myID, gameMap = getInit()
sendInit("BevsterBot")
#csvFile = csv.writer(open('\\\\ldnvnascti0037\\FXT_Grail$\\bevan\\halite.csv', "wb"))


def inCluster(location):
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        if neighbour_site.owner != myID:
            return False
    return True


def findHighestRatioNeighbour(location):
    maxRatio = 0
    maxRatioCardinal = -1
    foundSite = False

    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        if neighbour_site.owner != myID:
            if neighbour_site.strength == 0:
                return d
            else:
                ratio = neighbour_site.production / float(neighbour_site.strength)
                if ratio > maxRatio:
                    maxRatio = ratio
                    maxRatioCardinal = d
                    foundSite = True

    if foundSite:
        return maxRatioCardinal
    else:
        return -1


def findHighestAvailableRatioNeighbour(location):
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
        return maxRatioCardinal
    else:
        return -1


def findBestDirection(location):
    max_iter = gameMap.height

    min_number = max_iter
    min_cardinal = -1

    for d in CARDINALS:
        counter = 1
        in_cluster = True
        neighbour_site = gameMap.getSite(location, d)
        neighbour_loc = gameMap.getLocation(location, d)
        while counter<min_number:
            if neighbour_site.owner != myID:
                if counter < min_number:
                    min_number = counter
                    min_cardinal = d
                break
            else:
                neighbour_site = gameMap.getSite(neighbour_loc, d)
                neighbour_loc = gameMap.getLocation(neighbour_loc, d)
                counter += 1

    if min_cardinal > 0:
        return min_cardinal
    else:
        return NORTH

    # for d in CARDINALS:
    #     ourLoc = gameMap.getLocation(location, 0)
    #     ourLocX = ourLoc.x
    #     ourLocY = ourLoc.y
    #     leftRightMult = 1
    #     if d==1 or d==3:
    #         if d==3:
    #             leftRightMult = -1
    #
    #         height = gameMap.height
    #         keepSearching=True
    #         while keepSearching:
    #             halfWayDist = leftRightMult*int((height - ourLocY)/2)
    #             halfWay = ourLocY + halfWayDist
    #             location = Location(ourLocX, halfWay)
    #             if halfWayDist>2:
    #                 if gameMap.getLocation(location, 0).owner==myID:
    #                     ourLocY = halfWay
    #                 else:
    #                     height = halfWay
    #             else:
    #                 dist = (location.y - ourLoc.y)
    #                 break




    if min_cardinal > 0:
        return min_cardinal
    else:
        return NORTH


def move(location,startLoc):
    site = gameMap.getSite(location)
    dist = gameMap.getDistance(location,startLoc)


    # if dist>5 and site.strength<200 and inCluster(location)==False:
    #      return Move(location, STILL)
    #csvFile.writerow([startLoc.x,startLoc.y,location.x, location.y, dist])
    # TODO: implement, don't waste turn gathering strenth if it would exceed limit
    must_move = False
    if site.strength > 240:
        must_move = True

    # Only move when strength exceeds multiple of site production
    if site.strength < site.production * 5:
        return Move(location, STILL)

    if inCluster(location):
        # If in middle of cluster move to nearest edge site
        return Move(location, findBestDirection(location))
    else:
        # If at edge of cluster, move to highest production/strength ratio site
        availableCardinal = findHighestAvailableRatioNeighbour(location)
        if availableCardinal > 0:

            neighbour = gameMap.getSite(location, availableCardinal)
            myLocation = gameMap.getSite(location)
            if neighbour.strength>myLocation.strength and must_move==False:
                return Move(location,STILL)

            return Move(location, availableCardinal)
        else:
            bestCardinal = findHighestRatioNeighbour(location)

            neighbour = gameMap.getSite(location, bestCardinal)
            myLocation = gameMap.getSite(location)
            if neighbour.strength>myLocation.strength and must_move==False:
                return Move(location,STILL)

            if bestCardinal > 0:
                return Move(location, bestCardinal)
            else:
                if must_move:
                    return Move(location, NORTH)
                else:
                    return Move(location, STILL)



    # return Move(location, NORTH if random.random() > 0.5 else WEST)



startLoc = Location(0, 0)
firstLoop = True
while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                if firstLoop:
                    startLoc = Location(x,y)
                moves.append(move(location,startLoc))
                firstLoop = False
    sendFrame(moves)

