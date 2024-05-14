import pandas as pd
import random

file_path = 'datas/datas.xlsx'
df = pd.read_excel(file_path)
dico = df.to_dict(orient='records')

wallet = 500
new_dico = []
while wallet > 0:
    rand_action = random.choice(dico)
    if wallet < rand_action["cout"]:
        break
    wallet -= rand_action["cout"]
    dico.remove(rand_action)
    new_dico.append(rand_action)

print(f"reste wallet : {wallet}$.")
total_benef = 0
for action in new_dico:
    benef = action["cout"] * action["benef"]
    total_benef += benef

print(f"total benef 2 ans : {total_benef:.2f}$.")
