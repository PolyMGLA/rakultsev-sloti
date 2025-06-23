from market.data import data

import random


def rand(up):
    while True:
        x = random.expovariate(0.075)
        if 1 <= x <= up:
            return int(x)


def gen_course():
    data.hamster_course = rand(125)
