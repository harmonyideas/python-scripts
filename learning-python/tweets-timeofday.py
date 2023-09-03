import csv
import matplotlib.pyplot as plt
from collections import Counter

a_list = []

with open('tweets.csv') as csvfile:
    fieldnames = ['status_id',
                  'created_at',
                  'user_id',
                  'screen_name',
                  'text']

    stats = csv.DictReader(csvfile, delimiter=',', quotechar='"', fieldnames=fieldnames)
    stats.next()

    for row in stats:
        a_list.append((row['created_at'][11:13]))

values = Counter(a_list)
x_values = values.keys()
y_values = values.values()

plt.style.use(['ggplot'])
ax = plt.bar(x_values, y_values, color='r')

plt.title('Tweets by time of day')
plt.ylabel('Tweets')
plt.xlabel('Time of day')
plt.show()
