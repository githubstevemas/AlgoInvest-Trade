import pandas as pd
import random

FILE_PATH = 'datas/datas.xlsx'
MONEY = 500


def calculate_gain(stock_actions_list):

    for actions in stock_actions_list:

        total_gain = 0
        gain_action = 0
        for action in actions:
            gain_action += action["value"] * action["gain"]
            action["gain action"] = gain_action
            total_gain += gain_action

        actions.append(total_gain)
    return stock_actions_list


def choose_actions_to_buy():
    stock_actions_list = []
    boucle = 65536
    while boucle > 0:

        datas = pd.read_excel(FILE_PATH)
        actions_list = datas.to_dict(orient='records')

        nb_actions = random.randint(1, 17)
        choosen_actions = []

        # create stock portfolio with random actions
        for i in range(nb_actions):
            rand_action = random.choice(actions_list)
            choosen_actions.append(rand_action)
            actions_list.remove(rand_action)

        # sort actions lists, check if choosen actions not already in list and if cost < money account
        sorted_actions_names = sorted(choosen_actions, key=lambda dico: int(dico['name'].strip('#')))

        if sorted_actions_names not in stock_actions_list:
            if sum([action["value"] for action in sorted_actions_names]) < MONEY:
                stock_actions_list.append(choosen_actions)
                boucle -= 1
                print(f"Non tested : {boucle}")
            else:
                boucle -= 1
                print(f"Non tested : {boucle}")

    return stock_actions_list


stock_actions_list = choose_actions_to_buy()
final_list = calculate_gain(stock_actions_list)

best = max(final_list, key=lambda x: x[-1])

print(f"Total best gain : {round(best[-1], 2)}")
best.pop(-1)
best_names = [action["name"] for action in best]
print(f"Winners : {best_names}")
print(f"Start invest : {sum([action["value"] for action in best])}")
