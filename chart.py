import matplotlib.pylab as plt
from matplotlib.collections import EventCollection

def draw_chart(*dicts, *colours):
    for dict in dicts:
        lists = sorted(dict.items()) # sorted by key, return a list of tuples
        x, y = zip(*lists) # unpack a list of pairs into two tuples
        plt.plot(x, y, color='tab:orange')
        xevents = EventCollection(x, color='tab:orange', linelength=0.05)
        yevents = EventCollection(y, color='tab:orange', linelength=0.05, orientation='vertical')
    plt.show()
    return

