import matplotlib.pyplot as plt
import random
import numpy as np

plt.style.use(['ggplot'])
plt.figure(num=None, figsize=(13, 8), dpi=80, facecolor='w', edgecolor='k')

a_list = random.sample(range(100), 100)
y_pos = np.arange(len(a_list))
colors = np.random.rand(len(a_list))

for temp_slot in range(len(a_list)-1, 0, -1):
    max_pos = 0
    for position in range(1, temp_slot + 1):
        if a_list[position] > a_list[max_pos]:
            max_pos = position

    temp = a_list[temp_slot]
    a_list[temp_slot] = a_list[max_pos]
    a_list[max_pos] = temp

    # Need to change individual bars instead of clearing current axes
    plt.clf()
    plt.scatter(a_list, y_pos, c=colors, alpha=0.5)
    plt.pause(0.001)

# Window will close without this
plt.show()

