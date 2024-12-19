import pandas
from scipy import stats
import warnings
from scipy.stats import wilcoxon
from scipy.stats import levene
warnings.filterwarnings("ignore")

# Options
include_vaja = False

# Read csv file into DataFrame
df_pre_proms = pandas.read_csv('./analiza/preanalysis-outputs/vsi_pre.csv')
df_post_proms = pandas.read_csv('./analiza/preanalysis-outputs/vsi_post_brez_coruption.csv')


# Compute the Student's t-test for the means of pre and post PROMs
# separate by sound column representing the task and by AbsoluteAsynchrony and RelativeAsynchrony
print('Student\'s t-test for the means of pre and post PROMs')
print('separate by sound column representing the task')
print('-----------------------------------------------------')
print('Rhythm')
print('AbsoluteAsynchrony')

df_rhythm_pre = df_pre_proms.query('block == "ritem" & (phase != "vaja" & phase != "vaje")')
df_rhythm_post = df_post_proms.query('block == "ritem" & (phase != "vaja" & phase != "vaje")')

# # exlude under 8000 secs playtime
# outlier_users = [
#     'Taja',
#     'Natalija',
#     'Tajda',
#     'Ajda',
#     'MajaJ',
#     'Prosky',
#     'Lucija',
#     'Zoja',
#     'NinaP',
#     'NinaU',
#     'Masa',
#     'Rene',
#     'Nina',
#     'Mark',
#     'Klara',
#     'MajaL',
#     'Ziga',
#     'Anej',
#     'Jurij',
# #     'Aljaz',
# #     'Mitja',
#     'Mirkala',
# #     'Sarah',
# #     'Jernej',
# #     'Tilen',
#     'Okti',
#     'Jan',
#     'Teja',
#     'Gasper',
#     'Gloria'
# ]
#mirkala, okti, jan out
#
# outlier_users = [
#     'Jurij',
#     'Aljaz',
#     'Mitja',
#     'Mirkala',
#     'Sarah',
#     'Jernej',
#     'Tilen',
#     'Okti',
#     'Jan',
#     'Teja',
#     'Gasper',
#     'Gloria'
# ]
# outlier_users = []

# # VSI
# outlier_users = [
#     'Anej',
#     'Jan',
#     'Jurij',
#     'Klara',
#     'Lucija',
#     'MajaJ',
#     'Natalija',
#     'NinaKa',
#     'NinaP',
#     'NinaU',
#     'Nina',
#     'Prosky',
#     'Tajda',
#     'Teja',
#     'Tilen',
#     'Zoja',
#     'Ajda',
#     'Aljaz',
#     'Gasper',
#     'Gloria',
#     'Jernej',
#     'MajaL',
#     'Mark',
#     'Masa',
#     'Mirkala',
#     'Mitja',
#     'Okti',
#     'Rene',
#     'Sarah',
#     'Taja',
#     'Ziga'
# ]

# #STORY
# outlier_users = [
#     'Anej',
#     'Jan',
#     'Jurij',
#     'Klara',
#     'Lucija',
#     'MajaJ',
#     'Natalija',
#     'NinaKa',
#     'NinaP',
#     'NinaU',
#     'Nina',
#     'Prosky',
#     'Tajda',
#     'Teja',
#     'Tilen',
#     'Zoja'
#  ]
# #
# #NO STORY
# outlier_users = [
#     'Ajda',
#     'Aljaz',
#     'Gasper',
#     'Gloria',
#     'Jernej',
#     'MajaL',
#     'Mark',
#     'Masa',
#     'Mirkala',
#     'Mitja',
#     'Okti',
#     'Rene',
#     'Sarah',
#     'Taja',
#     'Ziga'
# ]

# # vsi stran razen najmanj igrali
# outlier_users = [
#     'Lucija',
#     'NinaP',
#     'Masa',
#     'Rene',
#     'Nina',
#     'Mark',
#     'Klara',
#     'MajaL',
#     'Ziga',
#     'Anej',
#     'Jurij',
#     'Aljaz',
#     'Mitja',
#     'Mirkala',
#     'Sarah',
#     'Jernej',
#     'Tilen',
#     'Okti',
#     'Jan',
#     'Teja',
#     'Gasper',
#     'Gloria'
# ]
#
# vsi stran razen srednja skupina po igranju

