#from pandas.hashtable import na_sentinel

import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging
from collections import namedtuple

myID, game_map, targetCoord = hlt.get_init()
hlt.send_init("Bevster")
#logging.basicConfig(filename=str(myID) + '.log', level=logging.DEBUG)


def find_nearest_enemy_direction(square):
    direction = NORTH
    max_distance = min(game_map.width, game_map.height) / 2
    for d in (NORTH, EAST, SOUTH, WEST):
        distance = 0
        current = square
        while (current.owner == myID or current.owner==0) and distance < max_distance:
            distance += 1
            current = game_map.get_target(current, d)
        if distance < max_distance:
            direction = d
            max_distance = distance
    return direction


def heuristic(square):
    if square.owner == 0 and square.strength > 0:
        return square.production / square.strength
    else:
        # return total potential damage caused by overkill when attacking this square
        return sum(neighbor.strength for neighbor in game_map.neighbors(square) if neighbor.owner not in (0, myID))


def get_move(square):
    target, direction = max(((neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))
                             if neighbor.owner != myID),
                            default=(None, None),
                            key=lambda t: heuristic(t[0]))


    if target is not None and target.strength < square.strength:
        return Move(square, direction)
    elif square.strength < square.production * 5: #and square.strength<100
        return Move(square, STILL)

    border = any(neighbor.owner != myID for neighbor in game_map.neighbors(square))
    if not border:
        #if square.strength < square.production * 2:
        #    return Move(square, STILL)
        #else:
        return Move(square, find_nearest_enemy_direction(square))
    else:
        # wait until we are strong enough to attack
        return Move(square, STILL)


def find_nearest_dense(square,targetCoord):

    dir = NORTH
    if (targetCoord.x- square.x)>0:
        neighbour = game_map.get_target(square, EAST)
        dir = EAST
    else:
        neighbour = game_map.get_target(square, WEST)
        dir = WEST

    maxStrength = neighbour.strength

    if (targetCoord.y - square.y) < 0:
        neighbour = game_map.get_target(square, NORTH)
        if neighbour.strength<maxStrength:
            dir = NORTH
    else:
        neighbour = game_map.get_target(square, SOUTH)
        if neighbour.strength<maxStrength:
            dir = SOUTH
    return Move(square, dir)


target = False
while True:
    game_map.get_frame()
    if target==False:
        #logging.debug(ma)
        #first = False
        moves = [find_nearest_dense(square,targetCoord) for square in game_map if square.owner == myID]
        for square in game_map:
            if square.x == targetCoord.x and square.y == targetCoord.y and square.owner == myID:
                target = True

    else:
        moves = [get_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)




# from hlt_old import *
# from networking_old import *
# import logging
#
# myID, gameMap = getInit()
#
# #logging.basicConfig(filename=str(myID) + '.log', level=logging.DEBUG)
#
# sendInit("ConnorBot")
#
#
# def find_nearest_enemy_direction(location):
#     direction = NORTH
#     max_distance = min(gameMap.width, gameMap.height) / 2
#
#     for d in CARDINALS:
#         distance = 0
#         current = location
#         site = gameMap.getSite(current, d)
#
#         while site.owner == myID and distance < max_distance:
#             distance += 1
#             current = gameMap.getLocation(current, d)
#             site = gameMap.getSite(current)
#
#         if distance < max_distance:
#             direction = d
#             max_distance = distance
#
#     #logging.debug("Moving: " + str(direction))
#     return direction
#
#
# def move(location):
#     site = gameMap.getSite(location)
#
#     strength = site.strength
#     production = site.production
#
#     # logging.debug("Current strength: " + str(strength))
#     # logging.debug("Current production: " + str(production))
#
#     border = False
#     for d in CARDINALS:
#         neighbour_site = gameMap.getSite(location, d)
#         if not neighbour_site.owner == myID:
#             #logging.debug("Enemy site: " + str(neighbour_site))
#             border = True
#             if neighbour_site.strength < strength:
#                 #logging.debug("Enemy strength is: " + str(neighbour_site.strength) + " my strength is " + str(strength))
#                 return Move(location, d)
#
#     if strength < production * 5:
#         return Move(location, STILL)
#
#
#     if not border:
#         return Move(location, find_nearest_enemy_direction(location))
#
#     #logging.debug("Staying still..")
#     return Move(location, STILL)
#
#
# while True:
#     moves = []
#     gameMap = getFrame()
#     for y in range(gameMap.height):
#         for x in range(gameMap.width):
#             location = Location(x, y)
#             if gameMap.getSite(location).owner == myID:
#                 moves.append(move(location))
#     sendFrame(moves)