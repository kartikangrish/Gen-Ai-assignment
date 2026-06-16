# ==============================================================================
# MATPLOTLIB ASSIGNMENT 
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

# Data Setup
x = np.arange(0, 100)
y = x * 2
z = x ** 2


# --- Exercise 1 ---
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.plot(x, y)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('title')


# --- Exercise 2 ---
fig2 = plt.figure()
ax1 = fig2.add_axes([0, 0, 1, 1])
ax2 = fig2.add_axes([0.2, 0.5, .2, .2])


# --- Exercise 3 ---
# Part 1: Blank inner plot creation
fig3 = plt.figure()
ax_main = fig3.add_axes([0, 0, 1, 1])
ax_inset = fig3.add_axes([0.2, 0.5, .4, .4])

# Part 2: Filled curves with custom limits
fig3_filled = plt.figure()
ax_main = fig3_filled.add_axes([0, 0, 1, 1])
ax_inset = fig3_filled.add_axes([0.2, 0.5, .4, .4])

# Plot main graph
ax_main.plot(x, z, color='b', lw=1)
ax_main.set_xlabel('X')
ax_main.set_ylabel('Z')
ax_main.set_xlim([0, 100])
ax_main.set_ylim([0, 10000])

# Plot inset zoom graph
ax_inset.plot(x, y, color='b', lw=1)
ax_inset.set_xlabel('X')
ax_inset.set_ylabel('Y')
ax_inset.set_title('zoom')
ax_inset.set_xlim([20.0, 22.0])
ax_inset.set_ylim([30, 50])


# --- Exercise 4 ---
# Part 1: Default layout subplots
fig4, axes = plt.subplots(nrows=1, ncols=2)

# Part 2: Plot curves with distinct styles and line weights
fig4_styled, axes_styled = plt.subplots(nrows=1, ncols=2)
axes_styled[0].plot(x, y, color='blue', lw=3, ls='--')
axes_styled[1].plot(x, z, color='red', lw=4, ls='-')

# Part 3: Resized layout subplots using figsize parameter
fig4_resized, axes_resized = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
axes_resized[0].plot(x, y, color='blue', lw=4, ls='-')
axes_resized[0].set_xlabel('x')
axes_resized[0].set_ylabel('y')

axes_resized[1].plot(x, z, color='red', lw=2, ls='--')
axes_resized[1].set_xlabel('x')
axes_resized[1].set_ylabel('z')

# Show all generated plots
plt.show()