outlier_users = [
    'Jan',
    'Lucija',
    'MajaJ',
    'Natalija',
    'NinaKa',
    'NinaU',
    'Nina',
    'Prosky',
    'Tajda',
    'Teja',
    'Tilen',
    'Zoja',
    'Ajda',
    'Gasper',
    'Gloria',
    'Jernej',
    'Masa',
    'Mirkala',
    'Okti',
    'Sarah',
    'Taja'
]
#
# # vsi stran razen najbolj igrani
# outlier_users = [
#     'Anej',
#     'Jurij',
#     'Klara',
#     'Lucija',
#     'MajaJ',
#     'Natalija',
#     'NinaP',
#     'NinaU',
#     'Nina',
#     'Prosky',
#     'Tajda',
#     'Zoja',
#     'Ajda',
#     'Aljaz',
#     'MajaL',
#     'Mark',
#     'Masa',
#     'Mitja',
#     'Rene',
#     'Taja',
#     'Ziga'
# ]

popravljeni_outlierji = [ime.capitalize() for ime in outlier_users]
#print(popravljeni_outlierji)

# Remove outlier user from both dataframes
df_rhythm_pre = df_rhythm_pre[~df_rhythm_pre['sbj'].isin(outlier_users)]
df_rhythm_post = df_rhythm_post[~df_rhythm_post['sbj'].isin(outlier_users)]

print(len(df_rhythm_pre['sbj'].unique()))
print(df_rhythm_post['sbj'].unique())

#Filter out the rows which have NaN value as AbsoluteAsynchrony in either dataframes
df_abs_rhythm_pre = df_rhythm_pre[df_rhythm_pre['AbsoluteAsynchrony'].notnull() & df_rhythm_post['AbsoluteAsynchrony'].notnull()]
df_abs_rhythm_post = df_rhythm_post[df_rhythm_pre['AbsoluteAsynchrony'].notnull() & df_rhythm_post['AbsoluteAsynchrony'].notnull()]

# Filter out the rows which have NaN value as RelativeAsynchrony in either dataframes
df_rel_rhythm_pre = df_rhythm_pre[df_rhythm_pre['RelativeAsynchrony'].notnull() & df_rhythm_post['RelativeAsynchrony'].notnull()]
df_rel_rhythm_post = df_rhythm_post[df_rhythm_pre['RelativeAsynchrony'].notnull() & df_rhythm_post['RelativeAsynchrony'].notnull()]


# For each sound column separately
for sound in df_abs_rhythm_pre['sound'].unique():
    print(f"===== {sound}")
