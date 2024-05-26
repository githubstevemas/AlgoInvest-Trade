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


def check_best_combination(names, combinaisons, values, profits):

    n = len(names)
    chosen_actions = []
    max_money = MONEY * 100

    while max_money > 0 and n > 0:
        if combinaisons[n][max_money] == combinaisons[n - 1][max_money - values[n - 1]] + profits[n - 1]:
            chosen_actions.append(names[n - 1])
            max_money -= values[n - 1]
        n -= 1

    total_cost = MONEY * 100 - max_money

    return chosen_actions, total_cost


def pick_actions(profits, values):
    """ With dataset file location,
        run function to make all combinaisons
        and find witch one is the best and return it """

    money_cents = MONEY * 100
    values = [int(value * 100) for value in values]

    combinaisons = [[0 for x in range(money_cents + 1)] for x in range(len(values) + 1)]

    for i in range(1, len(values) + 1):
        for current_money in range(1, money_cents + 1):
            if values[i - 1] <= current_money:
                combinaisons[i][current_money] = max(profits[i - 1] +
                                                     combinaisons[i - 1][current_money - values[i - 1]],
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
                   f"Total cost : {round(total_cost, 2)} $\n"
                   f"Total return : {best_profit} $")


def run_optimized(file_path):
    """ Start/stop profiling, and run main programm for optimized method """

    start_time, memory_before = profiling()

    datas = pd.read_csv(file_path, header=0)
    datas = datas[(datas["price"] > 0)]

    actions_names = datas["name"].tolist()
    actions_values = datas["price"].tolist()
    actions_gains = datas["profit"].tolist()
    actions_profits = [price * profit for price, profit in zip(actions_values * 100, actions_gains)]

    combinaisons, best_profit = pick_actions(actions_profits, actions_values)
    choosen_actions, total_cost = check_best_combination(actions_names, combinaisons, actions_values, actions_profits)

    end_time, memory_after = profiling()
    total_time = end_time - start_time
    total_memory = memory_after - memory_before

    write_txt(choosen_actions, total_cost, best_profit, file_path)

    return total_time, total_memory


if __name__ == "__main__":
    run_optimized("datas/dataset01.csv")
