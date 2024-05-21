import bruteforce
import optimized


def main_menu():

    print("Choose data to analyse :\n")
    print("[1] Datas00\n")
    print("[2} Datas01\n")
    datas_choice = input("\nYour choice : ")
    print("\nChoose method :\n")
    print("[1] Brute force\n")
    print("[2] Optimized\n")
    method_choice = input("\nYour choice : ")

    if method_choice == "1":
        bruteforce.run_brute()
    if method_choice == "2":
        optimized.run_optimized()


if __name__ == "__main__":
    main_menu()