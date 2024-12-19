import matplotlib.pyplot as plt

# Data from the image
ages = [17, 19, 20, 21, 22, 23, 24, 26, 25]
counts = [2, 1, 1, 16, 3, 3, 5, 1, 1]

# Create a bar plot
fig, ax = plt.subplots()

bars = ax.bar(ages, counts, color='#4d7a95')

# Adding the percentage labels on top of the bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval}', va='bottom', ha='center')

ax.set_xlabel('Starost', fontsize=14)
ax.set_ylabel('Število odgovorov', fontsize=14)
ax.set_title('Starost testirancev', fontsize=16, pad=15)
ax.set_xticks(ages)

plt.tight_layout()
plt.show()
