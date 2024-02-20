import pandas as pd
import matplotlib.pyplot as plt

names_program = ["BFS_Graph", "BFS_Tree", "DFS_Graph", "IDS"]

### Collect DATAS ###

colors = ["#FF5733", "#5F9EA0", "#FFD700", "#8A2BE2", "#32CD32"]
runtimes = []

for i in range(len(names_program)):

    data = pd.read_csv("csv_evaluation/" + names_program[i] + ".csv")

    runtimes.append(data.iloc[:, 1])
    instances = data.iloc[:, 0]

### Graph CREATION ###

plt.figure(figsize=(10, 6))

for i in range(len(names_program)):
    # plt.errorbar(instances, moyennes[i], yerr=ecart_types[i], fmt='o', color=colors[i], label=names_program[i])
    plt.plot(instances, runtimes[i], marker='o', linestyle='-', color=colors[i], label=names_program[i]) 

plt.xlabel('Instances')
plt.ylabel('Temps d\'exécution (s)')
plt.yscale('log')
plt.title('Comparaison des temps d\'exécution pour différentes instances\npour des algorithmes de recherche non informée différent')

plt.legend(title="Algorithmes", loc='upper left')

plt.grid(True)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.savefig("Time_Exec_Comp.pdf")
# plt.show()
