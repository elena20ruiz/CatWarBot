
import random, json, queue
from catwarbot import ctrl_data

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


def run_step(step):
    comarques = ctrl_data.load_comarques()
    veins = ctrl_data.load_veins()

    # 1. Get random id -> t
    n = len(comarques)
    t = random.randint(0, n - 1)

    # 2. Get conqueror -> c
    c = comarques[t][0]

    # 3. Get neightboor -> ne

    print('Empienza el movimiento en el territorio {}, perteneciente a {}'.format(t, c))
    ne = get_diff_neightboor(comarques, veins, t, c)    
    if ne == -1:
        return
    print( 'Lucha entre {}( de {}) y {}'.format(t,c,ne))


    if step < 400:
        # Fight!
        fight = random.randint(0,1)

        if fight < 0.5:

            ant = comarques[ne][0]

            # wins c
            comarques[ne][0] = c
            print('Se ha expandido ', comarques[c][1], ' conquiriendo ', comarques[ne][1], ' anteriormente era de ', comarques[ant][1])

        else:
            # wins ne
            ant = comarques[t][0]
            comarques[t][0] = ne
            print('Se ha expandido ', comarques[ne][1], ' conquiriendo ', comarques[t][1], ' anteriormente era de ', comarques[ant][1])

    else:
        ant = comarques[ne][0]

        # wins c
        comarques[ne][0] = c
        print('Se ha expandido ', comarques[c][1], ' conquiriendo ', comarques[ne][1], ' anteriormente era de ', comarques[ant][1])

    #print('Resultado mapa:')
    # print(comarques)
    ctrl_data.save_step(step, {"comarques": comarques})

    return comarques