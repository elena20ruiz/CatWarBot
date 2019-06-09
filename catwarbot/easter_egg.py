from catwarbot import map_game
import json, random


def read_file():
    with open('catwarbot/data/easter_eggs.json', 'r', encoding="utf-8") as f:
        data = json.loads(f)
    return data

def most_repetated_value(comarques):
    repetitions = {}
    for c in comarques:
        t_id = comarques[c][0]
        if not t_id in repetitions:
            repetitions[t_id] = 1
        else:
            repetitions[t_id] += 1

# Stole to the most conquered territory
def make_independence(comarques, veins):

    # 1. Get the one that has more conquered territories    

    # 2. Get the ser of conquered territory

    # 3. Get a random territory from them

    # 4. Make independence, assign to them 

    return

def run(comarques,veins):
    # Load easter eggs
    features = read_file()

    n = len(features.keys())
    nrandom = random.randint(0, n - 1)

    if features[nrandom]:
        make_independence()

    return comarques, veins