#     if (sound == 'R_M1_tapping.wav' & df_abs_rhythm_pre['sbj'] == 'MajaJ'):
#         continue


    df_abs_rhythm_pre_sound = df_abs_rhythm_pre[df_abs_rhythm_pre['sound'] == sound]
    df_abs_rhythm_post_sound = df_abs_rhythm_post[df_rhythm_post['sound'] == sound]

    if df_abs_rhythm_post_sound.shape[0] != df_abs_rhythm_pre_sound.shape[0]:
        continue
    print(f"\n===== {sound}")

  # Zapiši podatke v CSV
    df_abs_rhythm_pre_sound.to_csv(f'abs_rhythm_pre_{sound}.csv', index=False)
    df_abs_rhythm_post_sound.to_csv(f'abs_rhythm_post_{sound}.csv', index=False)
   # print(df_abs_rhythm_pre_sound, df_abs_rhythm_post_sound)

    print("*********")
   # Print Mean, Standard Deviation, Pearson Correlation Coefficient and p-value
    print(f'Mean {df_abs_rhythm_pre_sound["AbsoluteAsynchrony"].mean()} {df_abs_rhythm_post_sound["AbsoluteAsynchrony"].mean()}')
    print(f'Standard Deviation {df_abs_rhythm_pre_sound["AbsoluteAsynchrony"].std()} {df_abs_rhythm_post_sound["AbsoluteAsynchrony"].std()}')
    print(f'Pearson Correlation Coefficient {df_abs_rhythm_pre_sound["AbsoluteAsynchrony"].corr(df_abs_rhythm_post_sound["AbsoluteAsynchrony"])}')
    print(f'p-value {stats.ttest_rel(df_abs_rhythm_pre_sound["AbsoluteAsynchrony"], df_abs_rhythm_post_sound["AbsoluteAsynchrony"], alternative="greater")}')
    print('-----------------------------------------------------')


    # Calculate and print Wilcoxon Signed-Rank Test
    wilcoxon_result = wilcoxon(df_abs_rhythm_pre_sound["AbsoluteAsynchrony"], df_abs_rhythm_post_sound["AbsoluteAsynchrony"])
    print(f'Wilcoxon test statistic: {wilcoxon_result.statistic}, p-value: {wilcoxon_result.pvalue}')

    # Calculate and print rank range
    ranks = df_abs_rhythm_pre_sound["AbsoluteAsynchrony"] - df_abs_rhythm_post_sound["AbsoluteAsynchrony"]
    ranks = ranks[ranks != 0].abs().rank()
    print(f'Range of ranks: {ranks.min()} - {ranks.max()}')
    print('-----------------------------------------------------')


  # Calculate and print Levene's test for equality of variances
    levene_stat, levene_p = levene(df_abs_rhythm_pre_sound["AbsoluteAsynchrony"], df_abs_rhythm_post_sound["AbsoluteAsynchrony"])
    print(f'Levenejev test: stat = {levene_stat}, p-vrednost = {levene_p}')
    print('-----------------------------------------------------')


    df_rel_rhythm_pre_sound = df_rel_rhythm_pre[df_rel_rhythm_pre['sound'] == sound]
    df_rel_rhythm_post_sound = df_rel_rhythm_post[df_rel_rhythm_post['sound'] == sound]

    if df_rel_rhythm_post_sound.shape[0] != df_rel_rhythm_pre_sound.shape[0]:
        continue

    print(f"===== {sound}")


    print('RelativeAsynchrony')

   # Print Mean, Standard Deviation, Pearson Correlation Coefficient and p-value
    print(f'Mean {df_rel_rhythm_pre_sound["RelativeAsynchrony"].mean()} {df_rel_rhythm_post_sound["RelativeAsynchrony"].mean()}')
    print(f'Standard Deviation {df_rel_rhythm_pre_sound["RelativeAsynchrony"].std()} {df_rel_rhythm_post_sound["RelativeAsynchrony"].std()}')
    print(f'Pearson Correlation Coefficient {df_rel_rhythm_pre_sound["RelativeAsynchrony"].corr(df_rel_rhythm_post_sound["RelativeAsynchrony"])}')
    print(f'p-value {stats.ttest_rel(df_rel_rhythm_pre_sound["RelativeAsynchrony"], df_rel_rhythm_post_sound["RelativeAsynchrony"], alternative="greater")}')

    # Calculate and print Levene's test for equality of variances
    levene_stat_rel, levene_p_rel = levene(df_rel_rhythm_pre_sound["RelativeAsynchrony"], df_rel_rhythm_post_sound["RelativeAsynchrony"])
    print(f'Levenejev test (RelativeAsynchrony): stat = {levene_stat_rel}, p-vrednost = {levene_p_rel}')
    print('-----------------------------------------------------')


    # Calculate and print Wilcoxon Signed-Rank Test for RelativeAsynchrony
    wilcoxon_rel_result = wilcoxon(df_rel_rhythm_pre_sound["RelativeAsynchrony"], df_rel_rhythm_post_sound["RelativeAsynchrony"])
    print(f'Wilcoxon test statistic (RelativeAsynchrony): {wilcoxon_rel_result.statistic}, p-value: {wilcoxon_rel_result.pvalue}')

    # Calculate and print rank range for RelativeAsynchrony
    ranks_rel = df_rel_rhythm_pre_sound["RelativeAsynchrony"] - df_rel_rhythm_post_sound["RelativeAsynchrony"]
    ranks_rel = ranks_rel[ranks_rel != 0].abs().rank()
    print(f'Range of ranks (RelativeAsynchrony): {ranks_rel.min()} - {ranks_rel.max()}')
    print('-----------------------------------------------------')



