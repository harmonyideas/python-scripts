import matplotlib.pyplot as plt
import random
import numpy as np

a_list = random.sample(range(50), 50)
y_pos = np.arange(len(a_list))
plt.title('Bubble Sort (Short) Algorithm')
ax = plt.bar(y_pos, a_list, align='center', color='g', edgecolor='w')

swap = True
numpasses = len(a_list) - 1
while numpasses > 0 and swap:
    plt.pause(0.2)
    swap = False
    # Adjust individual bars to proper height of a_list[index]
    for i in range(numpasses):
        if a_list[i] > a_list[i + 1]:
            swap = True
            temp = a_list[i]
            ax[i].set_height(a_list[i + 1])
            a_list[i] = a_list[i + 1]
            a_list[i + 1] = temp
            ax[i + 1].set_height(temp)
    numpasses = numpasses-1

# Window will close without this
plt.show()
