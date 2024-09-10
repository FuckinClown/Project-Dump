import random

def UserAgent():
    file = open("data/user_agents.txt", "r").read().splitlines()
    agnt = random.choice(file)
    return agnt