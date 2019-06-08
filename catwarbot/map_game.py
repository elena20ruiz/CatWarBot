from bs4 import BeautifulSoup
from catwarbot import game
import json
import statistics

def init_map():
    with open("catwarbot/map/mapa-final.xml") as fp:
        data = fp.read()
    with open("catwarbot/map/steps/mapa_0.svg", "w") as fp:
        fp.write(data)


def print_frontera(root, t1, t2, css_class):
    front = root.findAll(attrs={"id" : "com{}:{}".format(t1,t2)})
    if not front:
        front = root.findAll(attrs={"id" : "com{}:{}".format(t2,t1)})
    
    if front:
        if front[0].name == 'polyline':
            front[0]['class'] = css_class
        else:
            lines = front[0].findAll('polyline')
            for line in lines:
                line['class'] = css_class
            lines = front[0].findAll('polygon')
            for line in lines:
                line['class'] = css_class

def get_position(territoris, id_t):
    path = territoris.find(attrs={"id" : "com{}".format(id_t)})

    if path.name == 'path':
        position = path['d']
        position = position.split('l')[0]
        position = position[1:]
        positions = position.split(',')
    elif path.name == 'polygon':
        position = path['points'].split(' ')[0]
        positions = position.split(',')
    else:
        return -1
    positions[0] = float(positions[0])
    positions[1] = float(positions[1])
    return positions

def change_fronteres(fronteres, comarques, veins, territory):
    veins = veins[territory]

    for vei in veins:
        # If same put 'igual' color
        if comarques[vei][0] == comarques[territory][0]:
            print_frontera(fronteres, vei, territory, 'igual')
        elif comarques[vei][0] != comarques[territory][0]:
            print_frontera(fronteres, vei, territory, 'front')

def add_complete_territories(territoris, importants, comarques, veins, winner, lost, territory):

    # 1. Reset capes
    lines = importants.findAll('polyline')
    lines += importants.findAll('polygon')
    lines += importants.findAll('line')
    for line in lines:
        line['class'] = 'st46'

    # - Variables of positions
    positions_win = []
    positions_lost = []

    # 2. Get comarques to print
    all_winner = []
    all_lost = []

    # Get conquered
    for p in comarques:
        if comarques[p][0] == lost:
            all_lost.append(p)
        elif comarques[p][0] == winner:
            all_winner.append(p)

    # 3. Print each
    for com in all_lost:
        com_veins = veins[com]
        com_veins.append(-1)
        positions_lost.append(get_position(territoris, com))
        for vei in com_veins:
            if vei == -1:
                print_frontera(importants, vei, com, 'lost')
            elif comarques[vei][0] != comarques[com][0]:
                print_frontera(importants, vei, com, 'lost')
    
    for com in all_winner:
        com_veins = veins[com]
        com_veins.append(-1)
        positions_win.append(get_position(territoris, com))
        for vei in com_veins:
            if vei == -1:
                print_frontera(importants, vei, com, 'winner')
            elif comarques[vei][0] != comarques[com][0]:
                print_frontera(importants, vei, com, 'winner')

    return positions_win, positions_lost

def get_mean_positions(positions):

    max_pos = 720
    min_pos = 10

    all_x = []
    all_y = []

    for p in positions:
        all_x.append(p[0])
        all_y.append(p[1])
    
    if all_x and all_y:
        x = statistics.mean(all_x)
        y = statistics.mean(all_y)

        if x < min_pos:
            x = 10
        elif x > max_pos:
            x = max_pos
        
        if y < min_pos:
            y = 10
        elif y > max_pos:
            y = max_pos

        output = 'matrix(1 0 0 1 ' + str(x) + ' ' + str(y) + ')'
        return output
    else:
        return


def add_texts(texts, territoris, comarques, winner, lost, territory, positions):

    mean_win = get_mean_positions(positions[0])
    if not mean_win:
        mean_win = get_mean_positions([get_position(territoris, winner)])
    mean_lost = get_mean_positions(positions[1])
    if not mean_lost:
        mean_lost= get_mean_positions([get_position(territoris, lost)])

    name_1 = comarques[winner][1]
    name_2 = comarques[lost][1]
    name_3 = comarques[territory][1]

    text1 = texts.find(attrs={"id" : "winner"})
    text1.string = name_1
    text1['transform'] = mean_win

    if not game.there_are_anyone(comarques,lost):
        text2 = texts.find(attrs={"id" : "lost"})
        text2.string = ''
    else:
        text2 = texts.find(attrs={"id" : "lost"})
        text2.string = name_2
        text2['transform'] = mean_lost
    
    text3 = texts.find(attrs={"id" : "territory"})
    text3.string = name_3
    text3['transform'] = get_mean_positions([get_position(territoris, territory)])


def print_step(step, comarques, veins, winner, territory, lost):
    with open("catwarbot/map/steps/mapa_{}.svg".format(step)) as fp:
        root = BeautifulSoup(fp, 'xml')

    # Get capes
    elems = root.svg
    capas = elems.findAll('g')

    # Get territories and print new territory
    territoris = root.find(attrs={"id" : "territoris"})
    paths = territoris.findAll('path')
    path2 = territoris.findAll('polygon')
    paths += path2
    for path in paths:
        t_id = path['id']
        t_id = int(t_id[3:])
        if t_id == territory:
            path['class'] = 'com{}'.format(winner) 

    # Print selected
    territoris2 = root.find(attrs={"id" : "territoris2"})
    paths = territoris2.findAll('path')
    path2 = territoris2.findAll('polygon')
    paths += path2
    for path in paths:
        t_id = path['id']
        t_id = int(t_id[3:])
        if t_id == territory:
            path['class'] = 'selected'
        else:
            path['class'] = 'st46' 

    # Get frontera
    fronteres = root.find(attrs={"id" : "fronteres"})
    change_fronteres(fronteres, comarques, veins, territory)

    # Add actual front
    importants = root.find(attrs={"id" : "importants"})
    positions = add_complete_territories(territoris, importants, comarques, veins, winner, lost, territory)

    # Get frontera
    texts = root.find(attrs={"id" : "noms"})
    add_texts(texts, territoris, comarques, winner, lost, territory, positions)

    # Save SVG
    with open("catwarbot/map/steps/mapa_{}.svg".format(step+1), "w") as fp:
        fp.write(str(root))
