from catwarbot import game, ctrl_data
from catwarbot import map_game


def wins(comarques):
    val = comarques[0][0]
    for el in comarques:
        if comarques[el][0] != val:
            return False
    return True

if __name__ == "__main__":
    ctrl_data.init_map()
    map_game.init_map()
    
    comarques = ctrl_data.load_comarques()

    i = 0
    while not wins(comarques):
        comarques, output = game.run_step(i)
        i += 1
        if not comarques:
            break
    print('Total rondas: ', i)