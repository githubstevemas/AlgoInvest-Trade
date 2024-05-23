import pandas as pd
import time

FILE_PATH = 'datas/datas00.xlsx'
MONEY = 500


def pick_actions(gains, values, names):

    combinaisons = []
    for i in range(len(names) + 1):
        combinaisons.append([])
        for j in range(MONEY + 1):
            combinaisons[i].append(0)

    for i in range(1, len(names) + 1):
        for current_money in range(1, MONEY + 1):
            if values[i-1] <= current_money:
                combinaisons[i][current_money] = max(combinaisons[i-1][current_money], gains[i-1] + combinaisons[i-1][current_money - values[i-1]])
            else:
                combinaisons[i][current_money] = combinaisons[i-1][current_money]

    n = len(names)
    chosen_actions = []
    chosen_gains = []
    chosen_values = []
    gains_total = 0
    max_money = MONEY

    while max_money > 0 and n > 0:
        if combinaisons[n][max_money] != combinaisons[n-1][max_money]:
            gains_total += values[n-1] * (1 + gains[n-1])
            chosen_gains.append(gains[n-1])
            chosen_actions.append(names[n-1])
            chosen_values.append(values[n - 1])
            max_money -= values[n-1]
        n -= 1

    return chosen_values, gains_total, chosen_actions


def run_optimized():

    start_time = time.time()
    datas = pd.read_excel(FILE_PATH, header=None)
    actions_names = datas[0].tolist()
    actions_values = datas[1].tolist()
    actions_gains = datas[2].tolist()

    chosen_values, gains_total, chosen_actions = pick_actions(actions_gains, actions_values, actions_names)

    print(f"Start invest : {sum(chosen_values)}")
    print(f"Total value after 2y : {round(gains_total, 2)}")
    print(f"Recommended actions : {chosen_actions}")

    total_time = time.time() - start_time
    print(round(total_time, 2))


if __name__ == "__main__":
    run_optimized()
