import pandas as pd
import itertools

FILE_PATH = 'datas/datas00.xlsx'
MONEY = 500


def calculate_gain(combinations_list):

    for actions in combinations_list:

        total_gain = 0
        gain_action = 0
        for action in actions:
            gain_action += action[1] * action[2]
            action.append(gain_action)
            total_gain += gain_action
        actions.append(total_gain)

    return combinations_list


def pick_actions():

    combinations_list = []
    datas = pd.read_excel(FILE_PATH, header=None)
    actions_list = datas.values.tolist()

    for i in range(1, len(actions_list) + 1):
        combinations = list(itertools.combinations(actions_list, i))

        for actions in combinations:
            print(actions)

            if sum(action[1] for action in actions) <= MONEY:
                print("prix combo ok")
                combinations_list.append(list(actions))
            else:
                print("prix trop cher pour notre petit porte monaie..")

    return combinations_list


def display_winning_combo(final_list):
    best = max(final_list, key=lambda x: x[-1])

    print(f"Total best gain : {round(best[-1], 2)}")
    best.pop(-1)
    best_names = [action[0] for action in best]
    print(f"Winners : {best_names}")
    print(f"Start invest : {sum([action[1] for action in best])}")


def run_brute():
    combinations_list = pick_actions()
    final_list = calculate_gain(combinations_list)
    display_winning_combo(final_list)


if __name__ == "__main__":
    run_brute()
