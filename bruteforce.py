import pandas as pd
import itertools
import time

FILE_PATH = 'datas/datas00.xlsx'
MONEY = 500


def pick_actions():
    combinations_list = []
    datas = pd.read_excel(FILE_PATH, header=None)
    actions_list = datas.values.tolist()

    for i in range(1, len(actions_list) + 1):
        combinations = list(itertools.combinations(actions_list, i))
        for actions in combinations:
            if sum(action[1] for action in actions) <= MONEY:
                combinations_list.append(actions)

    return combinations_list


def calculate_gain(actions):
    total_gain = 0
    for action in actions:
        gain = action[1] * (1 + action[2])
        total_gain += gain
    return total_gain


def check_best_combination():
    combinations_list = pick_actions()
    best_combination = None
    best_combinaison_gain = 0

    for combinaison in combinations_list:
        combinaison_gain = calculate_gain(combinaison)
        if combinaison_gain > best_combinaison_gain:
            best_combinaison_gain = combinaison_gain
            best_combination = combinaison

    return best_combination, best_combinaison_gain


def run_bruteforce():

    start_time = time.time()

    best_combination, best_combinaison_gain = check_best_combination()

    best_actions_names = [action[0] for action in best_combination]
    total_invest = sum([action[1] for action in best_combination])

    print(f"Start invest : {total_invest}")
    print(f"Total value after 2y : {round(best_combinaison_gain, 2)}")
    print(f"Recommended actions : {best_actions_names}")

    total_time = time.time() - start_time
    print(round(total_time, 2))


if __name__ == "__main__":
    run_bruteforce()