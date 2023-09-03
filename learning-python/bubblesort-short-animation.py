import matplotlib.pyplot as plt
import random
import numpy as np

fig = plt.gcf()
fig.show()

x_values = random.sample(range(25), 25)
y_values = np.arange(len(x_values))
plt.title('Bubble Sort Algorithm')
ax = plt.bar(y_values, x_values, align='center', color='g', edgecolor='w')

swap = True
numpasses = len(x_values) - 1
while numpasses > 0 and swap:
    swap = False
    # Adjust individual graph bars to proper height
    for i in range(numpasses):
        fig.canvas.draw()
        if x_values[i] > x_values[i + 1]:
            swap = True
            ax[i].set_height(x_values[i + 1])
            ax[i + 1].set_height(x_values[i])
            x_values[i], x_values[i + 1] = x_values[i + 1], x_values[i]
    numpasses = numpasses - 1

# Window will close without this
plt.show()
