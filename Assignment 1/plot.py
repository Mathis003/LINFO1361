import pandas as pd
import matplotlib.pyplot as plt

names_program = ["BFS_Graph", "BFS_Tree", "Depth_Limited_Search", "Iterative_Deepening_Search"]

### Collect DATAS ###

moyennes = []
ecart_types = []
medians = []

colors = ["#FF5733", "#5F9EA0", "#FFD700", "#8A2BE2", "#32CD32"]

for i in range(len(names_program)):

    data = pd.read_csv("csv/" + names_program[i] + ".csv")

    # Clean datas and convert them into numbers
    for col in data.columns[1:]:
        data[col] = data[col].apply(lambda x: float(x.split('m')[-1].split('s')[0]) if 'm' in x and 's' in x else None)

    # Calculate means, std and medians
    moyennes.append(data.drop(columns=['Instance']).mean(axis=1))
    ecart_types.append(data.drop(columns=['Instance']).std(axis=1))
    medians.append(data.drop(columns=['Instance']).median(axis=1))

    instances = data['Instance']

### Graph CREATION ###

plt.figure(figsize=(10, 6))

for i in range(len(names_program)):

    # plt.errorbar(instances, moyennes[i], yerr=ecart_types[i], fmt='o', color=colors[i], label=names_program[i])

    plt.plot(instances, medians[i], marker='o', linestyle='-', color=colors[i], label=names_program[i])  # Pas besoin de légende ici

plt.xlabel('Instances')
plt.ylabel('Temps d\'exécution (s)')
plt.yscale('log')
plt.title('Comparaison des temps d\'exécution pour différentes instances\npour des algorithmes de recherche non informée différent')

plt.legend(title="Algorithmes", loc='upper left')

plt.grid(True)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.show()
