import csv
import matplotlib.pyplot as plt
from collections import Counter

with open('tweets.csv') as csvfile:
    fieldnames = ['status_id',
                  'created_at',
                  'user_id',
                  'screen_name',
                  'text']

    stats = csv.DictReader(csvfile, delimiter=',', quotechar='"', fieldnames=fieldnames)
    next(stats)

    a_list = [row['created_at'][11:13] for row in stats]

values = Counter(a_list)
x_values, y_values = zip(*values.items())

plt.style.use(['ggplot'])
ax = plt.bar(x_values, y_values, color='r')

plt.title('Tweets by time of day')
plt.ylabel('Tweets')
plt.xlabel('Time of day')
plt.show()
