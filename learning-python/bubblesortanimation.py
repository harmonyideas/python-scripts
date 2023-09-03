import matplotlib.pyplot as plt
import random
import numpy as np

plt.style.use(['ggplot'])
x_values = random.sample(range(50), 50)
y_values = np.arange(len(x_values))
ax = plt.bar(y_values, x_values, align='center', color='g', edgecolor='w')
plt.title('Bubble Sort Algorithm')

for numpasses in range(len(x_values), 0, -1):
    for i in range(numpasses - 1):
        plt.pause(.01)
        if x_values[i] > x_values[i + 1]:
            ax[i].set_height(x_values[i + 1])
            ax[i + 1].set_height(x_values[i])
            x_values[i], x_values[i + 1] = x_values[i + 1], x_values[i]

# Window will close without this - need to fix and update individual bars instead
plt.show()




