import matplotlib.pyplot as plt
import random
import numpy as np

x_values = random.sample(range(25), 25)
y_values = np.arange(len(x_values))
plt.title('Bubble Sort Algorithm')
ax = plt.bar(y_values, x_values, align='center', color='g', edgecolor='w')

swap = True
numpasses = len(x_values) - 1
while numpasses > 0 and swap:
    swap = False
    # Adjust individual bars to proper height of a_list[index]
    for i in range(numpasses):
        plt.pause(0.1)
        if x_values[i] > x_values[i + 1]:
            swap = True
            ax[i].set_height(x_values[i + 1])
            ax[i + 1].set_height(x_values[i])
            x_values[i], x_values[i + 1] = x_values[i + 1], x_values[i]
    numpasses = numpasses-1

# Window will close without this
plt.show()

