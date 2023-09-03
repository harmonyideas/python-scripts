import csv
import matplotlib.pyplot as plt

y_values = []
x_values = list(range(1980, 2011))
x_values.insert(0, 'country')

# Should be using the pandas library for this - will update in future
with open('populationbycountry19802010millions.csv', 'rU') as csvfile:
    fieldnames = x_values
    stats = csv.DictReader(csvfile, delimiter=',', quotechar='"', fieldnames=fieldnames)

    for row in stats:
        if row['country'] == 'North America':
            for v in x_values:
                y_values.append(row[(v)])

plt.style.use(['ggplot'])
ax = plt.plot(x_values[1:], y_values[1:])
plt.title('Population of North America')
plt.ylabel('Population')
plt.xlabel('Year')
plt.show()


