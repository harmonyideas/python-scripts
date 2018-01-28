import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

plt.style.use(['ggplot'])
fig, (ax) = plt.subplots()

# Widgets Produced
x_values = [x for x in range(100, 600, 100)]
# C(x) = (variable costs) + (fixed costs) = 20x + 10000
y_values = [((20 * x) + 10000) for x in range(100, 600, 100)]
# R(x) = (widgets * price) = $80/widget
revenue = [(80 * x) for x in range(100, 600, 100)]

z1 = np.array(y_values)

ax.plot(x_values, y_values, color='r')
ax.fill_between(x_values, revenue, y_values,
                where=z1 < revenue, color='g', alpha=0.5, interpolate=True)

ax.plot(x_values, revenue, color='g')
ax.fill_between(x_values, revenue, y_values,
                where=z1 > revenue, color='r', alpha=0.5, interpolate=True)

# R(x) = C(x)
ax.annotate('Break even', xy=(166.66, 13333), xytext=(95, 20000),
            arrowprops=dict(facecolor='black', shrink=0.05),)

red_patch = mpatches.Patch(color='red', label='Loss')
green_patch = mpatches.Patch(color='green', label='Gain')

plt.legend(handles=[red_patch, green_patch], loc=4)
plt.title('Business: Profit and loss analysis')
plt.ylabel('Fixed Cost')
plt.xlabel('Widgets Produced')
plt.show()
