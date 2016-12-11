#from pandas.hashtable import na_sentinel

import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging
from collections import namedtuple

myID, game_map, targetCoord,d1,d2,d3 = hlt.get_init(0,0,1,1)
hlt.send_init("BrutalBevster")
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


def get_xydistance(self, sq1, sq2):
        "Returns Manhattan distance between two squares."
        dx = min(abs(sq1.x - sq2.x), sq1.x + self.width - sq2.x, sq2.x + self.width - sq1.x)
        dy = min(abs(sq1.y - sq2.y), sq1.y + self.height - sq2.y, sq2.y + self.height - sq1.y)
        return dx,dy

def find_nearest_dense(square,targetCoord):

    direc = NORTH
    lrDist = targetCoord.x- square.x

    lrFlip = False
    if abs(lrDist)>game_map.width/2:
        lrFlip = True

    if lrDist !=0:
        if lrFlip:
            if (lrDist) > 0:
                neighbour = game_map.get_target(square, WEST)
                direc = WEST
            else:
                neighbour = game_map.get_target(square, EAST)
                direc = EAST
        else:
            if (lrDist)>0:
                neighbour = game_map.get_target(square, EAST)
                direc = EAST
            else:
                neighbour = game_map.get_target(square, WEST)
                direc = WEST
        maxStrength = neighbour.strength
    else:
        maxStrength = 10000

    udDist = targetCoord.y - square.y

    udFlip = False
    if abs(udDist)>game_map.height/2:
        udFlip = True

    if udDist != 0:
        if udFlip:
            if (udDist) < 0:
                neighbour = game_map.get_target(square, SOUTH)
                if neighbour.strength<maxStrength:
                    direc = SOUTH
            else:
                neighbour = game_map.get_target(square, NORTH)
                if neighbour.strength<maxStrength:
                    direc = NORTH
        else:
            if (udDist) < 0:
                neighbour = game_map.get_target(square, NORTH)
                if neighbour.strength<maxStrength:
                    direc = NORTH
            else:
                neighbour = game_map.get_target(square, SOUTH)
                if neighbour.strength<maxStrength:
                    direc = SOUTH

    #logging.debug(str(direc) + " " + str(square) + " " + str(targetCoord))

    neighbour = game_map.get_target(square, direc)
    if neighbour.strength < square.strength:
        return Move(square, direc)
    else:# square.strength < square.production * 5: #and square.strength<100
        return Move(square, STILL)

target = True
while True:
    game_map.get_frame()
    if target==False:
        #logging.debug(ma)
        #first = False
        moves = [find_nearest_dense(square,targetCoord) for square in game_map if square.owner == myID]
        for square in game_map:
            if square.x == targetCoord.x and square.y == targetCoord.y and square.owner == myID:
                target = True
                #logging.debug(target)
        hlt.send_frame(moves)

    else:
        moves = [get_move(square) for square in game_map if square.owner == myID]
        hlt.send_frame(moves)

