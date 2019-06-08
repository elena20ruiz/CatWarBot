
import json
def init_map():
    try:
        with open('catwarbot/data/comarques_original.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
        with open('catwarbot/data/comarques.json', 'w',  encoding="utf-8") as outfile:
            json.dump(data, outfile)
        return True
    except IOError as e:
        print('Cannot load comarques.json file')
        print(str(e))
        return False
    except Exception as e:
        print(str(e))

def save_step(i, data):
    try:
        with open('catwarbot/data/steps/comarques_{}.json'.format(i), 'w',  encoding="utf-8") as outfile:
            json.dump(data, outfile)
        with open('catwarbot/data/comarques.json', 'w', encoding="utf-8") as outfile:
            json.dump(data, outfile)
    except IOError as e:
        print('Cannot write the step')
        print(str(e))
        return False
    except Exception as e:
        print(str(e))

def load_comarques():
    try:
        with open('catwarbot/data/comarques.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            comarques = data['comarques']
            comarques = keystoint(comarques)
            return comarques
    except IOError as e:
        print('Cannot load comarques.json file')
        print(str(e))

def load_veins():
    try:
        with open('catwarbot/data/veins.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            comarques = data['veins']
            comarques = keystoint(comarques)
            return comarques
    except IOError as e:
        print('Cannot load veins.json file')
        print(str(e))


def keystoint(x):
    return {int(k): v for k, v in x.items()}