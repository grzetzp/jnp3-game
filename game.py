import random


def defend():
    return random.randint(0, 1)


def attack():
    return random.randint(0, 1)


def attack_success(val):
    return val % 2 == 0


def defense_success(val):
    return val % 2 == 0
