
import random, json, queue
from catwarbot import ctrl_data
from catwarbot import map_game, easter_egg
from catwarbot.variables import setmanes, anys


def change_start_array(l):
    size = len(l)
    pos_v = random.randint(0, size - 1)

    res = []
    i = 0
    while i < size:
        res.append(l[i % size])
        i += 1
    return res


def get_diff_neightboor(comarques, veins, t, c):

    # 1. Different start

    # 2. Get a neightboor with different conqueror
    #    Return when founded
    #    1. First check the first level
    #    2. If not check the others levels
    q = queue.Queue()
    visited = [False] * len(comarques)
    visited[t] = True

    first_veins = change_start_array(veins[t])
    for el in first_veins:
        q.put(el)


    while not q.empty():

        # Get first
        id_vei = q.get()
        # Get veins of vei
        if not visited[id_vei]:
            if comarques[id_vei][0] != c:
                return id_vei
            else:
                visited[id_vei] = True
                for el in veins[id_vei]:
                    if not visited[el]:
                        q.put(el)
    return -1


def save_comarques(comarques):
    with open('catwarbot/data/comarques.json', 'w') as outfile:
        json.dump(comarques, outfile)


def get_n_last(comarques):
    restants = []
    for c in comarques:
        if not comarques[c][0] in restants:
            restants.append(comarques[c][0])
    return len(restants)


def there_are_anyone(comarques, lost):
    for c in comarques:
        if comarques[c][0] == lost:
            return True
    return False


def fight(step, t, c, ne, c_ne):
    if step < 500:
        # Fight!
        fight = random.randint(0,1)

        if fight < 0.5:
            # C wins ne territory
            winner = c
            lost = c_ne
            terr = ne
        else:
            # C_NE wins t territory
            winner = c_ne
            lost = c
            terr = t
    else:
        # C wins ne territory
        winner = c
        lost = c_ne
        terr = ne
    return winner, lost, terr


def generate_output(comarques, winner, lost, terr, step):
   
    winner_t = comarques[winner][1]
    lost_t = comarques[lost][1]
    terr_t = comarques[terr][1]

    init_year = 2020
    mod_4 = step % 4 
    mod_12 = int((step % 48)/4)
    year_m = int(step/48)
    year = init_year + year_m
    output = '{} setmana del mes {}, any {}. '.format(setmanes[mod_4], anys[mod_12], year)

    # 1. X ha conquistat Y
    output += '{} {} ha conquistat la comarca {} {}'.format(comarques[winner][4], winner_t, comarques[terr][5], terr_t)

    # 2 Y anteriorment ocupat per Z (opt)
    if terr != lost:
        output += ', anteriorment ocupada {} {}.'.format(comarques[lost][3], lost_t)

    # 3 Z ha sigut completament derrotat: si no hi ha mes
    if not there_are_anyone(comarques, lost):
        output += ' {} {} passa a ser una comarca derrotada.\n'.format(comarques[lost][4], comarques[lost][1])
        # 3.1 Queden N territoris restants
        num  = get_n_last(comarques)
        if num == 1:
            output += '\n Finalment, {} {} es proclama comarca guanyadora!'.format(comarques[winner][4], winner_t)
        else:
            output += ' {} comarques restants.'.format(num)

    # 4 Hashtags
    output += '\n \n'
    output += '#{} #{}'.format(winner_t.replace(" ", ""), terr_t.replace(" ", ""))
    if terr != lost:
        output += ' #{}'.format(lost_t.replace(" ", ""))
    output += ' #CatalunyaWarBot'
    return output


def run_step(step):
    """
    Run Step: Start the game step
    ---------------------------------------
    Load the last step comarques and veins.
    1. Get a random territory t
    2. Get t conqueror as a c
    3. Get a neightboor with different conqueror as n
    4. Get neightboor's conqueror as a c_ne
    5. Fight
    6. Assign the territory conquered, the winner and the lost.
    7. Implement text's tweet
    8. Update the image to show
    """
    comarques = ctrl_data.load_comarques()
    veins = ctrl_data.load_veins()

    if step != 0 and step % 1000 == 0:
        comarques, output = easter_egg.run(comarques, veins)
    else:
        # 1. Get random id -> t
        n = len(comarques)
        t = random.randint(0, n - 1)

        # 2. Get conqueror -> c
        c = comarques[t][0]

        # 3. Get neightboor -> ne
        ne = get_diff_neightboor(comarques, veins, t, c)  
        if ne == -1:
            return
        # 4. Get conqueror neightboot -> c_ne  
        c_ne = comarques[ne][0]

        # 5. Fight
        #print( 'Lucha entre {}( de {}) y {} (de {})'.format(t,c,ne,c_ne))
        winner, lost, terr = fight(step, t, c, ne, c_ne)
        
        # 6. Assign output
        comarques[terr][0] = winner

        # 7. Generate output
        output = generate_output(comarques, winner, lost, terr, step)

        # 8. Save step and generate map
        ctrl_data.save_step(step, {"comarques": comarques})
        map_game.print_step(step, comarques, veins, winner, terr, lost)

    return comarques, output