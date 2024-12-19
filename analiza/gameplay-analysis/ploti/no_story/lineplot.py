import matplotlib.pyplot as plt
import numpy as np

# Generiramo podatke za eno skupino s 100 stolpci
np.random.seed(0)
group1 = {'oseba' + str(i): [(np.random.randint(1, 5), np.random.randint(6, 10)) for _ in range(5)] for i in range(1, 21)}

# Priprava podatkov za line plot
for person, levels in group1.items():
    starts, ends = zip(*levels)
    plt.plot(range(len(starts)), starts, marker='o', label=f'{person} - start', linestyle='--')
    plt.plot(range(len(ends)), ends, marker='o', label=f'{person} - end')

# Dodamo oznake in legendo
plt.xlabel('Igra')
plt.ylabel('Nivo')
plt.title('Začetni in končni nivo igranja za skupino')
plt.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.show()
