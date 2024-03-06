import random

from dlgo.game_rules_implementation.Point import Point
from dlgo.game_rules_implementation.Player import Player


def to_python(player_state):
    if player_state is None:
        return 'None'
    if player_state == Player.black:
        return Player.black
    return Player.white


MAX63 = 0x7fffffffffffffff
global HASH_CODE, EMPTY_BOARD
HASH_CODE = {}
for row in range(1, 20):
    for col in range(1, 20):
        for state in (Player.black, Player.white):
            HASH_CODE[Point(row, col), state] = random.randint(0, MAX63)
    EMPTY_BOARD = 0
