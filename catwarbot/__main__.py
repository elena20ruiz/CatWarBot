from catwarbot import game, ctrl_data


def wins(comarques):
    val = comarques[0][0]
    for el in comarques:
        if comarques[el][0] != val:
            return False
    return True

if __name__ == "__main__":
    ctrl_data.init_map()

    i = 0
    comarques = game.run_step(i)
    if comarques:
        while not wins(comarques):
            comarques = game.run_step(i)
            i += 1
            if not comarques:
                break
    print('Total rondas: ', i)