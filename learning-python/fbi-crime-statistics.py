import csv
import matplotlib.pyplot as plt

a_list = []

# We should be using pandas library for this
with open('fbi-stats.csv') as csvfile:
    stats = csv.DictReader(csvfile, delimiter=',', quotechar='"')

    for row in stats:
        a_list.append((row['Year'][0:4], row['Violent\ncrime'].replace(",", "")))

x_values = [x[0] for x in a_list]
y_values = [y[1] for y in a_list]

plt.style.use(['ggplot'])
ax = plt.plot(x_values, y_values, color='r')
plt.title('FBI Violent Crime Statistics')
plt.ylabel('Volume')
plt.xlabel('Year')
plt.show()







