import matplotlib.pyplot as plt
import random
import numpy as np

# create initial plot with blank bars
x_values = random.sample(range(25), 25)
y_values = np.arange(len(x_values))
fig, ax = plt.subplots()
rects = ax.bar(y_values, np.zeros(len(x_values)), align='center', color='g', edgecolor='w')
plt.title('Bubble Sort Algorithm')
plt.ylim([0, max(x_values)])

# perform bubble sort and update plot
swap = True
numpasses = len(x_values) - 1
while numpasses > 0 and swap:
    swap = False
    for i in range(numpasses):
        if x_values[i] > x_values[i + 1]:
            swap = True
            x_values[i], x_values[i + 1] = x_values[i + 1], x_values[i]
            rects[i].set_height(x_values[i])
            rects[i + 1].set_height(x_values[i + 1])
            fig.canvas.draw_idle()
            plt.pause(.1)
    numpasses = numpasses - 1

plt.show()
