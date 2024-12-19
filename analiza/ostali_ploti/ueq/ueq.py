import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
data = pd.read_csv('./data.csv')
# Extract relevant columns for further analysis
columns_of_interest = [
    "ID naprave - ID Uporabnika",
    "Zgodba",
    "Ocenite igro.(1-se ne da upravljat, 5-z lahkoto vpravlja)",
    "Ocenite igro (1-komplicirana, 5 enostavna)",
    "Ocenite igro. (1-ni učinkovita, 5 učinkovita)",
    "Ocenite igro.(1-dolgočasna, 5-napeta)",
    "Ocenite igro. (1-nezanimiva, 5-zanimiva)",
    "Ocenite igro. (1-stara, 5-nova)",
    "Ocenite igro. (1-zastarela, 5-moderna)"
]



# Filter the data
filtered_data = data[columns_of_interest]

# Separate the data by group
data_with_story = filtered_data[filtered_data['Zgodba'] == 'Da']
data_without_story = filtered_data[filtered_data['Zgodba'] == 'Ne']


# List of questions to analyze
questions = [
    "Ocenite igro.(1-se ne da upravljat, 5-z lahkoto vpravlja)",
    "Ocenite igro (1-komplicirana, 5 enostavna)",
    "Ocenite igro. (1-ni učinkovita, 5 učinkovita)",
    "Ocenite igro.(1-dolgočasna, 5-napeta)",
    "Ocenite igro. (1-nezanimiva, 5-zanimiva)",
    "Ocenite igro. (1-stara, 5-nova)",
    "Ocenite igro. (1-zastarela, 5-moderna)"
]
# Recalculate the mean values for both groups
mean_values_with_story = data_with_story[questions].mean()
mean_values_without_story = data_without_story[questions].mean()

# Labels for the bars
# Labels for the bars
labels = [
    "Upravljivost",
    "Enostavnost",
    "Učinkovitost",
    "Napetost",
    "Zanimivost",
    "Novost",
    "Modernost"
]

# Plotting the horizontal bar chart
y = np.arange(len(labels))
height = 0.4

fig, ax = plt.subplots(figsize=(10, 7))

bars1 = ax.barh(y - height/2, mean_values_with_story, height, label='Z zgodbo', color='#8DB973')
bars2 = ax.barh(y + height/2, mean_values_without_story, height, label='Brez zgodbe', color='#E2B2C5')

# Adding some text for labels, title and custom y-axis tick labels, etc.
ax.set_xlabel('Povprečne ocene', fontsize=15)
ax.set_ylabel('Kriteriji', fontsize=15, labelpad=10)
ax.set_title('Povprečne ocene uporabniške izkušnje za obe verziji igre', fontsize=16, pad=15)
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.set_xlim(0, 5)  # Setting x-axis limit to 5

# Adding value labels on top of the bars
def add_labels(bars):
    for bar in bars:
        width = bar.get_width()
        ax.annotate('{}'.format(round(width, 2)),
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0),  # 3 points horizontal offset
                    textcoords="offset points",
                    ha='left', va='center',
                    fontsize=14)

add_labels(bars1)
add_labels(bars2)

# Adjusting legend position
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False, fontsize=14)

# Increase font size for x and y axis tick labels
ax.tick_params(axis='both', which='major', labelsize=14)

plt.tight_layout()
plt.show()
