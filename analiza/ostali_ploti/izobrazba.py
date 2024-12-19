import matplotlib.pyplot as plt

# Data from the image
categories = ["Ne obiskujem.", "1 do 3 leta", "3 do 5 let", "več kot 5 let"]
percentages = [66.7, 9.1, 3, 21.2]

# Define colors to match the request
colors = ['#E4A7BF', '#A9D18E', '#64A041', '#38761D']

# Set default font size for labels and percentage text
plt.rcParams.update({'font.size': 14})

# Create a pie chart
fig, ax = plt.subplots()

ax.pie(percentages, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
ax.set_title('Ali obiskujete / ste obiskovali glasbeno šolo?\nČe da, koliko let?', fontsize=16)

plt.tight_layout()
plt.show()
