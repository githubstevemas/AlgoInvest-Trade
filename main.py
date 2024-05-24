import matplotlib.pyplot as plt
import os

import bruteforce
import optimized


def edit_graph(time_brute, time_opti, ylabel, title):
    """ With matplotlib edit graphic results of profiling """

    categories = ["Brute Force", "Optimized"]
    valeurs = [time_brute, time_opti]

    plt.bar(categories, valeurs, color=["blue", "green"])

    plt.xlabel("Method")
    plt.ylabel(ylabel)
    plt.title(title)

    plt.savefig(f"datas/outputs/{title}.png")


def main_menu():
    """ Main menu, alow you to choose method of analysing """
    
    print("\nMenu\n")
    print("[1] Compare brute / Opti methods")
    print("[2] Choose dataset to run")
    choice = input("\nYour choice : ")

    if choice == "1":
        time_brute, memory_brute = bruteforce.run_bruteforce("datas/dataset01.csv")
        print(f"Time : {round(time_brute, 2)}secs / Memory : {round(memory_brute, 2)}MB")

        time_opti, memory_opti = optimized.run_optimized("datas/dataset01.csv")
        print(f"Time : {round(time_opti, 2)}secs / Memory : {round(memory_opti, 2)}MB")

        edit_graph(time_brute, time_opti, "Seconds", "Time performance")
        edit_graph(memory_brute, memory_opti, "MB", "Memory performance")

    if choice == "2":
        files = [f for f in os.listdir("datas/") if os.path.isfile(os.path.join("datas/", f))]

        print("\nChoose dataset to use : \n")
        for idx, file in enumerate(files, 1):
            print(f"[{idx}] {file}")
        csv_index = int(input("\nYour choice : ")) - 1
        file_path = os.path.join("datas/", files[csv_index])

        print("\nMethod to use :\n")
        print("[1] Brute force")
        print("[2] Optimized\n")
        method_choice = input("Your choice : ")

        if method_choice == "1":
            bruteforce.run_bruteforce(file_path)

        if method_choice == "2":
            optimized.run_optimized(file_path)


if __name__ == "__main__":
    main_menu()
