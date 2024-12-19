import os
import pandas as pd
from io import StringIO

# 3
def game_stats(df, old_csv_name):

    df['starttime'] = pd.to_datetime(df[" start"], utc=True, errors='coerce', format='%Y-%m-%d %H:%M:%S')
    df['finishtime'] = pd.to_datetime(df[' finish'], utc=True, errors='coerce', format='%Y-%m-%d %H:%M:%S')
    df['playtime'] = (df['finishtime'] - df['starttime']).dt.total_seconds()
    df['start_level'] = df[' start_level']
    df['finish_level'] = df[' finish_level']

    # Picks only the columns we want to keep
    output_df = df[['user_id', 'starttime', 'finishtime','playtime', 'start_level', 'finish_level']]

    # Add new row at the bottom, which contains the sum of all values in the 'playtime' column
    playtime_sum = output_df['playtime'].sum()
    name = old_csv_name
    sum_row = pd.DataFrame({'name': [name], 'user_id': ['Total'], 'starttime': [''], 'playtime': [playtime_sum], 'start_level': [''], 'finish_level': ['']})

    output_df = pd.concat([output_df, sum_row], ignore_index=True)
    #print(output_df)

    # Save the output DataFrame to a CSV file
    output_df.to_csv("processed_"+ old_csv_name, index=False)


# 2
# Creates a new CSV file with the same name as the input CSV file, but with 'post_' prefix
def create_post_csv(csv):
     postcsv_name = f'post_{os.path.basename(csv)}'
     first_dataframe = pd.read_csv(csv)

    #ocisti podvojene vrstice
     first_dataframe[' start'] = pd.to_datetime(first_dataframe[' start'], errors='coerce',utc=True)
     first_dataframe[' finish'] = pd.to_datetime(first_dataframe[' finish'], errors='coerce',utc=True)
     first_dataframe = first_dataframe.dropna(subset=[' start'])
     first_dataframe = first_dataframe.drop_duplicates(subset=' start', keep='first')

     game_stats(first_dataframe, csv)


# 1
def join_game_csvs(subdir_path, output_file, processed_csv_list):
    # Get all files in dir with "game" prefix
    csv_files = [f for f in os.listdir(subdir_path) if f.startswith('game') and f.endswith('.csv')]

    if not csv_files:
        print(f"There are no csv files in  {subdir_path}.")
        return

    # Create list of DataFrame objects from csv files
    dataframe_list = []
    for file in csv_files:
        path = os.path.join(subdir_path, file)
        dataframe = pd.read_csv(path)
        dataframe_list.append(dataframe)

    # join dataframes into one
    joined_dataframe = pd.concat(dataframe_list, ignore_index=True)

    # Save the joined DataFrame to the output CSV file
    joined_dataframe.to_csv(output_file, index=False)

    # Add path to the joined CSV to the list
    processed_csv_list.append(output_file)


# MAIN PROGRAM
base_path = './questdata'

processed_csv_list = []

# Find subdirs with "Story" prefix
for directory, subdirs, _ in os.walk(base_path):
    for subdirectory in subdirs:
        if subdirectory.startswith('Story') or subdirectory.startswith('No'):
            subdir_path = os.path.join(directory, subdirectory, 'files')
            output_file = f'{subdirectory}_games.csv'
            join_game_csvs(subdir_path, output_file, processed_csv_list)

# Na koncu imate seznam vseh poti do združenih CSV-jev
print("Seznam združenih CSV-jev:")
print(processed_csv_list)

# # Uporaba funkcije
for csv in processed_csv_list:
    create_post_csv(csv)

# Create csv of user, gametime
gameplay_data_path = './gameplay-analysis'
# Pridobi seznam vseh datotek v direktoriju
file_list = os.listdir(gameplay_data_path)

# Inicializiraj prazen DataFrame za shranjevanje zadnjih vrstic
combined_data = pd.DataFrame()

# Poišči in združi zadnje vrstice iz vseh CSV datotek
for file in file_list:
    if file.endswith('.csv'):

        # Preberi CSV datoteko
        df = pd.read_csv(os.path.join(gameplay_data_path, file))
        # Izberi samo stolpca 'name' in 'playtime'
        df = df[['name', 'playtime']]
        # Izberi zadnjo vrstico
        last_row = df.iloc[[-1]]
        # Dodaj zadnjo vrstico v skupne podatke
        combined_data = combined_data._append(last_row)
# Sortiraj podatke glede na stolpec 'playtime'
combined_data = combined_data.sort_values(by='playtime')
# Zapiši združene podatke v nov CSV
combined_data.to_csv('combined_gameplay_data.csv', index=False)