from hlt import *
from networking import *
import logging

myID, gameMap = getInit()

#logging.basicConfig(filename=str(myID) + '.log', level=logging.DEBUG)

sendInit("ConnorBot")


def find_nearest_enemy_direction(location):
    direction = NORTH
    max_distance = min(gameMap.width, gameMap.height) / 2

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

    #logging.debug("Moving: " + str(direction))
    return direction


def move(location):
    site = gameMap.getSite(location)

    strength = site.strength
    production = site.production

    # logging.debug("Current strength: " + str(strength))
    # logging.debug("Current production: " + str(production))

    border = False
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        if not neighbour_site.owner == myID:
            #logging.debug("Enemy site: " + str(neighbour_site))
            border = True
            if neighbour_site.strength < strength:
                #logging.debug("Enemy strength is: " + str(neighbour_site.strength) + " my strength is " + str(strength))
                return Move(location, d)

    if strength < production * 5:
        return Move(location, STILL)


    if not border:
        return Move(location, find_nearest_enemy_direction(location))

    #logging.debug("Staying still..")
    return Move(location, STILL)


while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))
    sendFrame(moves)