import os
import csv

# Define the correct root directory based on the image structure
root_dir = '../../analiza/questdata/'

# Initialize an empty list to store the results
results = []

# Iterate over each user directory in the root directory
for user_dir in os.listdir(root_dir):
    user_path = os.path.join(root_dir, user_dir)
    if os.path.isdir(user_path):
        files_path = os.path.join(user_path, "files")
        if os.path.isdir(files_path):
            total_beats = 0
            correct_beats = 0  # Initialize the correctBeats counter

            # Create sets to track matching files
            beat_files = set()
            command_files = set()

            # Iterate over files in the "files" directory to populate sets
            for file in os.listdir(files_path):
                if file.startswith("beat") and file.endswith(".csv"):
                    beat_files.add(file.replace("beat", ""))
                elif file.startswith("command") and file.endswith(".csv"):
                    command_files.add(file.replace("command", ""))

            # Find matching files
            matching_files = beat_files & command_files

            # Iterate over matching files and process them
            for match in matching_files:
                beat_file = f"beat{match}"
                command_file = f"command{match}"

                beat_file_path = os.path.join(files_path, beat_file)
                command_file_path = os.path.join(files_path, command_file)

                if os.path.isfile(beat_file_path):
                    with open(beat_file_path, newline='') as csvfile:
                        reader = csv.reader(csvfile)
                        row_count = sum(1 for row in reader) - 1  # Subtract 1 for the header row
                        total_beats += row_count

                if os.path.isfile(command_file_path):
                    with open(command_file_path, newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            command_name = row[' command_name']
                            if command_name in ["Attack", "Defend", "Retreat", "Infantry", "Archer"]:
                                correct_beats += 4
                            elif command_name == "Cavalry":
                                correct_beats += 6
                            elif command_name == "SpawnBalls":
                                correct_beats += 8
                            elif command_name in ["FireLeftCannon", "FireRightCannon"]:
                                correct_beats += 5

            # Append the user and their total beats and correct beats count to the results list
            results.append({"user": user_dir, "total_beats": total_beats, "correct_beats": correct_beats})

# Define the output CSV file path
output_csv = "./beat_counts.csv"

# Write the results to the CSV file
with open(output_csv, mode='w', newline='') as csv_file:
    fieldnames = ["user", "total_beats", "correct_beats"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        writer.writerow(result)
