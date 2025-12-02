import pyximport
pyximport.install()

from aoc23 import do_it

with open("data2.txt", "r") as fh:
    board = fh.readlines()
    board = [i.rstrip() for i in board]

do_it(board)
