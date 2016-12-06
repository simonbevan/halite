from pandas.hashtable import na_sentinel

import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging
from collections import namedtuple

myID, game_map, ma = hlt.get_init()
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

def get_areaDense(square):
    None
    #target, direction = (neighbor, direction) for direction, neighbor in enumerate(game_map.neighbors(square))

def get_squareDense(square,gm):
    squareDense = sum(neighbor.production / neighbor.strength if neighbor.production != 0  else neighbor.strength for neighbor in gm.neighbors(square)) \
    + square.production / square.strength if square.production != 0  else square.strength
    SquareDense = namedtuple('SquareDense', 'x y sd')
    return SquareDense(square.x,square.y,squareDense)

target = False
while True:
    game_map.get_frame()
    if target==False:
        #logging.debug(ma)
        #first = False
        moves = [get_move(square) for square in game_map if square.owner == myID]

    moves = [get_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)

