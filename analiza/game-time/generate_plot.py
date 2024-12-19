import matplotlib.pyplot as plt

# Podatki
data = [
    ("No_Taja_93e_games.csv", 685),
    ("Story_Natalija_580_games.csv", 778),
    ("Story_Tajda_c3d_games.csv", 1312),
    ("No_Ajda_862_games.csv", 2413),
    ("Story_MajaJ_c96_games.csv", 2713),
    ("Story_Prosky_games.csv", 2770),
    ("Story_Lucija_7e8_games.csv", 2886),
    ("Story_Zoja_7d6_games.csv", 3239),
    ("Story_NinaU_602_games.csv", 3804),
    ("No_Masa_b14_games.csv", 3945),
    ("No_Rene_fbc_games.csv", 4910),
    ("Story_NinaP_games.csv", 4976),
    ("No_Mark_games.csv", 5041),
    ("Story_Klara_4ca_games.csv", 5264),
    ("No_MajaL_feb_games.csv", 5664),
    ("No_Ziga_games.csv", 6667),
    ("Story_Anej_games.csv", 7743),
    ("Story_Jurij_games.csv", 8521),
    ("No_Aljaz_games.csv", 8758),
    ("No_Mitja_games.csv", 8885),
    ("No_Mirkala_8be_games.csv", 9033),
    ("No_Sarah_717_games.csv", 9118),
    ("No_Jernej_848_games.csv", 9471),
    ("Story_NinaKa_2ea_games.csv", 9699),
    ("Story_Tilen_games.csv", 10073),
    ("No_Okti_games.csv", 11125),
    ("Story_Jan_games.csv", 12611),
    ("Story_Tej_a_49d_games.csv", 13653),
    ("No_Gasper_games.csv", 25094),
    ("No_Gloria_f97_games.csv", 31608)
]

# Priprava podatkov za graf
y = [item[1] for item in data]
colors = ['red' if 'No' in item[0] else 'blue' for item in data]

# Ustvarjanje grafa
plt.figure(figsize=(12, 6))
plt.scatter(range(len(data)), y, c=colors)

# Oznake osi
plt.xticks([])
plt.xlabel('')
plt.ylabel('Čas (sekunde)')
plt.title('Čas v sekundah z barvami glede na prisotnost "No" v prvem stolpcu')

# Legenda
red_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='No')
blue_patch = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Story')
plt.legend(handles=[red_patch, blue_patch])

# Shranjevanje grafa
plt.savefig('graf.png')

# Prikaz grafa
plt.show()
