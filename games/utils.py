import random


def randint(a: int, b: int):
    return random.randint(a, b)


def choice(x: list):
    return x[randint(0, len(x) - 1)]

def shuffle(x: list):
    random.shuffle(x)
