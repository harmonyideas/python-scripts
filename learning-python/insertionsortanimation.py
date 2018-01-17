import matplotlib.pyplot as plt
import random
import numpy as np

plt.style.use(['ggplot'])
plt.figure(num=None, figsize=(13, 8), dpi=80, facecolor='w', edgecolor='k')

a_list = random.sample(range(100), 100)
y_pos = np.arange(len(a_list))
colors = np.random.rand(len(a_list))

for index in range(1,len(a_list)):
    
    currentkey = a_list[index]
    position = index

    while position > 0 and a_list[position - 1] > currentkey:
        a_list[position] = a_list[position-1]
        position = position-1
    a_list[position] = currentkey

# Need to change individual bars instead of clearing current axes
    plt.clf()
    plt.scatter(a_list, y_pos, c=colors, marker='*', alpha=0.5)
    plt.pause(0.001)

# Window will close without this
plt.show()

