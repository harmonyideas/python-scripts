import matplotlib.pyplot as plt
import random
import numpy as np

plt.style.use(['ggplot'])
a_list = random.sample(range(50), 50)
y_pos = np.arange(len(a_list))
ax = plt.bar(y_pos, a_list, align='center', color='g', edgecolor='w')
plt.title('Bubble Sort Algorithm')

for passnum in range(len(a_list), 0, -1):
    plt.pause(.1)
    for i in range(passnum - 1):
        if a_list[i] > a_list[i + 1]:
            ax[i].set_height(a_list[i + 1])
            temp = a_list[i]
            a_list[i] = a_list[i + 1]
            a_list[i + 1] = temp
            ax[i + 1].set_height(temp)

# Window will close without this - need to fix and update individual bars instead
plt.show()


