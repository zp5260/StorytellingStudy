import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter
import seaborn as sns

# Generiramo podatke za eno skupino s 15 igralci
np.random.seed(0)
group1 = {'oseba' + str(i): [(np.random.choice([1, 6, 11, 16]), np.random.randint(1, 21)) for _ in range(10)] for i in range(1, 16)}

# Priprava podatkov
data = []
for person, levels in group1.items():
    for start_level, end_level in levels:
        data.append((person, start_level, end_level))

# Uporaba Counter za štetje frekvence posameznih kombinacij
counter = Counter(data)
df = pd.DataFrame(counter.items(), columns=['Combination', 'Frequency'])
df[['Person', 'Start', 'End']] = pd.DataFrame(df['Combination'].tolist(), index=df.index)
df = df.drop(columns=['Combination'])

# Priprava barvne lestvice glede na frekvence
norm = plt.Normalize(df['Frequency'].min(), df['Frequency'].max())
cmap = sns.color_palette("Reds", as_cmap=True)

# Ustvarimo stolpčni graf
fig, ax = plt.subplots(figsize=(20, 10))

bar_width = 0.4
position = 0
person_positions = {}

# Prikazujemo podatke za skupino kot akumulativne stolpce
for person in df['Person'].unique():
    person_data = df[df['Person'] == person]
    start_pos = position
    for start_level in [1, 6, 11, 16]:
        cumulative_frequency = np.zeros(21)  # Ustvari niz za akumulativno frekvenco do nivoja 21
        for _, row in person_data[person_data['Start'] == start_level].iterrows():
            end_level = row['End']
            frequency = row['Frequency']
            for level in range(start_level, end_level + 1):
                cumulative_frequency[level] += frequency
            color = cmap(norm(cumulative_frequency[end_level]))
        # Risanje stolpca z akumulirano frekvenco
        for level in range(start_level, 21):
            if cumulative_frequency[level] > 0:
                ax.bar(position, level - start_level + 1, bottom=start_level, width=bar_width, color=cmap(norm(cumulative_frequency[level])), edgecolor='black')
        position += 1
    person_positions[person] = (start_pos, position - 1)
    position += 1  # Dodamo razmik med različnimi igralci

# Dodamo oznake in legendo
ax.set_xlabel('Igralec in nivo')
ax.set_ylabel('Nivo')
ax.set_title('Začetni in končni nivo igranja za skupino')
ax.grid(True, axis='y')

# Nastavimo y-os tako, da začne pri 1
ax.set_ylim(1, 21)  # Nastavite meje glede na vaše podatke

# Dodamo glavne in pomožne oznake y-osi
ax.set_yticks([1, 6, 11, 16, 21])
ax.set_yticks(np.arange(1, 22), minor=True)

# Odstranimo oznake in črtice na x-osi
ax.set_xticks([])
ax.set_xticklabels([])

# Dodamo puščice in oznake za igralce
for person, (start_pos, end_pos) in person_positions.items():
    ax.annotate('', xy=(start_pos, 0.5), xytext=(end_pos, 0.5), arrowprops=dict(arrowstyle='|-|', color='black'))
    ax.text((start_pos + end_pos) / 2, 0, person, ha='center', va='center', fontsize=10, bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))

plt.tight_layout()

# Dodamo barvno lestvico
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Frekvenca')

plt.show()
