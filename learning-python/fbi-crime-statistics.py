import csv
import matplotlib.pyplot as plt

a_list = []

with open('fbi-stats.csv') as csvfile:
    fieldnames = ['Year', 'Population1', 'Violent Crime', 'Violent crime rate', 
                  'Murder and nonnegligent manslaughter', 'Murder and nonnegligent manslaughter rate', 'Rape', 
                  'Rape rate', 'Rape(legacy)', 'Rape (legacy) rate', 'Robbery', 'Robbery rate', 'Aggravated assault', 
                  'Aggravated', 'assault rate', 'Property crime', 'Property crime rate ', 'Burglary', 'Burglary rate ',
                  'Larceny-theft', 'Larceny-theft rate', 'Motor vehicle theft', 'Motor vehicle theft rate']

    stats = csv.DictReader(csvfile, delimiter=',', quotechar='"', fieldnames=fieldnames)
    
    for row in stats:
        a_list.append((row['Year'][0:4], row['Violent Crime'].replace(",", "")))

x_values = [x[0] for x in a_list]
y_values = [y[1] for y in a_list]

plt.style.use(['ggplot'])
ax = plt.plot(x_values, y_values, color='r')

plt.title('FBI Violent Crime Statistics')
plt.ylabel('Volume')
plt.xlabel('Year')
plt.show()



