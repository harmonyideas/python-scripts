import matplotlib.pyplot as plt
import random
import numpy as np

plt.style.use(['ggplot'])
plt.figure(num=None, figsize=(13, 8), dpi=80, facecolor='w', edgecolor='k')
a_list = random.sample(range(50), 50)
y_pos = np.arange(len(a_list))


for passnum in range(len(a_list), 0, -1):
    plt.clf()
    plt.bar(a_list, y_pos, align='center', color='g', alpha=0.5)

    for i in range(passnum - 1):
        if a_list[i] > a_list[i + 1]:
            temp = a_list[i]
            a_list[i] = a_list[i + 1]
            a_list[i + 1] = temp
    plt.xticks(a_list, y_pos)
    plt.draw()
    plt.pause(.01)
    # time.sleep(0.001)
    
# Window will close without this - need to fix and update individual bars instead
plt.show()
plt.close()

