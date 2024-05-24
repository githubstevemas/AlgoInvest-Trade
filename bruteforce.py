import pandas as pd
import itertools
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


def pick_actions(file_path):
    """ With file location get dataset and make a list of all combinaisons and return it """

    combinations_list = []
    datas = pd.read_csv(file_path, header=0)
    datas["profit"] = datas["profit"] / 100
    actions_list = datas.values.tolist()

    for i in range(1, len(actions_list) + 1):
        combinations = list(itertools.combinations(actions_list, i))
        for actions in combinations:
            if sum(action[1] for action in actions) <= MONEY:
                combinations_list.append(actions)

    return combinations_list


def calculate_gain(actions):
    """ With actions list calculate gains for each one """

    total_gain = 0
    for action in actions:
        gain = action[1] * (1 + action[2])
        total_gain += gain

    return total_gain


def check_best_combination(file_path):
    """ With dataset file location,
    run function to make all combinaisons
    and find witch one is the best and return it """

    combinations_list = pick_actions(file_path)
    best_combination = None
    best_combinaison_gain = 0

    for combinaison in combinations_list:
        combinaison_gain = calculate_gain(combinaison)
        if combinaison_gain > best_combinaison_gain:
            best_combinaison_gain = combinaison_gain
            best_combination = combinaison

    return best_combination, best_combinaison_gain


def write_txt(chosen_actions, chosen_values, gains_total, file_path):
    """ Write txt file with results """

    file_name = os.path.basename(file_path)
    txt_path = os.path.splitext(file_name)[0]

    with open(f"datas/outputs/{txt_path}_brute.txt", "w") as file:
        file.write(f"Recommended to bought :\n{chosen_actions}\n"
                   f"Total cost : {chosen_values}$\n"
                   f"Total return : {round(gains_total - chosen_values, 2)}$")


def run_bruteforce(file_path):
    """ Start/stop profiling, and run main programm for bruteforce method """

    start_time, memory_before = profiling()

    best_combination, total_gains = check_best_combination(file_path)

    chosen_actions = [action[0] for action in best_combination]
    chosen_values = sum([action[1] for action in best_combination])

    end_time, memory_after = profiling()
    total_time = end_time - start_time
    total_memory = memory_after - memory_before

    write_txt(chosen_actions, chosen_values, total_gains, file_path)

    return total_time, total_memory


if __name__ == "__main__":
    run_bruteforce("datas/dataset01.csv")
