import csv
import matplotlib.pyplot as plt

with open('populationbycountry19802010millions.csv', 'rU') as csvfile:
    stats = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in stats:
        if row['country'] == 'North America':
            x_values = sorted(row.keys())
            y_values = sorted(row.values())

plt.style.use(['ggplot'])
ax = plt.plot(x_values[:-1], y_values[:-1])
plt.title('Population of North America')
plt.ylabel('Population')
plt.xlabel('Year')
plt.show()





