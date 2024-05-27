import pandas as pd
import time
import psutil
import os

MONEY = 500

process = psutil.Process(os.getpid())


def profiling():
    """ Profile time and ram use during runing """

    curent_time = time.time()
    memory = process.memory_info()
    memory_mb = memory.rss / (1024 * 1024)
    return curent_time, memory_mb


def check_best_combination(combinaisons, action_list):
    """ With matrix combinaisons and dataset values, return actions names and their values """

    n = len(action_list)
    chosen_actions = []
    max_money = MONEY * 100

    while max_money > 0 and n > 0:
        if combinaisons[n][max_money] == combinaisons[n - 1][max_money - action_list[n - 1][1]] + action_list[n - 1][2]:
            chosen_actions.append(action_list[n - 1][0])
            max_money -= action_list[n - 1][1]
        n -= 1

    total_cost = MONEY * 100 - max_money

    return chosen_actions, total_cost


def pick_actions(actions_list):
    """ With action list,
        make combinaisons matrix and return it with the best profit """

    money_cents = MONEY * 100

    combinaisons = [[0 for x in range(money_cents + 1)] for x in range(len(actions_list) + 1)]

    for i in range(1, len(actions_list) + 1):
        for current_money in range(1, money_cents + 1):
            if actions_list[i - 1][1] <= current_money:
                combinaisons[i][current_money] = max(actions_list[i - 1][2] +
                                                     combinaisons[i - 1][current_money - actions_list[i - 1][1]],
                                                     combinaisons[i - 1][current_money])
            else:
                combinaisons[i][current_money] = combinaisons[i - 1][current_money]

    best_profit = combinaisons[-1][-1]

    return combinaisons, best_profit / 100


def write_txt(chosen_actions, best_profit, total_cost, file_path):
    """ Write txt file with results """

    file_name = os.path.basename(file_path)
    txt_path = os.path.splitext(file_name)[0]

    with open(f"datas/outputs/{txt_path}_opti.txt", "w") as file:
        file.write(f"Recommended to bought :\n{chosen_actions}\n"
                   f"Total cost : {round(total_cost, 2) / 100} $\n"
                   f"Total return : {best_profit} $")


def run_optimized(file_path):
    """ Start/stop profiling, and run main programm for optimized method """

    start_time, memory_before = profiling()

    datas = pd.read_csv(file_path, header=0)
    datas_list = datas.values.tolist()

    actions_list = []
    for action in datas_list:
        if float(action[1]) > 0 and float(action[2]) > 0:
            action_profit = round(float(action[1]) * float(action[2]))
            actions_list.append([action[0], round(float(action[1]) * 100), action_profit])

    combinaisons, best_profit = pick_actions(actions_list)

    chosen_actions, total_cost = check_best_combination(combinaisons, actions_list)

    end_time, memory_after = profiling()
    total_time = end_time - start_time
    total_memory = memory_after - memory_before

    write_txt(chosen_actions, best_profit, total_cost, file_path)

    return total_time, total_memory


if __name__ == "__main__":
    run_optimized("datas/dataset01.csv")
