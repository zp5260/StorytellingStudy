import matplotlib.pyplot as plt
import numpy as np

# Podatki
no_all = [821, 3651, 5724, 6726, 7737, 8873, 9930, 10520, 13854, 15544, 16428, 16442, 17333, 18642, 43932]
no_correct = [480, 1457, 3392, 5173, 5630, 7877, 7957, 8147, 9798, 10443, 12620, 13460, 13011, 16893, 33891]
story_all = [967, 2292, 3296, 4889, 4908, 5463, 5916, 8509, 9343, 15188, 15346, 15965, 16615, 17387, 25175]
story_correct = [468, 1084, 1450, 3890, 3826, 2624, 4432, 6200, 7830, 10242, 10302, 11717, 13072, 13200, 19547]

# Sortiranje podatkov glede na odstotke
no_percentages = [(c / a) * 100 for a, c in zip(no_all, no_correct)]
story_percentages = [(c / a) * 100 for a, c in zip(story_all, story_correct)]

sorted_no = sorted(zip(no_all, no_correct, no_percentages), key=lambda x: x[2])
sorted_story = sorted(zip(story_all, story_correct, story_percentages), key=lambda x: x[2])

# Razpakiranje podatkov
no_all_sorted, no_correct_sorted, no_percentages_sorted = zip(*sorted_no)
story_all_sorted, story_correct_sorted, story_percentages_sorted = zip(*sorted_story)

# Priprava procentov za prikaz
no_percentages_labels = [f"{p:.1f}%" for p in no_percentages_sorted]
story_percentages_labels = [f"{p:.1f}%" for p in story_percentages_sorted]

# Izračun povprečja procentov
avg_no_percentage = np.mean(no_percentages)
avg_story_percentage = np.mean(story_percentages)

story_label = f'Z zgodbo, Povp: {avg_story_percentage:.1f}%'
no_label = f'Brez zgodbe, Povp: {avg_no_percentage:.1f}%'

# Ustvarjanje figure in podgrafov
fig, ax = plt.subplots()

# Nastavitev položajev in širine za stolpce
pos = np.arange(len(no_all_sorted))
bar_width = 0.4

# Risanje stolpcev
for i in range(len(no_all_sorted)):
    ax.barh(pos[i], story_correct_sorted[i], bar_width, label=story_label if i == 0 else "", color='#64A041')
    ax.barh(pos[i], story_all_sorted[i] - story_correct_sorted[i], bar_width, left=story_correct_sorted[i], color='#8DB973')
    ax.barh(pos[i], -no_correct_sorted[i], bar_width, label=no_label if i == 0 else "", color='#D47D9F')
    ax.barh(pos[i], -(no_all_sorted[i] - no_correct_sorted[i]), bar_width, left=-no_correct_sorted[i], color='#E2B2C5')

    # Dodajanje odstotkov
    ax.text(story_all_sorted[i] + 500, pos[i], story_percentages_labels[i], va='center', ha='left', color='black')
    ax.text(-(no_all_sorted[i] + 500), pos[i], no_percentages_labels[i], va='center', ha='right', color='black')

# Odstranjevanje y osi in levi rob ter y oznake
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(left=False)
ax.set_yticklabels([])

# Dodajanje oznak
ax.set_yticks(pos)
ax.set_yticklabels([])
ax.set_xlabel('Število udarcev na bobne (uspešnih in vseh)')
ax.set_ylabel('Testiranci', labelpad=12, fontsize=13)
ax.set_title('Prikaz števila uspešno izvedenih udarcev napram\nvsem udarcem za testirance', pad=12)

# Dodajanje povprečij v legendo
ax.legend(loc='lower left', bbox_to_anchor=(-0.1, 0))

# Dodajanje navpične črte na ničli kot referenca
plt.axvline(0, color='grey', linewidth=0.8)

# Prikaz grafa
plt.show()
