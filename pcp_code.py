# reference:https://benalexkeen.com/parallel-coordinates-in-matplotlib/ 

import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import ticker

# the reference set loaded as a numpy matrix
all_soln = np.loadtxt(open("GAA-reference-set.csv"), delimiter=",")

# the indices of the non-dominated solutions from the Pareto set
# the best-weighted solution is on line 561
nd_indices = np.loadtxt(open("non-dominated-index.csv"), delimiter=",")

# the 10 objectives of the reference set
objs = ['NOISE', 'WEMP', 'DOC', 'ROUGH', 'WFUEL', 'PURCH', 'RANGE', 'LDMAX', 'VCMAX', 'PFPF']

# create an array of integers ranging from 0 to the number of objectives
x = [i for i, _ in enumerate(objs)]

# create a figure and its associated axes along the x axis
# there are len(x)-1 subplots
# sharey=False indicates that all the subplot y-axes will be set to different values
# by default, sharex=TRUE so fig2 will have only one x-axis
fig2, ax2 = plt.subplots(1,len(x)-1, sharey=False, figsize=(15,5))

min_max_range = {}
for i in range(len(objs)):
    all_soln[:,i] = np.true_divide(all_soln[:,i] - min(all_soln[:,i]), np.ptp(all_soln[:,i]))
    min_max_range[objs[i]] = [min(all_soln[:,i]), max(all_soln[:,i]), np.ptp(all_soln[:,i])]
    
# enumerate through all the axes in the figure and plot the data
# only the first line of each 
# blue for the nondominated solutions
# orange for the best-weighted solution
# grey or everthing else
for i, ax_i in enumerate(ax2):
    for d in range(len(all_soln)):
        if (d in nd_indices):
            if (d == nd_indices[0]):
                ax_i.plot(objs, all_soln[d, :], color='blue', alpha=0.3, label='Nondominated', linewidth=2)
            elif (d == 560):
                ax_i.plot(objs, all_soln[d, :], color='darkorange', label='Best-weighted', linewidth=2.5)
            else:
                ax_i.plot(objs, all_soln[d, :], color='blue', alpha=0.3, linewidth=2)
        else:
            if (d == 0):
                ax_i.plot(objs, all_soln[d, :], color='lightgrey', label='Dominated', alpha=0.4, linewidth=2)
            else:
                ax_i.plot(objs, all_soln[d, :], color='lightgrey', alpha=0.4, linewidth=2)
    ax_i.set_xlim([x[i], x[i+1]])

# function for setting ticks and tick_lables along the y-axis of each subplot
def set_ticks_for_axis(dim, ax_i, ticks):
    min_val, max_val, v_range = min_max_range[objs[dim]]
    step = v_range/float(ticks)
    tick_labels = [round(min_val + step*i, 2) for i in range(ticks)]
    norm_min = min(all_soln[:,dim])
    norm_range = np.ptp(all_soln[:,dim])
    norm_step =(norm_range/float(ticks-1))
    ticks = [round(norm_min + norm_step*i, 2) for i in range(ticks)]
    ax_i.yaxis.set_ticks(ticks)
    ax_i.set_yticklabels(tick_labels)

# enumerating over each axis in fig2
for dim, ax_i in enumerate(ax2):
    ax_i.xaxis.set_major_locator(ticker.FixedLocator([dim]))  # set tick locations along the x-axis
    set_ticks_for_axis(dim, ax_i, ticks=10)   # set ticks along the y-axis

# create a twin axis on the last subplot of fig2
# this will enable you to label the last axis with y-ticks 
ax3 = plt.twinx(ax2[-1])
dim = len(ax2)
ax3.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x [-1]]))
set_ticks_for_axis(dim, ax3, ticks=10)
ax3.set_xticklabels([objs[-2], objs[-1]])

plt.subplots_adjust(wspace=0, hspace=0.2, left=0.1, right=0.85, bottom=0.1, top=0.9)
ax2[8].legend(bbox_to_anchor=(1.25, 1), loc='upper left', prop={'size': 10})
plt.title("PCP Example")
plt.savefig("example.png")
plt.show()
