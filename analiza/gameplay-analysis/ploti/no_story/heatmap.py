import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Generiramo podatke za eno skupino s 100 stolpci
np.random.seed(0)
group1 = {'oseba' + str(i): [(np.random.randint(1, 5), np.random.randint(6, 10)) for _ in range(5)] for i in range(1, 21)}

# Priprava podatkov za heatmap
data = []
max_level = 0
for i, (person, levels) in enumerate(group1.items()):
    for start_level, end_level in levels:
        data.append([i + 1, start_level, end_level])
        max_level = max(max_level, start_level, end_level)

# Preoblikovanje podatkov v matriko za heatmap
matrix = np.zeros((max_level, len(group1) * 5))
for d in data:
    matrix[d[1]-1, d[0]-1] += 1
    matrix[d[2]-1, d[0]-1] += 1

# Ustvarimo heatmap
plt.figure(figsize=(20, 10))
sns.heatmap(matrix, cmap='Reds', cbar=True, linewidths=0.5)
plt.xlabel('Igralec')
plt.ylabel('Nivo')
plt.title('Toplotni zemljevid začetnih in končnih nivojev za skupino')
plt.show()
