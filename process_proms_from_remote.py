import pandas
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

# Options
include_vaja = False

# Read csv file into DataFrame
df_pre_proms = pandas.read_csv('./analiza/nostorypre.csv')
df_post_proms = pandas.read_csv('./analiza/nostorypost.csv')


# Compute the Student's t-test for the means of pre and post PROMs
# separate by sound column representing the task and by AbsoluteAsynchrony and RelativeAsynchrony
print('Student\'s t-test for the means of pre and post PROMs')
print('separate by sound column representing the task')
print('-----------------------------------------------------')
print('Rhythm')
print('AbsoluteAsynchrony')

df_rhythm_pre = df_pre_proms.query('block == "ritem" & (phase != "vaja" & phase != "vaje")')
df_rhythm_post = df_post_proms.query('block == "ritem" & (phase != "vaja" & phase != "vaje")')

outlier_users = [
    '2225796f97692c3d4d3ff0bdebc13512df614678-1', # Random user
    '2225796f97692c3d4d3ff0bdebc13512df614678-2', # Random user
    '2225796f97692c3d4d3ff0bdebc13512df614678-3', # Random user
    '9ac02f6700b5fa6d1a3360a26727480e-1', # Lori
    #'72bdb79df0c1714322ce2fc32d45b2ad-1', # Nik
    #'72bdb79df0c1714322ce2fc32d45b2ad-2', # Pik
    #'e312a03f18c76df29a479bfa21057063-1'  # Jonatan
]

# Remove outlier user from both dataframes
df_rhythm_pre = df_rhythm_pre[~df_rhythm_pre['sbj'].isin(outlier_users)]
df_rhythm_post = df_rhythm_post[~df_rhythm_post['sbj'].isin(outlier_users)]

print(len(df_rhythm_pre['sbj'].unique()))

# Filter out the rows which have NaN value as AbsoluteAsynchrony in either dataframes
df_abs_rhythm_pre = df_rhythm_pre[df_rhythm_pre['AbsoluteAsynchrony'].notnull() & df_rhythm_post['AbsoluteAsynchrony'].notnull()]
df_abs_rhythm_post = df_rhythm_post[df_rhythm_pre['AbsoluteAsynchrony'].notnull() & df_rhythm_post['AbsoluteAsynchrony'].notnull()]

# Filter out the rows which have NaN value as RelativeAsynchrony in either dataframes
df_rel_rhythm_pre = df_rhythm_pre[df_rhythm_pre['RelativeAsynchrony'].notnull() & df_rhythm_post['RelativeAsynchrony'].notnull()]
df_rel_rhythm_post = df_rhythm_post[df_rhythm_pre['RelativeAsynchrony'].notnull() & df_rhythm_post['RelativeAsynchrony'].notnull()]

# Perform for each sound column separately
for sound in df_rhythm_pre['sound'].unique():
    df_abs_rhythm_pre_sound = df_abs_rhythm_pre[df_abs_rhythm_pre['sound'] == sound]
    df_abs_rhythm_post_sound = df_abs_rhythm_post[df_abs_rhythm_post['sound'] == sound]

    if df_abs_rhythm_post_sound.shape[0] != df_abs_rhythm_pre_sound.shape[0]:
        continue
    print(f"\n===== {sound}")
    print("*********")

    # Print Mean, Standard Deviation, Pearson Correlation Coefficient and p-value
    print(f'Mean {df_abs_rhythm_pre_sound["AbsoluteAsynchrony"].mean()} {df_abs_rhythm_post_sound["AbsoluteAsynchrony"].mean()}')
    print(f'Standard Deviation {df_abs_rhythm_pre_sound["AbsoluteAsynchrony"].std()} {df_abs_rhythm_post_sound["AbsoluteAsynchrony"].std()}')
    print(f'Pearson Correlation Coefficient {df_abs_rhythm_pre_sound["AbsoluteAsynchrony"].corr(df_abs_rhythm_post_sound["AbsoluteAsynchrony"])}')
    print(f'p-value {stats.ttest_rel(df_abs_rhythm_pre_sound["AbsoluteAsynchrony"], df_abs_rhythm_post_sound["AbsoluteAsynchrony"], alternative="greater")}')
    print('-----------------------------------------------------')

    df_rel_rhythm_pre_sound = df_rel_rhythm_pre[df_rel_rhythm_pre['sound'] == sound]
    df_rel_rhythm_post_sound = df_rel_rhythm_post[df_rel_rhythm_post['sound'] == sound]

    if df_rel_rhythm_post_sound.shape[0] != df_rel_rhythm_pre_sound.shape[0]:
        continue


    print('RelativeAsynchrony')

    # Print Mean, Standard Deviation, Pearson Correlation Coefficient and p-value
    print(f'Mean {df_rel_rhythm_pre_sound["RelativeAsynchrony"].mean()} {df_rel_rhythm_post_sound["RelativeAsynchrony"].mean()}')
    print(f'Standard Deviation {df_rel_rhythm_pre_sound["RelativeAsynchrony"].std()} {df_rel_rhythm_post_sound["RelativeAsynchrony"].std()}')
    print(f'Pearson Correlation Coefficient {df_rel_rhythm_pre_sound["RelativeAsynchrony"].corr(df_rel_rhythm_post_sound["RelativeAsynchrony"])}')
    print(f'p-value {stats.ttest_rel(df_rel_rhythm_pre_sound["RelativeAsynchrony"], df_rel_rhythm_post_sound["RelativeAsynchrony"], alternative="greater")}')

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

    # Print Mean, Standard Deviation, Pearson Correlation Coefficient and p-value
    print(f'Mean {df_abs_tempo_pre_sound["Asynchrony"].mean()} {df_abs_tempo_post_sound["Asynchrony"].mean()}')
    print(f'Standard Deviation {df_abs_tempo_pre_sound["Asynchrony"].std()} {df_abs_tempo_post_sound["Asynchrony"].std()}')
    print(f'Pearson Correlation Coefficient {df_abs_tempo_pre_sound["Asynchrony"].corr(df_abs_tempo_post_sound["Asynchrony"])}')
    print(f'p-value {stats.ttest_rel(df_abs_tempo_pre_sound["Asynchrony"], df_abs_tempo_post_sound["Asynchrony"], alternative="greater")}')
    print('-----------------------------------------------------')