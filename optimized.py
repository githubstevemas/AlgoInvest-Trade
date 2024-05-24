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


def pick_actions(gains, values, names):
    """ With dataset file location,
        run function to make all combinaisons
        and find witch one is the best and return it """

    money_cents = MONEY * 100
    values = [int(value * 100) for value in values]

    combinaisons = [[0] * (money_cents + 1) for _ in range(len(names) + 1)]

    for i in range(1, len(names) + 1):
        for current_money in range(1, money_cents + 1):
            if values[i - 1] <= current_money:
                previous_value = combinaisons[i - 1][current_money - values[i - 1]]
                combinaisons[i][current_money] = max(combinaisons[i - 1][current_money], gains[i - 1] + previous_value)
            else:
                combinaisons[i][current_money] = combinaisons[i - 1][current_money]

    n = len(names)
    chosen_actions = []
    chosen_gains = []
    chosen_values = []
    gains_total = 0
    max_money = money_cents

    while max_money > 0 and n > 0:
        if combinaisons[n][max_money] != combinaisons[n - 1][max_money]:
            if max_money - values[n - 1] >= 0:
                gains_total += values[n - 1] * (1 + gains[n - 1])
                chosen_gains.append(gains[n - 1])
                chosen_actions.append(names[n - 1])
                chosen_values.append(values[n - 1] / 100)
                max_money -= values[n - 1]
        n -= 1

    return chosen_values, gains_total / 100, chosen_actions


def write_txt(chosen_actions, chosen_values, gains_total, file_path):
    """ Write txt file with results """

    file_name = os.path.basename(file_path)
    txt_path = os.path.splitext(file_name)[0]

    with open(f"datas/outputs/{txt_path}_opti.txt", "w") as file:
        file.write(f"Recommended to bought :\n{chosen_actions}\n"
                   f"Total cost : {round(sum(chosen_values), 2)}$\n"
                   f"Total return : {round(gains_total - sum(chosen_values), 2)}$")


def run_optimized(file_path):
    """ Start/stop profiling, and run main programm for optimized method """

    start_time, memory_before = profiling()

    datas = pd.read_csv(file_path, header=0)
    datas["profit"] = datas["profit"] / 100
    datas = datas[datas['price'] > 0]
    actions_names = datas["name"].tolist()
    actions_values = datas["price"].tolist()
    actions_gains = datas["profit"].tolist()

    chosen_values, gains_total, chosen_actions = pick_actions(actions_gains, actions_values, actions_names)

    end_time, memory_after = profiling()
    total_time = end_time - start_time
    total_memory = memory_after - memory_before

    write_txt(chosen_actions, chosen_values, gains_total, file_path)

    return total_time, total_memory


if __name__ == "__main__":
    run_optimized("datas/dataset01.csv")