print('-----------------------------------------------------')
print('')
print('Tempo (only for Asynchrony)')


df_tempo_pre = df_pre_proms.query('block == "tempo" & (phase != "vaja" & phase != "vaje")')
df_tempo_post = df_post_proms.query('block == "tempo" & (phase != "vaja" & phase != "vaje")')

# Remove outlier user from both dataframes
df_tempo_pre = df_tempo_pre[~df_tempo_pre['sbj'].isin(outlier_users)]
df_tempo_post = df_tempo_post[~df_tempo_post['sbj'].isin(outlier_users)]

# Filter out the rows which have NaN value as Asynchrony in either dataframes
df_abs_tempo_pre = df_tempo_pre[df_tempo_pre['Asynchrony'].notnull() & df_tempo_post['Asynchrony'].notnull()]
df_abs_tempo_post = df_tempo_post[df_tempo_pre['Asynchrony'].notnull() & df_tempo_post['Asynchrony'].notnull()]

# For each sound column separately
for sound in df_abs_tempo_pre['sound'].unique():
    print(f"===== {sound}")
    df_abs_tempo_pre_sound = df_abs_tempo_pre[df_abs_tempo_pre['sound'] == sound]
    df_abs_tempo_post_sound = df_abs_tempo_post[df_abs_tempo_post['sound'] == sound]

   #  print(df_abs_tempo_pre_sound, df_abs_tempo_post_sound)
    df_abs_tempo_pre_sound.to_csv(f'abs_tempo_pre_{sound}.csv', index=False)
    df_abs_tempo_post_sound.to_csv(f'abs_tempo_post_{sound}.csv', index=False)

    # Print Mean, Standard Deviation, Pearson Correlation Coefficient and p-value
    print(f'Mean {df_abs_tempo_pre_sound["Asynchrony"].mean()} {df_abs_tempo_post_sound["Asynchrony"].mean()}')
    print(f'Standard Deviation {df_abs_tempo_pre_sound["Asynchrony"].std()} {df_abs_tempo_post_sound["Asynchrony"].std()}')
    print(f'Pearson Correlation Coefficient {df_abs_tempo_pre_sound["Asynchrony"].corr(df_abs_tempo_post_sound["Asynchrony"])}')
    print(f'p-value {stats.ttest_rel(df_abs_tempo_pre_sound["Asynchrony"], df_abs_tempo_post_sound["Asynchrony"], alternative="greater")}')
    print('-----------------------------------------------------')


   # Calculate and print Levene's test for equality of variances
    levene_stat_tempo, levene_p_tempo = levene(df_abs_tempo_pre_sound["Asynchrony"], df_abs_tempo_post_sound["Asynchrony"])
    print(f'Levenejev test (Tempo): stat = {levene_stat_tempo}, p-vrednost = {levene_p_tempo}')
    print('-----------------------------------------------------')


    # Calculate and print Wilcoxon Signed-Rank Test for Asynchrony in Tempo block
    wilcoxon_tempo_result = wilcoxon(df_abs_tempo_pre_sound["Asynchrony"], df_abs_tempo_post_sound["Asynchrony"])
    print(f'Wilcoxon test statistic (Tempo): {wilcoxon_tempo_result.statistic}, p-value: {wilcoxon_tempo_result.pvalue}')

    # Calculate and print rank range for Asynchrony in Tempo block
    ranks_tempo = df_abs_tempo_pre_sound["Asynchrony"] - df_abs_tempo_post_sound["Asynchrony"]
    ranks_tempo = ranks_tempo[ranks_tempo != 0].abs().rank()
    print(f'Range of ranks (Tempo): {ranks_tempo.min()} - {ranks_tempo.max()}')
    print('-----------------------------------------------------')