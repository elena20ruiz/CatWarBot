from catwarbot import game, ctrl_data
from catwarbot import map_game, send_tweet
import json
def get_step():
    with open('catwarbot/data/actual_step.json', 'r') as f:
        data = json.load(f)
    step = data['step']
    return step


def save_step(new_step):
    data = {
        "step": new_step
    }
    with open('catwarbot/data/actual_step.json', 'w') as f:
        json.dump(data, f)

def wins(comarques):
    val = comarques[0][0]
    for el in comarques:
        if comarques[el][0] != val:
            return False
    return True

def run():

    step = get_step()
    if step == 0:
        ctrl_data.init_map()
        map_game.init_map()
    comarques = ctrl_data.load_comarques()
    if wins(comarques):
        print('Game is over')
    else:
        comarques, output = game.run_step(step)
        if wins(comarques):
            guanyador = comarques[0][0]
            t_guanyador = comarques[guanyador][1]
        send_tweet.run(output, 'catwarbot/map/steps/mapa_{}.svg'.format(step+1))
        save_step(step + 1)

if __name__ == "__main__":
    run()