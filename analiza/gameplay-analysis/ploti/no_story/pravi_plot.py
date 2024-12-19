import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Preberi podatke iz CSV datoteke
df = pd.read_csv('final_no_story.csv')

# Sortiraj DataFrame po Odgovor na glasbo in Odgovor na videoigre
df = df.sort_values(by=['Odgovor na glasbo', 'Odgovor na videoigre'], ascending=[True, True])

# Shrani DataFrame v CSV datoteko
df.to_csv('final_no_story.csv', index=False)

# Priprava barvne lestvice glede na frekvence
norm = plt.Normalize(df['Frequency'].min(), df['Frequency'].max())
#cmap = sns.color_palette("Blues", as_cmap=True)
cmap = sns.light_palette("#0A496F", as_cmap=True)

# Ustvarimo stolpčni graf z manjšimi dimenzijami
fig, ax = plt.subplots(figsize=(12, 8))  # Prilagodil sem velikost

bar_width = 0.9  # Širina stolpcev
position = 0.5  # Začetna pozicija za prvi stolpec
person_positions = {}
person_labels = {}

# Track the last position of the person without a musical background
last_no_music_position = None

# Prikazujemo podatke za skupino kot akumulativne stolpce
for person_index, person in enumerate(df['Person'].unique(), start=1):
    person_data = df[df['Person'] == person]
    start_pos = position
    for start_level in [1, 6, 11, 16]:
        cumulative_frequency = np.zeros(22)  # Ustvari niz za akumulativno frekvenco do nivoja 21
        for _, row in person_data[person_data['Start'] == start_level].iterrows():
            end_level = row['End']
            frequency = row['Frequency']
            # Dodajanje frekvenc kumulativnemu nizu
            for level in range(start_level, end_level + 1):
                cumulative_frequency[level] += frequency
        # Risanje delov stolpcev z akumulirano frekvenco
        for level in range(start_level, 22):
            if cumulative_frequency[level] > 0:
                # Barva za določen nivo
                color = cmap(norm(cumulative_frequency[level]))
                # Risanje nivoja kot posamezno vrstico
                ax.bar(position, 1, bottom=level, width=bar_width, color=color, edgecolor='black')
        position += 1
        # Dodajanje sivih črtkanih črt samo na levi strani vsakega stolpca, ki se začne iz nivoja ena in se razteza do vrha grafa
        if start_level == 1:
            ax.axvline(x=position - 1.5, ymin=0, ymax=1, color='gray', linestyle='--', linewidth=0.5)
    person_positions[person] = (start_pos, position - 1)
    person_labels[person] = f'Oseba {person_index}'
    if df[df['Person'] == person]['Odgovor na glasbo'].iloc[0] == False:
        last_no_music_position = position - 0.5  # Update the last position of the person without musical background

    # Add the video game playing answer text below the bars for the person
    video_game_answer = df[df['Person'] == person]['Odgovor na videoigre'].iloc[0]
    ax.text((start_pos + position - 1) / 2, -0.5, video_game_answer, ha='center', va='center', fontsize=15, rotation=0)

    position += 0.5  # Manjši razmik med različnimi igralci

# Dodajmo oznako [h/mesec] na konec vseh odgovorov na videoigre pod x osjo
ax.text(position, -0.5, '[h/mesec]', ha='left', va='center', fontsize=15)


# Odstranitev oznak na x-osi
ax.set_xticks([])
ax.set_xticklabels([])

# Dodamo oznake in legendo
ax.set_xlabel('Čas igranja videoiger na mesec in glasbena izobrazba', labelpad=100, fontsize=17)
ax.set_ylabel('Nivo', fontsize=17)
ax.set_title('Prikaz pogostosti igranja nivojev igre brez zgodbe', pad=110, fontsize = 20)
ax.grid(True, axis='y')

# Nastavimo y-os tako, da začne pri 1
ax.set_ylim(1, 22)  # Nastavite meje glede na vaše podatke

# Dodamo glavne in pomožne oznake y-osi
ax.set_yticks([1, 6, 11, 16, 21])
ax.set_yticks(np.arange(1, 23), minor=True)
ax.tick_params(axis='x', labelsize=15)  # Nastavitev velikosti pisave za x os
ax.tick_params(axis='y', labelsize=15)

# Dodamo puščice in oznake za igralce
no_music_start = None
music_start = None

for person, (start_pos, end_pos) in person_positions.items():
    ax.annotate('', xy=(start_pos, 0.5), xytext=(end_pos, 0.5), arrowprops=dict(arrowstyle='|-|', color='black'))
    answer_music = df[df['Person'] == person]['Odgovor na glasbo'].iloc[0]
    if answer_music == True:
        if music_start is None:
            music_start = start_pos
        music_end = end_pos
    else:
        if no_music_start is None:
            no_music_start = start_pos
        no_music_end = end_pos

# Dodajmo oznake za vsako osebo nad grafom
for person, (start_pos, end_pos) in person_positions.items():
    label_position = (start_pos + end_pos) / 2 + 0.8
    ax.text(label_position, 25, person_labels[person], ha='center', va='center', fontsize=15, rotation=70, bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))

# Dodajmo oznake za glasbeno izobrazbo
ax.text(last_no_music_position / 2, -3, 'Brez glasbene izobrazbe', ha='center', va='center', fontsize=15)
ax.text((last_no_music_position + position) / 2, -3, 'Z glasbeno izobrazbo', ha='center', va='center', fontsize=15)

plt.tight_layout()

# Dodamo barvno lestvico
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Frekvenca', fontsize = 16)
cbar.ax.tick_params(labelsize=15)

plt.savefig('graf.png', bbox_inches='tight')  # Shrani graf kot sliko 'graf.png' z ustreznimi mejami
plt.show()
