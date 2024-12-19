import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Priprava podatkov
data = {
    'Name': [
        'No_Taja_93e_games.csv', 'Story_Natalija_580_games.csv',
        'Story_Tajda_c3d_games.csv', 'No_Ajda_862_games.csv', 'Story_MajaJ_c96_games.csv',
        'Story_Prosky_games.csv', 'Story_Lucija_7e8_games.csv', 'Story_Zoja_7d6_games.csv',
        'Story_NinaU_602_games.csv', 'No_Masa_b14_games.csv', 'No_Rene_fbc_games.csv',
        'Story_NinaP_games.csv', 'No_Mark_games.csv', 'Story_Klara_4ca_games.csv',
        'No_MajaL_feb_games.csv', 'No_Ziga_games.csv', 'Story_Anej_games.csv',
        'Story_Jurij_games.csv', 'No_Aljaz_games.csv', 'No_Mitja_games.csv',
        'No_Mirkala_8be_games.csv', 'No_Sarah_717_games.csv', 'No_Jernej_848_games.csv',
        'Story_NinaKa_2ea_games.csv', 'Story_Tilen_games.csv', 'No_Okti_games.csv',
        'Story_Jan_games.csv', 'Story_Tej_a_49d_games.csv', 'No_Gasper_games.csv',
        'No_Gloria_f97_games.csv'
    ],
    'Seconds': [
        685, 778, 1312, 2413, 2713, 2770, 2886, 3239, 3804, 3945, 4910, 4976, 5041, 5264,
        5664, 6667, 7743, 8521, 8758, 8885, 9033, 9118, 9471, 9699, 10073, 11125, 12611, 13653,
        25094, 31608
    ]
}

# Ustvarjanje DataFrame-a
df = pd.DataFrame(data)

# Dodajanje stolpca za vrsto igre
df['Type'] = df['Name'].apply(lambda x: 'Z zgodbo' if 'Story' in x else 'Brez zgodbe')
# Pretvorba sekund v minute in zaokroževanje
df['Minutes'] = df['Seconds'] / 60
df['Minutes'] = df['Minutes'].round(2)

# Ustvarjanje grafa
plt.figure(figsize=(6, 6))

# Uporaba seaborn za ustvarjanje strip plota s pastelni barvami
palette = {'Z zgodbo': '#64A041', 'Brez zgodbe': '#D47D9F'}
sns.stripplot(x='Type', y='Minutes', data=df, jitter=True, palette=palette, size=12, alpha=1.0)

# Dodajanje oznak in naslova
plt.xlabel('Verzija igre', fontsize=13, labelpad=15)
plt.ylabel('Čas igranja [min]', fontsize=13, labelpad=15)
plt.title('Primerjava časa igranja obeh verzij igre', fontsize=15, pad=20)

# Povečanje velikosti oznak za os y in x
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Prikaz grafa
plt.tight_layout()

# Prikaz grafa
plt.show()
