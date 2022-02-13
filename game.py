import random


def attack_success(attack_success_chance):
    return random.uniform(0, 1) <= attack_success_chance
