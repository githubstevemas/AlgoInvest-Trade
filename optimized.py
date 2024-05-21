import pandas as pd

FILE_PATH = 'datas/datas01.xlsx'
MONEY = 500


def run_optimized(gains, values, max_money):

    n = len(actions_names)

    dp = []
    for i in range(n + 1):
        dp.append([])
        for j in range(max_money + 1):
            dp[i].append(0)

    for i in range(1, n + 1):
        for current_money in range(1, max_money + 1):
            if values[i-1] <= current_money:
                dp[i][current_money] = max(dp[i-1][current_money], gains[i-1] + dp[i-1][current_money - values[i-1]])
            else:
                dp[i][current_money] = dp[i-1][current_money]

    print(dp[n][max_money])


if __name__ == "__main__":

    datas = pd.read_excel(FILE_PATH, header=None)
    actions_names = datas[0].tolist()
    actions_values = datas[1].tolist()
    actions_gains = datas[2].tolist()

    run_optimized(actions_gains, actions_values, MONEY)
