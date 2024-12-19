import matplotlib.pyplot as plt
import numpy as np

# Generiramo podatke za eno skupino s 100 stolpci
np.random.seed(0)  # Za reproducibilnost
group1 = {'oseba' + str(i): [(np.random.randint(1, 5), np.random.randint(6, 10)) for _ in range(5)] for i in range(1, 21)}

# Priprava podatkov
def prepare_data(group):
    starts = []
    ends = []
    positions = []
    for i, (person, levels) in enumerate(group.items()):
        for j, (start_level, end_level) in enumerate(levels):
            starts.append(start_level)
            ends.append(end_level)
            positions.append(i * len(levels) + j + 1)
    return starts, ends, positions

starts1, ends1, positions1 = prepare_data(group1)

# Širina stolpcev
bar_width = 0.8

# Ustvarimo stolpčni graf
plt.figure(figsize=(20, 10))

# Prikazujemo podatke za skupino kot stolpce
for start, end, pos in zip(starts1, ends1, positions1):
    plt.bar(pos, end - start, bottom=start, width=bar_width, color='#ff9999', edgecolor='black')

# Dodamo oznake in legendo
plt.xlabel('Igra')
plt.ylabel('Nivo')
plt.title('Začetni in končni nivo igranja za skupino')
plt.grid(True, axis='y')

# Nastavimo y-os tako, da začne pri 1
plt.ylim(0, 10)  # Nastavite meje glede na vaše podatke
plt.xticks(range(1, len(positions1) + 1))
plt.show()
